import { AppService } from './app.service';
import { Request } from 'express';
import { ParsedQs } from 'qs';
interface RequestResponse {
    body?: any;
    headers: Record<string, string | string[] | undefined>;
    query: ParsedQs;
    params: Record<string, string>;
}
export declare class AppController {
    private readonly appService;
    constructor(appService: AppService);
    getCat(req: Request, params: any): RequestResponse;
    getHello(): string;
}
export {};
