import { AxiosResponse } from 'axios';
import { fighterjet } from 'src/jet/interfaces/jet.interface';
import { OperationResult } from './interfaces/operation_result.interface';
import { Request, Response } from 'express';
export declare class CommonService {
    hello_world_html_string: string;
    src_db_base_url: string;
    dest_db_base_url: string;
    self_base_url: string;
    success_str: string;
    fail_not_found_str: string;
    fail_internal_str: string;
    fail_badreq_str: string;
    success_code: number;
    fail_not_found_code: number;
    fail_internal_code: number;
    fail_badreq_code: number;
    jets_france_from_route(): Promise<fighterjet[]>;
    jets_china_from_db(): Promise<fighterjet[]>;
    req_headers_string(req: Request): string;
    res_headers_string(res: Response): string;
    get_from_db_id<T>(id: number): Promise<T>;
    get_from_db_id_batch<T>(ids: number[]): Promise<T[]>;
    get_from_dest_db_id_promise<T>(id: number): Promise<AxiosResponse<T>>;
    post_to_db_obj<T>(obj: T): Promise<OperationResult>;
    post_to_db_obj_batch<T>(objs: T[]): Promise<OperationResult>;
    delete_in_db(id: number): Promise<OperationResult>;
    checkout_checkin<T>(id: number): Promise<OperationResult>;
}
