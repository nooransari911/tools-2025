import { KvsKeyInterface } from "../core/Key/KvsKeyInterface";
import { KvsRecord } from "../core/Record/KvsRecord";



export interface CarinaeServiceInterface {
    Get <T> (Key: KvsKeyInterface, options?: any): Promise <ApiResponse <KvsRecord <T>>>;


    Set <T> (record: KvsRecord<T>, options?: any): Promise <ApiResponse <void>>;

    
    Delete (Key: KvsKeyInterface): Promise <ApiResponse <{ deleted: boolean }>>;


    Keys (): Promise <ApiResponse <KvsKeyInterface []>>;
}



export interface ApiResponseBase {
    status: 'success' | 'error';
    timestamp: number;
}

export interface ApiSuccessResponse <T> extends ApiResponseBase {
    status: 'success';
    data: T;
}


export interface ApiErrorResponse extends ApiResponseBase {
    status: 'error';
    error: {
        code: string;
        message: string;
        details?: any;
    };
}

export type ApiResponse <T> = ApiSuccessResponse <T> | ApiErrorResponse;