import { BaseMetadataInterface } from "../../interfaces/core/Metadata/BaseMetadataInterface";
import { BaseMetadataServiceInterface } from "../../interfaces/raw-services/MetadataService";

export class BaseMetadata implements BaseMetadataServiceInterface {
    private _version: number;
    private _modifiedBy: string | undefined;
    private _dataHash: string;
    private _schemaHash: string | undefined;

    constructor (initialData: Partial <BaseMetadataInterface>) {
        this._dataHash = initialData?.DataHash ?? "";
        this._version = initialData?.Version ?? 0;
        this._modifiedBy = initialData?.ModifiedBy ?? undefined;
        this._schemaHash = initialData?.SchemaHash ?? undefined;
    }

    public GetVersion(): number {
        return this._version;
    }

    public IncrementVersion(): number {
        this._version++;
        return this._version;
    }

    public DecrementVersion(): number {
        this._version--;
        return this._version;
    }


    public GetModifiedBy(): string | undefined {
        return this._modifiedBy;
    }

    public UpdateModifiedBy(modifiedBy: string): void {
        this._modifiedBy = modifiedBy;
    }


    public GetDataHash(): string {
        return this._dataHash;
    }

    public UpdateDataHash(dataHash: string): void {
        this._dataHash = dataHash;
    }


    public GetSchemaHash(): string | undefined {
        return this._schemaHash;
    }

    public UpdateSchemaHash(schemaHash: string): void {
        this._schemaHash = schemaHash;
    }
}
