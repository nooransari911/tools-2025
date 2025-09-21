import KvsEntryInterface from "../core/Data/KvsEntryInterface"



export interface CoreStorageServiceInterface {
    Get <T> (Key: string): Promise <KvsEntryInterface <T> | undefined>;
    Set <T> (Key: string, entry: KvsEntryInterface <T>): Promise <void>;
    Delete (Key: string): Promise <boolean>;
    Keys (): Promise<string[]>;
}
