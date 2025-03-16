import { Body, Controller, Delete, Get, ParseIntPipe, Post, Query } from '@nestjs/common';
import { ParseIntArrayPipe } from 'src/common/pipes/parse_int_array_pipe.pipe';
import { User } from './interfaces/user.interface';
import { UsersService } from './users.service';
import { OperationResult } from 'src/common/interfaces/operation_result.interface';

@Controller('users')
export class UsersController {
    constructor (private readonly userservice: UsersService) {}




    
    @Get ('user')
    async function_get_user (
        @Query ('id', ParseIntPipe) id: number
    ): Promise <User> {
        const response_user = await this.userservice.get_user_id (id);
        return response_user;
    }



    

    @Get ('user-batch')
    async function_get_user_batch (
         @Query ('ids', ParseIntArrayPipe) ids: number []
    ): Promise <User []> {
        const response_user_batch = await this.userservice.get_user_batch (ids);
        return response_user_batch;
    }

    

    @Get ('post-user')
    async function_user_post_id (
        @Query ('id', ParseIntPipe) id: number
    ): Promise <OperationResult>  {
        const hit_post_promise: Promise <OperationResult> = this.userservice.post_user_id (id);

        const await_promise: OperationResult = await hit_post_promise;

        return await_promise;
    }



    @Post ('post-user')
    async function_user_post_body (
        @Body () body: User
    ): Promise <OperationResult> {
        const hit_post_promise: Promise <OperationResult> = this.userservice.post_user (body);
        const await_promise: OperationResult = await hit_post_promise;
        return await_promise;
    }



    @Post ('post-user-batch')
    async function_user_post_body_batch (
        @Body () body: User []
    ): Promise <OperationResult> {
        const hit_post_promise: Promise <OperationResult> = this.userservice.post_user_batch (body);
        const await_promise: OperationResult = await hit_post_promise;
        return await_promise;
    }




    @Delete ('delete-user')
    async function_user_delete (
        @Query ('id', ParseIntPipe) id: number
    ): Promise <OperationResult> {
        return await this.userservice.delete_user (id);
    }






    @Get ('check')
    async route_check (
        @Query ('id', ParseIntPipe) id: number
    ) {
        return this.userservice.service_checkout_checkin (id);
    }
    

}
