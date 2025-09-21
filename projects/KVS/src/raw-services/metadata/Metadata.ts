import { MetadataInterface } from "../../interfaces/core/Metadata/MetadataInterface";
import { MetadataServiceInterface } from "../../interfaces/raw-services/MetadataService";



export class Metadata implements MetadataServiceInterface {
    private _version: number;
    private _modifiedBy: string | undefined;
    private _dataHash: string;
    private _schemaHash: string | undefined;


    private _createdAt: number;
    private _updatedAt: number;
    private _expiresAt: number | undefined;
    private _tags: string[];
    private _revisionHistory: MetadataInterface["RevisionHistory"];


    constructor(initialData?: Partial<MetadataInterface>) {
        const now = Date.now();
        // Base Metadata properties
        this._version = initialData?.Version ?? 0;
        this._modifiedBy = initialData?.ModifiedBy ?? undefined;
        this._dataHash = initialData?.DataHash ?? "";
        this._schemaHash = initialData?.SchemaHash ?? undefined;

        // Main Metadata properties
        this._createdAt = initialData?.CreatedAt ?? now;
        this._updatedAt = initialData?.UpdatedAt ?? now;
        this._expiresAt = initialData?.ExpiresAt;
        this._tags = initialData?.Tags ?? [];
        this._revisionHistory = initialData?.RevisionHistory ?? [];
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






    public GetCreatedAt(): number {
        return this._createdAt;
    }

    public UpdateCreatedAt(createdAt: number): void {
        this._createdAt = createdAt;
    }


    public GetUpdatedAt(): number {
        return this._updatedAt;
    }

    public UpdateUpdatedAt(updatedAt: number): void {
        this._updatedAt = updatedAt;
    }


    public GetExpiresAt(): number | undefined {
        return this._expiresAt;
    }

    public UpdateExpiresAt(expiresAt: number): void {
        this._expiresAt = expiresAt;
    }

    public RemoveExpiresAt(): void {
        this._expiresAt = undefined;
    }


    public GetTags(): string[] {
        // Return a copy to prevent external modification of the internal array
        return [...this._tags];
    }

    public AddTag(tag: string): void {
        if (!this._tags.includes(tag)) {
            this._tags.push(tag);
        }
    }

    public RemoveTag(tag: string): void {
        this._tags = this._tags.filter(t => t !== tag);
    }

    public ClearTags(): void {
        this._tags = [];
    }


    public GetRevisionHistory(): MetadataInterface["RevisionHistory"] {
        // Return a copy for encapsulation
        return [...this._revisionHistory];
    }

    public AddRevisionHistory(history: MetadataInterface["RevisionHistory"][0]): void {
        this._revisionHistory.push(history);
    }

    public ClearRevisionHistory(): void {
        this._revisionHistory = [];
    }




    public GetState(): MetadataInterface {
        return {
            Version: this._version,
            DataHash: this._dataHash,
            ModifiedBy: this._modifiedBy,
            SchemaHash: this._schemaHash,
            CreatedAt: this._createdAt,
            UpdatedAt: this._updatedAt,
            ExpiresAt: this._expiresAt,
            Tags: [...this._tags],
            RevisionHistory: [...this._revisionHistory],
        };
    }
}