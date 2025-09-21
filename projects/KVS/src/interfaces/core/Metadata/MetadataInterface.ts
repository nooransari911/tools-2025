import { BaseMetadataInterface } from "./BaseMetadataInterface";
import { HistoricalMetadataInterface } from "./HistoricalMetadataInterface";


export interface MetadataInterface extends BaseMetadataInterface {
    CreatedAt: number;
    UpdatedAt: number;
    ExpiresAt?: number | undefined;
    Tags: string[];
    RevisionHistory: HistoricalMetadataInterface[];
}
