import { KvsRecord } from "../../interfaces/core/Record/KvsRecord";
import { ApiErrorResponse, ApiResponse, ApiSuccessResponse, CarinaeServiceInterface } from "../../interfaces/public-services/CarinaeInterface";
import { CoreStorageServiceInterface } from "../../interfaces/raw-services/CoreStorageService";
import { HashingServiceInterface } from "../../interfaces/raw-services/HashingService";
import { KeyServiceInterface } from "../../interfaces/raw-services/KeyService";
import { LockServiceInterface } from "../../interfaces/raw-services/LockService";
import { KvsEntryInterface } from "../../interfaces/core/Data/KvsEntryInterface";
import { KvsKeyInterface } from "../../interfaces/core/Key/KvsKeyInterface";
import { createError, createSuccess } from "../../utils/utils-0";
import { Metadata } from "../../raw-services/metadata/Metadata";
import { MessageInterface } from "../../interfaces/core/Messages/Message";
import { EventBusServiceInterface } from "../../interfaces/raw-services/EventBusService";






export class Carinae implements CarinaeServiceInterface {
    private readonly storageService: CoreStorageServiceInterface;
    private readonly keyService: KeyServiceInterface;
    private readonly lockService: LockServiceInterface;
    private readonly hashingService: HashingServiceInterface;
    private readonly eventBusService: EventBusServiceInterface;




    constructor(dependencies: {
        storageService: CoreStorageServiceInterface;
        keyService: KeyServiceInterface;
        lockService: LockServiceInterface;
        hashingService: HashingServiceInterface;
        eventBusService: EventBusServiceInterface;
    }) {
        this.storageService = dependencies.storageService;
        this.keyService = dependencies.keyService;
        this.lockService = dependencies.lockService;
        this.hashingService = dependencies.hashingService;
        this.eventBusService = dependencies.eventBusService;
    }



    public async Get<T>(Key: KvsKeyInterface, options?: any): Promise<ApiResponse<KvsRecord<T>>> {
        try {
            const stringKey = this.keyService.Encode(Key);
            const entry = await this.storageService.Get<T>(stringKey);

            if (!entry) {
                return createError('NOT_FOUND', `Record with key "${stringKey}" not found.`);
            }

            const record = { Key: Key, Value: entry };
            return createSuccess(record);
        } catch (err: any) {
            return createError('INTERNAL_ERROR', 'An unexpected error occurred during Get.', err.message);
        }
    }


    public async Set<T>(record: KvsRecord<T>, options?: any): Promise<ApiResponse<void>> {
        try {
            const stringKey = this.keyService.Encode(record.Key);
            let finalEntry: KvsEntryInterface<T>;

            await this.lockService.FineGrainedExecuteAtomic(stringKey, async () => {
                const existingEntry = await this.storageService.Get<T>(stringKey);
                const newDataHash = await this.hashingService.Hash(record.Value.Value);

                const metadataManager = new Metadata(existingEntry?.Metadata);

                metadataManager.IncrementVersion();
                metadataManager.UpdateDataHash(newDataHash);

                if (existingEntry) {
                    const oldMeta = existingEntry.Metadata;
                    metadataManager.UpdateUpdatedAt(Date.now());
                    metadataManager.AddRevisionHistory({
                        Version: oldMeta.Version,
                        DataHash: oldMeta.DataHash,
                        Timestamp: oldMeta.UpdatedAt,
                        ModifiedBy: oldMeta.ModifiedBy,
                    });
                }

                const finalMetadata = metadataManager.GetState();

                finalEntry = {
                    Value: record.Value.Value,
                    Metadata: finalMetadata
                };

                await this.storageService.Set(stringKey, finalEntry);
            });

            const eventMessage: MessageInterface = {
                Type: 'SET',
                Key: stringKey,
                Value: finalEntry!.Value,
                Timestamp: finalEntry!.Metadata.UpdatedAt
            };
            this.eventBusService.PublishForAllTopics(stringKey, 'SET', eventMessage);

            return createSuccess(undefined);
        } catch (err: any) {
            return createError('INTERNAL_ERROR', 'An unexpected error occurred during Set.', err.message);
        }
    }


    public async Delete(Key: KvsKeyInterface): Promise<ApiResponse<{ deleted: boolean }>> {
        try {
            const stringKey = this.keyService.Encode(Key);
            const result = await this.lockService.ExecuteAtomic(stringKey, () => {
                return this.storageService.Delete(stringKey);
            });
            if (result) {
                const eventMessage: MessageInterface = {
                    Type: 'DELETE',
                    Key: stringKey,
                    Value: null,
                    Timestamp: Date.now()
                };
                this.eventBusService.PublishForAllTopics(stringKey, 'DELETE', eventMessage);

            }
            return createSuccess({ deleted: result });
        } catch (err: any) {
            return createError('INTERNAL_ERROR', 'An unexpected error occurred during Delete.', err.message);
        }
    }

    public async Keys(): Promise<ApiResponse<KvsKeyInterface[]>> {
        try {
            const stringKeys = await this.storageService.Keys();
            const structuredKeys = stringKeys.map(key => this.keyService.Decode(key));
            return createSuccess(structuredKeys);
        } catch (err: any) {
            return createError('INTERNAL_ERROR', 'An unexpected error occurred during Keys.', err.message);
        }
    }
}