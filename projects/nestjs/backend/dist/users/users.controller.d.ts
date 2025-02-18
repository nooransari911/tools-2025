import { User } from './interfaces/user.interface';
import { UsersService } from './users.service';
import { OperationResult } from 'src/common/interfaces/operation_result.interface';
export declare class UsersController {
    private readonly userservice;
    constructor(userservice: UsersService);
    function_get_user(id: number): Promise<User>;
    function_get_user_batch(ids: number[]): Promise<User[]>;
    function_user_post_id(id: number): Promise<OperationResult>;
    function_user_post_body(body: User): Promise<OperationResult>;
    function_user_post_body_batch(body: User[]): Promise<OperationResult>;
    function_user_delete(id: number): Promise<OperationResult>;
    route_check(id: number): Promise<OperationResult>;
}
