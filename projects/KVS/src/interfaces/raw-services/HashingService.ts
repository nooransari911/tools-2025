export interface HashingServiceInterface {
    Hash(data: any): Promise<string>;
    Verify(data: any, hash: string): Promise<boolean>;
}