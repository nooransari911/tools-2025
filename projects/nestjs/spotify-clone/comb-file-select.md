# src/common/common.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { CommonService } from './common.service';

describe('CommonService', () => {
  let service: CommonService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [CommonService],
    }).compile();

    service = module.get<CommonService>(CommonService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});



# src/common/exceptions/jetexfilter.exception.ts
import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Logger } from "@nestjs/common";
import { Request, Response } from "express";




@Catch (HttpException)
export class JetExFilter implements ExceptionFilter {
  // public readonly logger = new Logger ('JetController')


  catch(exception: HttpException, host: ArgumentsHost) {
      const ctx = host.switchToHttp ();
      const response = ctx.getResponse<Response> ();
      const request = ctx.getRequest<Request> ();
      const status = exception.getStatus ();
      const standard_exc_body = exception.getResponse ();




      response
        .status (status)
        .json ({
          standard_exc_body,
          // path: request.url,
        })
  }

}



# src/common/exceptions/primtive_ex_filter.exception.ts
import { ArgumentsHost, BadRequestException, Catch, ExceptionFilter, HttpException, HttpStatus } from "@nestjs/common";
import { BadReqExc } from "./status.exception";
import { request, Response } from "express";

@Catch(BadRequestException)
export class ValidationExceptionFilter implements ExceptionFilter<BadRequestException> {
  public catch (exception, host: ArgumentsHost) {
    const ctx = host.switchToHttp ();
    const response = ctx.getResponse<Response> ();
    const request = ctx.getRequest<Request> ();
    const status = exception.getStatus ();
    const standard_exc_body = {
          status: HttpStatus.BAD_REQUEST,
          status_string: "Invalidation Failed;",
          timestamp: new Date ().toISOString(),
          message: "Invalidation Failed;",
          requested_resource: request.url
        }    
        
    response
      .status(status)
      .json({
        standard_exc_body,
        // path: request.url
      })
  
  }

}



@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  public catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    // Determine the status code
    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    // Determine status string and message based on the exception
    let status_string = "Internal Server Error";
    let message = "An unexpected error occurred.";

    if (exception instanceof HttpException) {
      // Attempt to extract message from HttpException response
      const httpExceptionResponse = exception.getResponse();

      if (typeof httpExceptionResponse === 'object' && httpExceptionResponse !== null && 'status_string' in httpExceptionResponse) {
        status_string = (httpExceptionResponse as { status_string: string }).status_string;
      }

      if (typeof httpExceptionResponse === 'string') {
        message = httpExceptionResponse;
      } else if (typeof httpExceptionResponse === 'object' && httpExceptionResponse !== null && 'message' in httpExceptionResponse) {
        message = (httpExceptionResponse as { message: string }).message;
      }
      
    }



    // Build the response body, closely matching your original format
    const errorResponse = {
      standard_exc_body: {
        status: status,
        status_string: status_string,
        timestamp: new Date().toISOString(),
        message: message,
        requested_resource: request.url,
      },
      // path: request.url,
    };

    // Log the error (optional but recommended)
    console.error(exception);

    // Send the response
    response.status(status).json(errorResponse);
  }
}



# src/common/exceptions/status.exception.ts
import { ArgumentsHost, HttpException, HttpStatus, Logger } from "@nestjs/common";




export class ForbExc extends HttpException {
  public readonly logger = new Logger ('JetController')

  constructor (message: string) {
    super ({
      status: HttpStatus.FORBIDDEN,
      status_string: "Forbidden Request;",
      timestamp: new Date ().toISOString(),
      message: "This is my message for a 403/forbidden status code",
      requested_resource: message
    }, HttpStatus.FORBIDDEN)

    
    this.logger.error (`Exception:: message:  ${message}`);
  }
}



export class TeaExc extends HttpException {
  public readonly logger = new Logger ('JetController')


  constructor (message: string) {
    super ({
      status: HttpStatus.I_AM_A_TEAPOT,
      status_string: "I'm a Teapot;",
      timestamp: new Date ().toISOString(),
      message: "This is my message for a 418/I'm a teapot status code",
      requested_resource: message
    }, HttpStatus.I_AM_A_TEAPOT)


    this.logger.error (`Exception:: message:  ${message}`);
  }
}



export class InternalServerExc extends HttpException {
  public readonly logger = new Logger ('JetController')


  constructor (message: string) {
    super ({
      status: HttpStatus.INTERNAL_SERVER_ERROR,
      status_string: "An internal error has occured;",
      timestamp: new Date ().toISOString(),
      message: "this is my message for a 500/An internal error has occured;",
      requested_resource: message
    }, HttpStatus.INTERNAL_SERVER_ERROR)


    this.logger.error (`Exception:: message:  ${message}`);
  }
}





