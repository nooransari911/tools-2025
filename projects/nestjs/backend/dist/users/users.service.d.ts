import { User } from './interfaces/user.interface';
import { CommonService } from 'src/common/common.service';
import { OperationResult } from 'src/common/interfaces/operation_result.interface';
export declare class UsersService {
    private readonly commonservice;
    constructor(commonservice: CommonService);
    get_user_id(id: number): Promise<User>;
    get_user_batch(ids: number[]): Promise<User[]>;
    post_user_id(id: number): Promise<OperationResult>;
    post_user(user: User): Promise<OperationResult>;
    post_user_batch(user: User[]): Promise<OperationResult>;
    delete_user(id: number): Promise<OperationResult>;
    service_checkout_checkin(id: number): Promise<OperationResult>;
}
