import { Carinae } from '@src/public-services/core/Carinae';
import { MemoryStorage } from '@src/raw-services/storage/MemoryStorage';
import { KeyService } from '@src/raw-services/key/Key';
import { LockService } from '@src/raw-services/concurrency/Locks';
import { HashingService } from '@src/raw-services/hash/Hash';
import { EventBus } from '@src/raw-services/message/EventBus';

/**
 * Creates a fully wired-up Carinae instance for testing.
 * @returns An object containing the Carinae instance and its dependencies.
 */
export function createTestInstance() {
  const storageService = new MemoryStorage();
  const keyService = new KeyService();
  const lockService = new LockService();
  const hashingService = new HashingService();
  const eventBusService = new EventBus ();

  const carinae = new Carinae({
    storageService,
    keyService,
    lockService,
    hashingService,
    eventBusService,
  });

  return {
    carinae,
    keyService,
    eventBus: eventBusService,
  };
}