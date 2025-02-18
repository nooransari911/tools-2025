import { Injectable } from '@nestjs/common';
import { User } from './interfaces/user.interface';
import { CommonService } from 'src/common/common.service';
import { OperationResult } from 'src/common/interfaces/operation_result.interface';

@Injectable()
export class UsersService {
    constructor (private readonly commonservice: CommonService) {}

    
    async get_user_id (id: number): Promise<User> {
        return this.commonservice.get_from_db_id <User> (id);
    }


    async get_user_batch (ids: number []): Promise <User []> {
        return this.commonservice.get_from_db_id_batch <User> (ids);
    }



    async post_user_id (id: number): Promise <OperationResult> {
        const user: User = await this.commonservice.get_from_db_id <User> (id);
        const opres: OperationResult = await this.commonservice.post_to_db_obj <User> (user);
        return opres;
    }



    async post_user (user: User): Promise <OperationResult> {
        const opres: OperationResult = await this.commonservice.post_to_db_obj <User> (user);
        return opres;
    }



    async post_user_batch (user: User []): Promise <OperationResult> {
        const opres: OperationResult = await this.commonservice.post_to_db_obj_batch <User> (user);
        return opres;
    }



    async delete_user (id: number): Promise <OperationResult> {
        const opres: OperationResult = await this.commonservice.delete_in_db (id);
        return opres;
    }




    async service_checkout_checkin (id: number): Promise <OperationResult> {
        return await this.commonservice.checkout_checkin (id);
    }





}
