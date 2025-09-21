import { KvsKeyInterface } from '@src/interfaces/core/Key/KvsKeyInterface';
import { KvsRecord } from '@src/interfaces/core/Record/KvsRecord';
import { MetadataInterface } from '@src/interfaces/core/Metadata/MetadataInterface';
import { TestCase } from '../runner/TestRunner';
import assert from 'assert/strict';

export const basicCrudTests: TestCase[] = [
    {
        title: 'Set a simple key and verify the SET event',
        async testFn({ carinae, keyService, eventConsumer }) {
            eventConsumer.clear();

            const simpleKey: KvsKeyInterface = { File: 'name' };
            const simpleValue = 'my-name';
            const simpleStringKey = keyService.Encode(simpleKey);

            const record: KvsRecord<string> = {
                Key: simpleKey,
                Value: { Value: simpleValue, Metadata: {} as MetadataInterface },
            };

            await carinae.Set(record);

            const event = await eventConsumer.waitForEvent('SET', simpleStringKey);

            assert.strictEqual(event.Value, simpleValue, 'Event value mismatch');
        },
    },
    {
        title: 'Get the previously set simple key',
        async testFn({ carinae }) {
            const simpleKey: KvsKeyInterface = { File: 'name' };
            const expectedValue = 'my-name';

            const response = await carinae.Get<string>(simpleKey);

            assert.equal(response.status, 'success', 'API response should be successful');
            if (response.status === 'success') { // Type guard
                assert.strictEqual(response.data.Value.Value, expectedValue);
            }
        },
    },
    {
        title: 'Set a namespaced key and verify the data',
        async testFn({ carinae, keyService, eventConsumer }) {
            eventConsumer.clear();

            const namespacedKey: KvsKeyInterface = { Namespace: ["organization", "users"], File: 'profile' };
            const namespacedValue = { id: 123, role: 'admin' };
            const namespacedStringKey = keyService.Encode(namespacedKey);

            const record: KvsRecord<object> = {
                Key: namespacedKey,
                Value: { Value: namespacedValue, Metadata: {} as MetadataInterface },
            };

            await carinae.Set(record);
            await eventConsumer.waitForEvent('SET', namespacedStringKey);

            const response = await carinae.Get<object>(namespacedKey);
            assert.equal(response.status, 'success');
            if (response.status === 'success') {
                assert.deepStrictEqual(response.data.Value.Value, namespacedValue);
            }
        },
    },
    {
        title: 'Get the previously set namespaced key',
        async testFn({ carinae, keyService, eventConsumer }) {
            const namespacedKey: KvsKeyInterface = { Namespace: ["organization", "users"], File: 'profile' };
            const namespacedStringKey = keyService.Encode(namespacedKey);
            const expectedValue = { id: 123, role: 'admin' };

            const response = await carinae.Get<object>(namespacedKey);

            assert.equal(response.status, 'success', 'API response should be successful');
            if (response.status === 'success') { // Type guard
                assert.deepStrictEqual(response.data.Value.Value, expectedValue);
            }
        },
    },
    {
        title: 'Delete the namespaced key and verify the DELETE event',
        async testFn({ carinae, keyService, eventConsumer }) {
            eventConsumer.clear();

            const namespacedKey: KvsKeyInterface = { Namespace: ["organization", "users"], File: 'profile' };
            const namespacedStringKey = keyService.Encode(namespacedKey);

            const deletePromise = carinae.Delete(namespacedKey);
            const eventPromise = eventConsumer.waitForEvent('DELETE', namespacedStringKey);

            const [response, event] = await Promise.all([deletePromise, eventPromise]);

            assert.equal(response.status, 'success');
            if (response.status === 'success') {
                assert.strictEqual(response.data.deleted, true, 'Delete operation should return true');
            }
            assert.strictEqual(event.Key, namespacedStringKey, 'Event key mismatch');
        }
    },

    {
        title: 'Verify the key is gone after deletion',
        async testFn({ carinae }) {
            const namespacedKey: KvsKeyInterface = { Namespace: ["organization", "users"], File: 'profile' };
            const response = await carinae.Get(namespacedKey);

            assert.equal(response.status, 'error', 'Expected an error response for a deleted key');
            if (response.status === 'error') {
                assert.equal(response.error.code, 'NOT_FOUND', 'Error code should be NOT_FOUND');
            }
        }
    }
];