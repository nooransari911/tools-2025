import { MemoryStorage } from '@src/raw-services/storage/MemoryStorage';
import { KeyService } from '@src/raw-services/key/Key';
import { HashingService } from '@src/raw-services/hash/Hash';
import { EventBus } from '@src/raw-services/message/EventBus';
import { KvsKeyInterface } from '@src/interfaces/core/Key/KvsKeyInterface';
import { KvsRecord } from '@src/interfaces/core/Record/KvsRecord';
import { MetadataInterface } from '@src/interfaces/core/Metadata/MetadataInterface';
import { LockService } from '@src/raw-services/concurrency/Locks';
import { Carinae } from '@src/public-services/core/Carinae';


// Helper function to format test output
const runTest = async (title: string, testFn: () => Promise<any>) => {
    console.log(`\n--- Running Test: ${title} ---`);
    try {
        const result = await testFn();
        if (result && result.status === 'error') {
            console.error(`🔴 Test Failed:`, result.error);
        } else {
            console.log('🟢 Test Passed');
        }
    } catch (e: any) {
        console.error(`🔴 Test Crashed: ${e.message}`);
    }
};


async function main() {
    console.log("Initializing Carinae KVS with in-memory services...");

    // --- 1. Setup Dependencies ---
    const storageService = new MemoryStorage();
    const keyService = new KeyService();
    const lockService = new LockService();
    const hashingService = new HashingService();
    const eventBusService = new EventBus();

    const carinae = new Carinae({
        storageService,
        keyService,
        lockService,
        hashingService,
        eventBusService: eventBusService
    });

    // --- 2. Setup Event Listeners ---
    // Listen for any 'SET' operation
    eventBusService.Subscribe('SET', (message) => {
        console.log(`[EVENT:SET] Key "${message.Key}" was set. Value:`, message.Value);
    });

    // Listen for any 'DELETE' operation
    eventBusService.Subscribe('DELETE', (message) => {
        console.log(`[EVENT:DELETE] Key "${message.Key}" was deleted.`);
    });


    // --- 3. Define Keys and Data ---
    const simpleKey: KvsKeyInterface = { File: 'name' };
    const simpleValue = 'my-name';

    const namespacedKey: KvsKeyInterface = { Namespace: ['institute-name', 'users'], File: 'profile' };
    const namespacedValue = { id: 123, role: 'admin' };


    // --- 4. Run Operations ---

    await runTest('Set a simple key-value pair', async () => {
        const record: KvsRecord<string> = {
            Key: simpleKey,
            Value: {
                Value: simpleValue,
                // For a new record, metadata can be empty; Carinae will build it.
                Metadata: {} as MetadataInterface
            }
        };
        return await carinae.Set(record);
    });

    await runTest('Set a namespaced key-value pair', async () => {
        const record: KvsRecord<object> = {
            Key: namespacedKey,
            Value: {
                Value: namespacedValue,
                Metadata: {} as MetadataInterface
            }
        };
        return await carinae.Set(record);
    });

    await runTest('Get the simple key', async () => {
        const response = await carinae.Get<string>(simpleKey);
        if (response.status === 'success') {
            console.log('  Retrieved Value:', response.data.Value.Value);
            if (response.data.Value.Value !== simpleValue) {
                throw new Error('Retrieved value does not match original!');
            }
        }
        return response;
    });

    await runTest('Get the namespaced key', async () => {
        const response = await carinae.Get<object>(namespacedKey);
        if (response.status === 'success') {
            console.log('  Retrieved Value:', response.data.Value.Value);
            if (JSON.stringify(response.data.Value.Value) !== JSON.stringify(namespacedValue)) {
                throw new Error('Retrieved object does not match original!');
            }
        }
        return response;
    });

    await runTest('List all keys', async () => {
        const response = await carinae.Keys();
        if (response.status === 'success') {
            console.log('  Available Keys:', response.data.map(k => keyService.Encode(k)));
        }
        return response;
    });

    await runTest('Delete the simple key', async () => {
        const response = await carinae.Delete(simpleKey);
        if (response.status === 'success') {
            console.log('  Delete successful:', response.data.deleted);
        }
        return response;
    });

    await runTest('Verify simple key is gone', async () => {
        const response = await carinae.Get(simpleKey);
        // We EXPECT an error here, so this is a pass.
        if (response.status === 'error' && response.error.code === 'NOT_FOUND') {
            console.log('  Correctly received NOT_FOUND error.');
            // Remap to a success for the test runner
            return { status: 'success' };
        }
        // If we get here, it's a failure
        return { status: 'error', error: { code: 'UNEXPECTED_FOUND', message: 'Key was found after deletion.' } };
    });

    await runTest('List keys after deletion', async () => {
        const response = await carinae.Keys();
        if (response.status === 'success') {
            console.log('  Remaining Keys:', response.data.map(k => keyService.Encode(k)));
        }
        return response;
    });
}


// Execute the main function
main().catch(error => {
    console.error("An unhandled error occurred in the test script:", error);
    process.exit(1);
});