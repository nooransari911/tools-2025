import { KvsEntryInterface } from "../../interfaces/core/Data/KvsEntryInterface";
import { CoreStorageServiceInterface } from "../../interfaces/raw-services/CoreStorageService";


export class MemoryStorage implements CoreStorageServiceInterface {
    private static store = new Map <string, KvsEntryInterface <any>>();

    Get = async <T> (Key: string): Promise <KvsEntryInterface <T> | undefined> => {
        const record: KvsEntryInterface <T> | undefined = MemoryStorage.store.get (Key);
        return record;
    }

    Set = async <T> (Key: string, entry: KvsEntryInterface <T>): Promise <void> => {
        MemoryStorage.store.set (Key, entry);
        return;
    }

    Delete = async (Key: string): Promise <boolean> => {
        const existed: boolean = MemoryStorage.store.has (Key);
        const deleted: boolean = MemoryStorage.store.delete (Key);
        return deleted;
    }

    Keys = async (): Promise <string []> => {
        const keys: string [] = [...MemoryStorage.store.keys ()];
        return keys;
    }
}