import { BaseMetadataInterface } from "./BaseMetadataInterface";

export interface HistoricalMetadataInterface extends BaseMetadataInterface {
  Timestamp: number;
  Comment?: string;

  TrackingHash?: boolean,
  Hashes?: string [];
}