export class BadReqExc extends HttpException {
  public readonly logger = new Logger ('JetController')


  constructor (message: string) {
    super ({
      status: HttpStatus.BAD_REQUEST,
      status_string: "Invalidation Failed;",
      timestamp: new Date ().toISOString(),
      message: "Invalidation Failed;",
      requested_resource: message
    }, HttpStatus.BAD_REQUEST)  


    this.logger.error (`Exception:: message:  ${message}`);
  }
}





# src/common/interfaces/operation_result.interface.ts
export class OperationResult {
  // HTTP-Style Status codes (e.g., 200, 404, 500)
  StatusCode: number;
  
  // Response message (e.g., success or error description)
  message: string;

  // Data returned in the response (optional)
  data?: any;

}



# src/common/common.controller.ts
import { Controller, Get, ParseIntPipe, Query } from '@nestjs/common';
import axios from 'axios';
import { JetExFilter } from 'src/jet/exceptions/jetexfilter.exception';
import { fighterjet } from 'src/jet/interfaces/jet.interface';
import { CommonService } from './common.service';
import { User } from 'src/users/interfaces/user.interface';
import { ParseIntArrayPipe } from './pipes/parse_int_array_pipe.pipe';




@Controller('common')
export class CommonController {
    constructor (private readonly commonservice: CommonService) {};


    @Get ('get-hello')
    function_get_hello () {
        return this.commonservice.hello_world_html_string;
    }


    @Get ('france')
    async function_get_france (): Promise <fighterjet []> {
        const response_france = await this.commonservice.jets_france_from_route ();
        return response_france;
    }


    @Get ('china')
    async function_get_china (): Promise <fighterjet []> {
        const response_china = await this.commonservice.jets_china_from_db ();
        return response_china;
    }







}



# src/common/pipes/parse_int_array_pipe.pipe.ts
import { Injectable, PipeTransform, ArgumentMetadata} from '@nestjs/common';
import { InternalServerExc } from '../exceptions/status.exception';
import { privateEncrypt } from 'node:crypto';

@Injectable()
export class ParseIntArrayPipe implements PipeTransform {
  transform(value: any, metadata: ArgumentMetadata) {
    // If the value is a string, try parsing it as a JSON array
    if (typeof value === 'string') {
      try {
        // Try to parse it as a JSON array
        value = JSON.parse(value);
        // console.log (value);
      } catch (e) {
        throw new InternalServerExc ('Invalid array format');
      }
    }

    // Check if the value is now an array
    if (!Array.isArray(value)) {
      throw new InternalServerExc ('Query parameter should be an array');
    }

    // Validate that each item in the array is a valid integer
    const parsedArray = value.map((item) => {
      const parsedValue = parseInt(item, 10);
      if (isNaN(parsedValue)) {
        throw new InternalServerExc ('All elements must be valid integers');
      }
      return parsedValue;
    });

    // console.log (`The parsed array is: ${parsedArray}`)
    return parsedArray;
  }
}



# src/common/common.module.ts
import { Module } from '@nestjs/common';
import { CommonService } from './common.service';
import { CommonController } from './common.controller';

@Module({
  providers: [CommonService],
  controllers: [CommonController]
})
export class CommonModule {}



# src/common/common.service.ts
import { Injectable } from '@nestjs/common';
import axios, { AxiosResponse } from 'axios';
import { fighterjet } from 'src/jet/interfaces/jet.interface';
import { User } from 'src/users/interfaces/user.interface';
import { InternalServerExc } from './exceptions/status.exception';
import { OperationResult } from './interfaces/operation_result.interface';





@Injectable()
export class CommonService {
    public hello_world_html_string = `
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Hello World</title>
                <style>
                    body {
                    background-color: black;
                    color: white;
                    font-family: 'Courier New', Courier, monospace;
                    }
                </style>
            </head>
            <body>
                <h1>Hello World</h1>
            </body>
        </html>
    `;

    public src_db_base_url = "http://localhost:7000";
    public dest_db_base_url = "http://localhost:8000";
    public self_base_url = "http://localhost:3000";
    public success_str            : string    = "successful";
    public fail_not_found_str     : string    = "Not Found";
    public fail_internal_str      : string    = "Internal Server Error";
    public fail_badreq_str        : string    = "Bad Request";
    public success_code           : number    = 200;
    public fail_not_found_code    : number    = 404;
    public fail_internal_code     : number    = 500;
    public fail_badreq_code       : number    = 400;



    async jets_france_from_route (): Promise <fighterjet []> {
        const response_france: AxiosResponse <fighterjet []> = await axios.get <fighterjet[]> (`${this.self_base_url}/jet/france/`);
        return response_france.data;
    }


