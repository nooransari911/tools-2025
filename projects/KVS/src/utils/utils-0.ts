import { ApiErrorResponse, ApiSuccessResponse } from "../interfaces/public-services/CarinaeInterface";

const createSuccess = <T>(data: T): ApiSuccessResponse<T> => ({
    status: 'success',
    timestamp: Date.now(),
    data: data,
});

const createError = (code: string, message: string, details?: any): ApiErrorResponse => ({
    status: 'error',
    timestamp: Date.now(),
    error: { code, message, details },
});



export { createError, createSuccess }