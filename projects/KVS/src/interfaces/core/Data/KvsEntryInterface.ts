import { MetadataInterface } from "../Metadata/MetadataInterface";



export interface KvsEntryInterface <T = any> {
  Value: T;
  Metadata:MetadataInterface;
}
