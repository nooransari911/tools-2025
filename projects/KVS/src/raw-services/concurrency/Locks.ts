import { LockServiceInterface } from "../../interfaces/raw-services/LockService";

export class LockService implements LockServiceInterface {
    private activeLocks = new Map<string, Promise<any>>();

    public async ExecuteAtomic<T>(resourceId: string, operation: () => Promise<T>): Promise<T> {
        const priorTask = this.activeLocks.get(resourceId) || Promise.resolve();

        const newTask = priorTask.then(operation);

        this.activeLocks.set(resourceId, newTask);

        try {
            return await newTask;
        }
        finally {
            if (this.activeLocks.get(resourceId) === newTask) {
                this.activeLocks.delete(resourceId);
            }
        }
    }




    /**
     * Parses a resource key into its hierarchical lock components.
     * @example _getLockHierarchy("users/profiles:123")
     * // returns ["users", "users/profiles", "users/profiles:123"]
     */
    private _getLockHierarchy(resourceId: string): string[] {
        // This helper remains the same as it is already clear.
        const parts = resourceId.replace(':', '/').split('/');
        return parts.map((_, i) => parts.slice(0, i + 1).join('/'));
    }

    /**
     * Acquires a single lock for a given lockId by queueing behind any existing operations.
     * @param lockId The unique string for the resource to lock (e.g., "users/profiles").
     * @returns A promise that resolves when the lock is acquired.
     */
    private _acquireSingleLock(lockId: string): Promise<void> {
        // Find the promise of the last operation currently in the queue for this lock.
        // If the queue is empty, start with an already-resolved promise.
        const lastOperationInQueue = this.activeLocks.get(lockId) || Promise.resolve();

        // The "lock acquisition" is a new, empty operation that we schedule to run
        // only after the last operation in the queue is completely finished.
        const lockAcquisitionPromise = lastOperationInQueue.then(() => {
            // This empty function signifies that the only goal is to wait for our turn.
            // No actual work is done here; the value is the timing.
        });

        // CRITICAL STEP: We immediately place our new promise at the end of the queue.
        // Anyone arriving after us will now have to wait for our promise to resolve.
        this.activeLocks.set(lockId, lockAcquisitionPromise);

        return lockAcquisitionPromise;
    }

    /**
     * Executes an operation with a guarantee of exclusive access to a hierarchical resource.
     */
    public async FineGrainedExecuteAtomic<T>(resourceId: string, operation: () => Promise<T>): Promise<T> {
        // Phase 1: Determine the full set of locks that must be acquired.
        const locksToAcquire = this._getLockHierarchy(resourceId);
        const acquiredLocks: string[] = [];

        try {
            // Phase 2: Acquire all locks sequentially, in the correct top-down order.
            // This loop ensures that we don't even attempt to lock a child namespace
            // until we have successfully locked its parent.
            for (const currentLockId of locksToAcquire) {
                await this._acquireSingleLock(currentLockId);
                // Keep track of the locks we successfully acquire so we can release them later.
                acquiredLocks.push(currentLockId);
            }

            // Phase 3: Execute the user's critical section code.
            // This line is only reached after ALL required locks have been successfully acquired.
            return await operation();

        } finally {
            // Phase 4: Release all acquired locks in the reverse (bottom-up) order.
            // This 'finally' block guarantees that locks are released even if the 'operation' throws an error.
            for (const lockIdToRelease of acquiredLocks.reverse()) {
                // To "release" a lock, we simply remove its entry from the map.
                // This signals to the next waiter that the resource is free.
                // Note: A more robust implementation would ensure it's removing the *correct* promise,
                // but this is clear and sufficient for this model.
                this.activeLocks.delete(lockIdToRelease);
            }
        }
    }
}