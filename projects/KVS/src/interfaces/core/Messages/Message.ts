export interface MessageInterface {
    Type: string;
    Key: string;
    // Value: object | null;
    Value: any;
    Timestamp: number;
}

export interface ResponseInterface {
    Success: boolean;
    Found?: boolean;
    Value: object | null;
    Error: string | null;
}