import { HistoricalMetadataServiceInterface } from "../../interfaces/raw-services/MetadataService";

export class HistoricalMetadataService implements HistoricalMetadataServiceInterface {
    private _timestamp: number;
    private _comment: string | undefined;
    private _trackingHashes: boolean;
    private _hashes: string [];

    constructor (initialData: {
        timestamp?: number;
        comment?: string;
    }) {
        this._timestamp = initialData.timestamp ?? Date.now ();
        this._comment = initialData.comment ?? "";
    }

    public GetTimestamp(): number {
        return this._timestamp;
    }

    public UpdateTimestamp (timestamp: number): void {
        this._timestamp = timestamp;
    }

    public GetComment(): string | undefined {
        return this._comment;
    }

    public UpdateComment(comment: string): void {
        this._comment = comment;
    }


    public GetIsTrackingHash(): boolean {
        return this._trackingHashes;
    }

    public SetIsTrackingHAsh(flag: boolean): void {
        this._trackingHashes = flag;
    }


    public GetHashes(): string[] {
        return [...this._hashes];
    }

    public GetHashLatest(): string {
        return this._hashes [this._hashes.length - 1];
    }

    public AddHash(newHash: string): void {
        this._hashes.push (newHash);
    }
}