    async jets_china_from_db (): Promise <fighterjet []> {
        const response_china_1: AxiosResponse <fighterjet> = await axios.get <fighterjet> (`${this.src_db_base_url}/1`);
        const response_china_2: AxiosResponse <fighterjet> = await axios.get <fighterjet> (`${this.src_db_base_url}/2`);



        return [
            response_china_1.data,
            response_china_2.data
        ]
    }


    async get_from_db_id <T> (id: number): Promise <T> {
        try {
            const obj_promise: Promise <AxiosResponse <T>> = axios.get <T> (`${this.src_db_base_url}/${id}`);
            const await_promise: AxiosResponse <T> = await obj_promise;
       
            return await_promise.data;
        }

    catch (error) {
        throw new InternalServerExc ("Failed to get from db");
    }

    
    }



    async get_from_db_id_batch <T> (ids: number []): Promise <T []> {
        try {
            const all_promises: Promise <AxiosResponse <T>> [] = ids.map (id =>
                axios.get <T> (`${this.src_db_base_url}/${id}`)
            );


            const await_promises: AxiosResponse <T> [] = await Promise.all (all_promises);

            const all_objs: T [] = await_promises.map (obj => obj.data);

            // console.log (`The fetched objs are: ${all_objs}`);

            return all_objs;

            
        }

        
        catch (error) {
            throw new InternalServerExc ("Error fetching the objs");
        }
    }





    async post_to_db_obj <T> (obj: T): Promise <OperationResult> {
        const a: OperationResult = {
            message: "hi",
            StatusCode: 200,
        }


        try {
            const obj_promise = await axios.post (`${this.dest_db_base_url}/checkout`, obj);

            return {
                message: this.success_str,
                StatusCode: this.success_code
            }
        }
        
        catch (error) {
            throw new InternalServerExc ("Failed to create/update object");
        }


    }


    async post_to_db_obj_batch <T> (objs: T []): Promise <OperationResult> {
        try {
            const all_promises: Promise <AxiosResponse <T>> [] = objs.map (obj =>
                axios.post <T> (`${this.dest_db_base_url}/checkout`, obj)
            );

            const await_promises: AxiosResponse <T> [] = await Promise.all (all_promises);

            const opress: OperationResult = {
                message: this.success_str,
                StatusCode: this.success_code
            }

            return opress
        }


        catch (error) {
            throw new InternalServerExc ("Failed to add users batch");
        }
        
    }

    








  
    async delete_in_db (id: number): Promise <OperationResult> {
        try {
            const promise = await axios.delete (`${this.dest_db_base_url}/checkout/${id}`);


            return {
                message: this.success_str,
                StatusCode: this.success_code
                
            }
        }



        catch (error) {
            // console.log (error);
            throw new InternalServerExc ("Failed to delete");
        }
    }
        
        
        

}



# src/common/common.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { CommonController } from './common.controller';

describe('CommonController', () => {
  let controller: CommonController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [CommonController],
    }).compile();

    controller = module.get<CommonController>(CommonController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});



# src/users/users.service.ts
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


}



# src/users/interfaces/user.interface.ts
export class User {
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    username: string;
    phone: string;
    field_0: string;
    field_1: string;
    field_2: string;
    field_3: string;



/*
    constructor(
        id: number,
        first_name: string,
        last_name: string,
        email: string,
        username: string,
        phone: string,
        field_0: string,
        field_1: string,
        field_2: string,
        field_3: string
    ) {
        this.id = id;
        this.first_name = first_name;
        this.last_name = last_name;
        this.email = email;
        this.username = username;
        this.phone = phone;
        this.field_0 = field_0;
        this.field_1 = field_1;
        this.field_2 = field_2;
        this.field_3 = field_3;
    }

*/


}










# src/users/users.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UsersService } from './users.service';

describe('UsersService', () => {
  let service: UsersService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [UsersService],
    }).compile();

    service = module.get<UsersService>(UsersService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});



# src/users/users.controller.ts
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
        const hit_post_promise: Promise <OperationResult> = this.userservice.delete_user (id);
        const await_promise: OperationResult = await hit_post_promise;
        return await_promise;
    }




    

}



# src/users/users.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { UsersController } from './users.controller';

describe('UsersController', () => {
  let controller: UsersController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UsersController],
    }).compile();

    controller = module.get<UsersController>(UsersController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});



# src/users/users.module.ts
import { Module } from '@nestjs/common';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { CommonService } from 'src/common/common.service';

@Module({
  controllers: [UsersController],
  providers: [UsersService, CommonService]
})
export class UsersModule {}



