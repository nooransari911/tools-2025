import { MetadataInterface } from "../core/Metadata/MetadataInterface"


export interface BaseMetadataServiceInterface {
    GetVersion (): number;
    IncrementVersion (): number;
    DecrementVersion (): number;

    GetModifiedBy (): string | undefined;
    UpdateModifiedBy (modifiedBy: string): void;


    GetDataHash (): string;
    UpdateDataHash (dataHash: string): void;


    GetSchemaHash (): string | undefined;
    UpdateSchemaHash (schemaHash: string): void;
}



export interface HistoricalMetadataServiceInterface {
    GetTimestamp (): number;
    UpdateTimestamp (timestamp: number): void;


    GetComment (): string | undefined;
    UpdateComment (comment: string): void;


    GetIsTrackingHash (): boolean;
    SetIsTrackingHAsh (flag: boolean): void;

    GetHashes (): string [];
    GetHashLatest (): string;
    AddHash (newHash: string): void;
}





export interface MetadataServiceInterface {
    GetCreatedAt (): number;
    UpdateCreatedAt (createdAt: number): void;


    GetUpdatedAt (): number;
    AutoUdatedAt? (): void;
    UpdateUpdatedAt (updatedAt: number): void;


    GetExpiresAt (): number | undefined;
    UpdateExpiresAt (expiresAt: number): void;
    RemoveExpiresAt (): void;


    GetTags (): string[];
    AddTag (tag: string): void;
    RemoveTag (tag: string): void;
    ClearTags (): void;


    GetRevisionHistory (): MetadataInterface ["RevisionHistory"];
    AddRevisionHistory (history: MetadataInterface ["RevisionHistory"] [0]): void;
    ClearRevisionHistory (): void;

    GetState(): MetadataInterface;
}
