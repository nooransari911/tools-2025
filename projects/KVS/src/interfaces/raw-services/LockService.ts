export interface LockServiceInterface {
    ExecuteAtomic<T>(resourceId: string, operation: () => Promise<T>): Promise<T>;
    FineGrainedExecuteAtomic <T> (resourceId: string, operation: () => Promise <T>): Promise <T>;
}