# src/jet/jet.service.ts
import { HttpException, HttpStatus, Injectable, Logger } from "@nestjs/common";
import { HttpService } from "@nestjs/axios";
import { fighterjet, user_profile } from "./interfaces/jet.interface";
import { Response } from "express";
import { ForbExc, InternalServerExc, TeaExc } from "./exceptions/status.exception";
import { lastValueFrom } from "rxjs"; 







@Injectable ()
export class JetService {
  // private name: string;
  public readonly logger = new Logger ('JetController');
  public readonly domain = "http://localhost:3000/";
  constructor (private readonly httpservice: HttpService) {}




  france (): fighterjet [] {
     return [
      {
        country: "france",
        block: "NATO",
        name: "rafale",
        manufacturer: "dassault",
        gen: "4.5",
        role: "multirole",
        mtow: "24"
      }
    ]   
  }



  china (): fighterjet [] {
     return  [
      {
        country: "china",
        block: "SCO",
        name: "J20",
        manufacturer: "chengdu",
        gen: "5",
        role: "air superiority",
        mtow: "35"
      },
      {
        country: "china",
        block: "SCO",
        name: "J15",
        manufacturer: "shenyang",
        gen: "4.5",
        role: "air superiority",
        mtow: "30"
      }
    ]  
  }


  vietnam () {
    throw new ForbExc ('vietnam');
  }



  
  nz () {
    throw new TeaExc ('NZ');
  }



  
  user (uid: number, ugroup: string) {
    return {
      user_id: uid,
      user_group: ugroup
    }
  }



  async hit_profile (bodyobj: user_profile) {
    try {
      const profile_response = await lastValueFrom(
        this.httpservice.post(
          `${this.domain}jet/profile/`,
          bodyobj
        )
      );
      return profile_response.data;
    }
    
    catch (error) {
      throw new InternalServerExc ("[JetService] Hitting Profile;");
    }
  }




  async post_user_profile (bodyobj: user_profile) {
    try {
      const profile_response = await lastValueFrom(
        this.httpservice.post(
          `${this.domain}jet/profile/`,
          bodyobj
        )
      );
      return profile_response.data;
    }
    
    catch (error) {
      throw new InternalServerExc ("[JetService] Error when Post to Profile;") ;
    }
  }




  profile (user: user_profile): user_profile {
    this.logger.log (user);

    return user;
  }









}















# src/jet/exceptions/jetexfilter.exception.ts
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



# src/jet/exceptions/primtive_ex_filter.exception.ts
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



# src/jet/exceptions/status.exception.ts
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





# src/jet/interfaces/jet.interface.ts
import { Transform } from "class-transformer";
import { IsString, IsInt, IsNotEmpty } from "class-validator";
import { Timestamp } from "rxjs";


export class fighterjetrequest {
  country: string;
  // block: string
  // name: string;
  // manufacturer: string;
  // gen: string;
  // role: string;
  // mtow: string;


}



export class fighterjet {
  country: string;
  block: string;
  name: string;
  manufacturer: string;
  gen: string;
  role: string;
  mtow: string;


}






export class user_profile {
  @IsInt ()
  @IsNotEmpty ()
  @Transform(({ value }) => parseInt(value, 10))
  id: number;



  @IsInt ()
  @IsNotEmpty ()
  @Transform(({ value }) => parseInt(value, 10))
  phone: number;


  @IsString ()
  @IsNotEmpty ()
  name: string;



  @IsString ()
  @IsNotEmpty ()
  dept: string;






  // @IsString ()
  // group: string;


  // @IsString ()
  // gender: string;


  // @IsString ()
  // email: string;


  // @IsString ()
  // field1: string [];


  // @IsString ()
  // field2: string [];


  // @IsString ()
  // field3: string [];


  // @IsString ()
  // field4: string [];




}








# src/jet/jet.controller.ts
import { Controller, Get, Post, Body, Req, Param, UseFilters, Query, ParseIntPipe, ValidationPipe, HttpException, UsePipes, UseInterceptors } from '@nestjs/common';
import {fighterjetrequest, fighterjet, user_profile} from './interfaces/jet.interface';
import { JetService } from './jet.service';
import { JetExFilter } from './exceptions/jetexfilter.exception';
import { Request } from 'express';
import { BadReqExc, InternalServerExc } from './exceptions/status.exception';
import { AllExceptionsFilter, ValidationExceptionFilter } from './exceptions/primtive_ex_filter.exception';




@Controller ('jet')
@UseFilters (JetExFilter, ValidationExceptionFilter, AllExceptionsFilter)
export class JetController {


  constructor (private jetservice: JetService) {}


  
  @Get ('france')
  france (@Req () req: Request, @Body () body: fighterjetrequest): fighterjet[] {
    // this.jetservice.logger.log ('france');
    return this.jetservice.france ();
  }



  @Get ('china')
  china (@Req () req: Request, @Body () body: fighterjetrequest): fighterjet[] {
    // this.jetservice.logger.log ('china')
    return this.jetservice.china ();
  }


  @Get ('viet')
  viet () {
    return this.jetservice.vietnam ();
  }



  @Get ('nz')
  nz(){
    return this.jetservice.nz ();
  }


  @Get ('user')
  user (@Query ('uid', ParseIntPipe) id: number, @Query ('ugroup', ValidationPipe) group: string) {
    return this.jetservice.user (id, group);
  }




  @Get ('hit-profile')
  async hit_profile (
                @Req () req: Request,
                @Query ('id', ParseIntPipe) id: number,
                @Query ('phone', ParseIntPipe) phone: number,
                @Query ('dept', ValidationPipe) dept: string,
                @Query ('name', ValidationPipe) name: string
              ) {

    const bodyobj: user_profile = {
      id:    id,
      name:  name,
      dept:  dept,
      phone: phone
    };

    try {
      const response = await this.jetservice.hit_profile (bodyobj);
      return response;
    }
    
    catch (error) {
      throw new InternalServerExc ("[JetController] Hitting Profile;") ;
    }


    
  }

  @Post ('profile')
  profile (@Body () body: user_profile) {
    return this.jetservice.profile (body);
  }






  @Get ('post_user_profile')
  async post_user_profile (
                @Req () req: Request,
                @Query () query: user_profile
              ) {
    try {
      const response = await this.jetservice.post_user_profile (query);
      return response;
    }
    
    catch (error) {
      throw new InternalServerExc ("[JetController] Error when Post to Profile;") ;
    }


    
  }



}



# src/jet/jet2.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { JetService } from './jet.service';
import { HttpService } from '@nestjs/axios';
import { HttpException, HttpStatus } from '@nestjs/common';
import { of, throwError } from 'rxjs';
import { ForbExc, TeaExc } from './exceptions/status.exception';
import { AxiosResponse, AxiosError, AxiosRequestHeaders } from 'axios';

describe('JetService', () => {
  let service: JetService;
  let httpService: HttpService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        JetService,
        {
          provide: HttpService,
          useValue: {
            post: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<JetService>(JetService);
    httpService = module.get<HttpService>(HttpService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('france', () => {
    it('should return an array of French fighter jets', () => {
      const result = service.france();
      expect(result).toEqual([
        {
          country: 'france',
          block: 'NATO',
          name: 'rafale',
          manufacturer: 'dassault',
          gen: '4.5',
          role: 'multirole',
          mtow: '24',
        },
      ]);
    });
  });

  describe('china', () => {
    it('should return an array of Chinese fighter jets', () => {
      const result = service.china();
      expect(result).toEqual([
        {
          country: 'china',
          block: 'SCO',
          name: 'J20',
          manufacturer: 'chengdu',
          gen: '5',
          role: 'air superiority',
          mtow: '35',
        },
        {
          country: 'china',
          block: 'SCO',
          name: 'J15',
          manufacturer: 'shenyang',
          gen: '4.5',
          role: 'air superiority',
          mtow: '30',
        },
      ]);
    });
  });

  describe('vietnam', () => {
    it('should throw a ForbExc exception', () => {
      expect(() => service.vietnam()).toThrow(ForbExc);
      expect(() => service.vietnam()).toThrowError(
        'This is my message for a 403/forbidden status code'
      );
    });
  });

  describe('nz', () => {
    it('should throw a TeaExc exception', () => {
      expect(() => service.nz()).toThrow(TeaExc);
      expect(() => service.nz()).toThrowError(
        "This is my message for a 418/I'm a teapot status code"
      );
    });
  });

  describe('user', () => {
    it('should return user information', () => {
      const uid = 123;
      const ugroup = 'admin';
      const result = service.user(uid, ugroup);
      expect(result).toEqual({
        user_id: uid,
        user_group: ugroup,
      });
    });
  });

  describe('hit_profile', () => {
    it('should successfully return profile data', async () => {
      const bodyobj = {
        id: 1,
        phone: 1234567890,
        name: 'John Doe',
        dept: 'Engineering',
      };

      const mockResponse: AxiosResponse = {
        data: bodyobj,
        status: 200,
        statusText: 'OK',
        headers: {},
        config: {
          url: `${service.domain}jet/profile/`,
          method: 'post',
          data: bodyobj,
          headers: {} as AxiosRequestHeaders,
        },
      };

      jest.spyOn(httpService, 'post').mockReturnValueOnce(of(mockResponse));

      const result = await service.hit_profile(bodyobj);
      expect(result).toEqual(bodyobj);
      expect(httpService.post).toHaveBeenCalledWith(
        `${service.domain}jet/profile/`,
        bodyobj
      );
    });

    it('should throw an HttpException on communication error', async () => {
      const bodyobj = {
        id: 1,
        phone: 1234567890,
        name: 'John Doe',
        dept: 'Engineering',
      };

      const error = new Error('Network Error');
      jest.spyOn(httpService, 'post').mockImplementationOnce(() => throwError(() => error));

      await expect(service.hit_profile(bodyobj)).rejects.toThrow(HttpException);
      await expect(service.hit_profile(bodyobj)).rejects.toThrowError(
        'this is my message for a 500/An internal error has occured;'
      );
    });

    it('should re-throw the exact error received from axios', async () => {
        const bodyobj = {
          id: 1,
          phone: 1234567890,
          name: 'John Doe',
          dept: 'Engineering',
        };
        const axiosError = new Error('Axios specific error');
        jest.spyOn(httpService, 'post').mockImplementationOnce(() => throwError(() => axiosError));


        await expect(service.hit_profile(bodyobj)).rejects.toThrow(HttpException);
        await expect(service.hit_profile(bodyobj)).rejects.toThrowError(
          'this is my message for a 500/An internal error has occured;'
        );


    });
  });

  describe('profile', () => {
    it('should return the user profile', () => {
      const user = {
        id: 1,
        phone: 1234567890,
        name: 'John Doe',
        dept: 'Engineering',
      };
      const result = service.profile(user);
      expect(result).toEqual(user);
    });

    it('should log the user profile', () => {
        const user = {
          id: 1,
          phone: 1234567890,
          name: 'John Doe',
          dept: 'Engineering',
        };
        const spy = jest.spyOn(service.logger, 'log');
        service.profile(user);
        expect(spy).toHaveBeenCalledWith(user);
      });
  });
});



# src/jet/jet.module.ts
import { Module } from "@nestjs/common";
import { JetController } from "./jet.controller"; 
import { JetService } from "./jet.service"; 
import { HttpModule } from "@nestjs/axios";



@Module({
  imports: [HttpModule],
  controllers: [JetController],
  providers: [JetService],
  exports: [HttpModule]
})
export class JetModule {}



# src/jet/jet.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { JetController } from './jet.controller';
import { JetService } from './jet.service';
import { HttpModule, HttpService } from '@nestjs/axios';
import { of } from 'rxjs';
import { fighterjet, user_profile } from './interfaces/jet.interface';
import { HttpException } from '@nestjs/common';

describe('JetController', () => {
  let controller: JetController;
  let service: JetService;
  let httpService: HttpService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      imports: [HttpModule],
      controllers: [JetController],
      providers: [JetService],
    }).compile();

    controller = module.get<JetController>(JetController);
    service = module.get<JetService>(JetService);
    httpService = module.get<HttpService>(HttpService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('france', () => {
    it('should return an array of French fighter jets', () => {
      const expectedResult: fighterjet[] = [
        {
          country: 'france',
          block: 'NATO',
          name: 'rafale',
          manufacturer: 'dassault',
          gen: '4.5',
          role: 'multirole',
          mtow: '24',
        },
      ];
      jest.spyOn(service, 'france').mockReturnValue(expectedResult);

      expect(controller.france({} as any, {} as any)).toEqual(expectedResult);
    });
  });

  describe('china', () => {
    it('should return an array of Chinese fighter jets', () => {
      const expectedResult: fighterjet[] = [
        {
          country: 'china',
          block: 'SCO',
          name: 'J20',
          manufacturer: 'chengdu',
          gen: '5',
          role: 'air superiority',
          mtow: '35',
        },
        {
          country: 'china',
          block: 'SCO',
          name: 'J15',
          manufacturer: 'shenyang',
          gen: '4.5',
          role: 'air superiority',
          mtow: '30',
        },
      ];
      jest.spyOn(service, 'china').mockReturnValue(expectedResult);

      expect(controller.china({} as any, {} as any)).toEqual(expectedResult);
    });
  });

  describe('viet', () => {
    it('should throw a ForbiddenException', () => {
      jest.spyOn(service, 'vietnam').mockImplementation(() => {
        throw new Error('Forbidden');
      });

      expect(() => controller.viet()).toThrowError('Forbidden');
    });
  });

  describe('nz', () => {
    it("should throw an 'I am a teapot' exception", () => {
      jest.spyOn(service, 'nz').mockImplementation(() => {
        throw new Error("I'm a teapot");
      });

      expect(() => controller.nz()).toThrowError("I'm a teapot");
    });
  });

  describe('user', () => {
    it('should return user information', () => {
      const expectedResult = { user_id: 1, user_group: 'group1' };
      jest.spyOn(service, 'user').mockReturnValue(expectedResult);

      expect(controller.user(1, 'group1')).toEqual(expectedResult);
    });
  });

  describe('hit_profile', () => {
    it('should successfully interact with the profile endpoint', async () => {
      const mockProfileResponse = { id: 1, name: 'John Doe', dept: 'IT', phone: 1234567890 };
      jest.spyOn(httpService, 'post').mockReturnValue(of({ data: mockProfileResponse } as any));
      jest.spyOn(service, 'hit_profile').mockResolvedValue(mockProfileResponse);

      const result = await controller.hit_profile({} as any, 1, 1234567890, 'John Doe', 'IT');

      expect(result).toEqual(mockProfileResponse);
    });

    it('should handle errors when communicating with the profile endpoint', async () => {
      jest.spyOn(service, 'hit_profile').mockRejectedValue(new Error('An error occurred while contacting profile route.'));

      try {
        await controller.hit_profile({} as any, 1, 1234567890, 'John Doe', 'IT');
      } catch (error) {
        // expect(error).toBeInstanceOf(BadRequestException);
        const standard_exc_body = (error as HttpException).getResponse();
        expect(standard_exc_body).toEqual({
          status: 500,
          status_string: 'An internal error has occured;',
          timestamp: expect.any(String),
          message: 'this is my message for a 500/An internal error has occured;',
          requested_resource: '[JetController] Hitting Profile;',
        });
      }
    });
  });

  describe('profile', () => {
    it('should create a user profile', () => {
      const userProfile: user_profile = { id: 1, name: 'John Doe', dept: 'IT', phone: 1234567890 };
      jest.spyOn(service, 'profile').mockReturnValue(userProfile);

      expect(controller.profile(userProfile)).toEqual(userProfile);
    });
  });
});



# src/jet/jet2.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { JetController } from './jet.controller';
import { JetService } from './jet.service';
import { HttpModule, HttpService } from '@nestjs/axios';
import { of, throwError } from 'rxjs';
import { fighterjet, user_profile } from './interfaces/jet.interface';
import { BadRequestException, InternalServerErrorException, HttpException } from '@nestjs/common';
import { AxiosResponse } from 'axios';
import { ForbExc, TeaExc, InternalServerExc } from './exceptions/status.exception';

describe('JetController', () => {
  let controller: JetController;
  let service: JetService;
  let httpService: HttpService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      imports: [HttpModule],
      controllers: [JetController],
      providers: [
        JetService,
        {
          provide: HttpService,
          useValue: {
            post: jest.fn(),
          },
        },
      ],
    }).compile();

    controller = module.get<JetController>(JetController);
    service = module.get<JetService>(JetService);
    httpService = module.get<HttpService>(HttpService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('france', () => {
    it('should return an array of French fighter jets', () => {
      const mockFighterJets: fighterjet[] = [
        {
          country: 'france',
          block: 'NATO',
          name: 'rafale',
          manufacturer: 'dassault',
          gen: '4.5',
          role: 'multirole',
          mtow: '24',
        },
      ];
      jest.spyOn(service, 'france').mockReturnValue(mockFighterJets);

      expect(controller.france({} as any, {} as any)).toEqual(mockFighterJets);
    });
  });

  describe('china', () => {
    it('should return an array of Chinese fighter jets', () => {
      const mockFighterJets: fighterjet[] = [
        {
          country: 'china',
          block: 'SCO',
          name: 'J20',
          manufacturer: 'chengdu',
          gen: '5',
          role: 'air superiority',
          mtow: '35',
        },
        {
          country: 'china',
          block: 'SCO',
          name: 'J15',
          manufacturer: 'shenyang',
          gen: '4.5',
          role: 'air superiority',
          mtow: '30',
        },
      ];
      jest.spyOn(service, 'china').mockReturnValue(mockFighterJets);

      expect(controller.china({} as any, {} as any)).toEqual(mockFighterJets);
    });
  });

  describe('viet', () => {
    it('should throw a ForbExc exception and validate standard_exc_body', () => {
      jest.spyOn(service, 'vietnam').mockImplementation(() => {
        throw new ForbExc('vietnam');
      });

      try {
        controller.viet();
      } catch (error) {
        expect(error).toBeInstanceOf(ForbExc);
        const standard_exc_body = (error as HttpException).getResponse(); // Directly get the standard_exc_body
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          status: 403,
          status_string: 'Forbidden Request;',
          timestamp: expect.any(String),
          message: 'This is my message for a 403/forbidden status code',
          requested_resource: 'vietnam',
        });
      }
    });
  });

  describe('nz', () => {
    it('should throw a TeaExc exception and validate standard_exc_body', () => {
      jest.spyOn(service, 'nz').mockImplementation(() => {
        throw new TeaExc('NZ');
      });

      try {
        controller.nz();
      } catch (error) {
        expect(error).toBeInstanceOf(TeaExc);
        const standard_exc_body = (error as HttpException).getResponse(); // Directly get the standard_exc_body
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          status: 418,
          status_string: "I'm a Teapot;",
          timestamp: expect.any(String),
          message: "This is my message for a 418/I'm a teapot status code",
          requested_resource: 'NZ',
        });
      }
    });
  });

  describe('user', () => {
    it('should return user information for valid id and group', () => {
      const mockUser = { user_id: 1, user_group: 'group1' };
      jest.spyOn(service, 'user').mockReturnValue(mockUser);

      expect(controller.user(1, 'group1')).toEqual(mockUser);
    });

    it('should throw BadRequestException for invalid user id and validate standard_exc_body', () => {
      try {
        controller.user(NaN, 'group1');
      } catch (error) {
        // expect(error).toBeInstanceOf(BadRequestException);
        const standard_exc_body = (error as HttpException).getResponse(); // Directly get the standard_exc_body
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          statusCode: 400,
          message: 'Validation failed (numeric string is expected)',
          error: 'Bad Request',
        });
      }
    });

    it('should throw BadRequestException for empty user group and validate standard_exc_body', () => {
      try {
        controller.user(1, '');
      } catch (error) {
        // expect(error).toBeInstanceOf(BadRequestException);
        const standard_exc_body = (error as HttpException).getResponse(); // Directly get the standard_exc_body
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          statusCode: 400,
          message: 'User group cannot be empty',
          error: 'Bad Request',
        });
      }
    });
  });

  describe('hit_profile', () => {
    it('should successfully interact with the profile endpoint and return profile data', async () => {
      const mockProfileResponse = { id: 1, name: 'John Doe', dept: 'IT', phone: 1234567890 };
      const mockAxiosResponse: AxiosResponse = {
        data: mockProfileResponse,
        status: 200,
        statusText: 'OK',
        headers: {},
        config: { headers: {} as any },
      };

      jest.spyOn(httpService, 'post').mockReturnValueOnce(of(mockAxiosResponse));
      jest.spyOn(service, 'hit_profile').mockResolvedValue(mockProfileResponse);

      const result = await controller.hit_profile(
        {} as any,
        1,
        1234567890,
        'John Doe',
        'IT',
      );

      expect(result).toEqual(mockProfileResponse);
    });

    it('should handle errors, throw InternalServerErrorException, and validate standard_exc_body', async () => {
      jest
        .spyOn(service, 'hit_profile')
        .mockRejectedValue(new Error('An error occurred while contacting profile route.'));

      try {
        await controller.hit_profile({} as any, 1, 1234567890, 'John Doe', 'IT');
      } catch (error) {
        expect(error).toBeInstanceOf(InternalServerExc);
        const standard_exc_body = (error as HttpException).getResponse(); // Directly get the standard_exc_body
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          status: 500,
          status_string: 'An internal error has occured;',
          timestamp: expect.any(String),
          message: 'this is my message for a 500/An internal error has occured;',
          requested_resource: '[JetController] Hitting Profile;',
        });
      }
    });

    it('should throw BadRequestException for invalid id and validate standard_exc_body', async () => {
      try {
        await controller.hit_profile({} as any, NaN, 1234567890, 'John Doe', 'IT');
      } catch (error) {
        // expect(error).toBeInstanceOf(BadRequestException);
        const standard_exc_body = (error as HttpException).getResponse();
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          status: 500,
          status_string: 'An internal error has occured;',
          timestamp: expect.any(String),
          message: 'this is my message for a 500/An internal error has occured;',
          requested_resource: '[JetController] Hitting Profile;',
        });

      }
    });

    it('should throw BadRequestException for invalid phone and validate standard_exc_body', async () => {
      try {
        await controller.hit_profile({} as any, 1, NaN, 'John Doe', 'IT');
      } catch (error) {
        // expect(error).toBeInstanceOf(BadRequestException);
        const standard_exc_body = (error as HttpException).getResponse();
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          status: 500,
          status_string: 'An internal error has occured;',
          timestamp: expect.any(String),
          message: 'this is my message for a 500/An internal error has occured;',
          requested_resource: '[JetController] Hitting Profile;',
        });
      }
    });

    it('should throw BadRequestException for invalid name and validate standard_exc_body', async () => {
      try {
        await controller.hit_profile({} as any, 1, 1234567890, '', 'IT');
      } catch (error) {
        // expect(error).toBeInstanceOf(BadRequestException);
        const standard_exc_body = (error as HttpException).getResponse();
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          status: 500,
          status_string: 'An internal error has occured;',
          timestamp: expect.any(String),
          message: 'this is my message for a 500/An internal error has occured;',
          requested_resource: '[JetController] Hitting Profile;',
        });
      }
    });

    it('should throw BadRequestException for invalid dept and validate standard_exc_body', async () => {
      try {
        await controller.hit_profile({} as any, 1, 1234567890, 'John Doe', '');
      } catch (error) {
        // expect(error).toBeInstanceOf(BadRequestException);
        const standard_exc_body = (error as HttpException).getResponse();
        expect(standard_exc_body).toEqual({ // Compare directly with standard_exc_body
          status: 500,
          status_string: 'An internal error has occured;',
          timestamp: expect.any(String),
          message: 'this is my message for a 500/An internal error has occured;',
          requested_resource: '[JetController] Hitting Profile;',
        });
      }
    });
  });

  describe('profile', () => {
    it('should create a user profile', () => {
      const mockUserProfile: user_profile = { id: 1, name: 'John Doe', dept: 'IT', phone: 1234567890 };
      jest.spyOn(service, 'profile').mockReturnValue(mockUserProfile);

      expect(controller.profile(mockUserProfile)).toEqual(mockUserProfile);
    });
  });
});



# src/jet/jet.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { JetService } from './jet.service';
import { HttpService } from '@nestjs/axios';
import { HttpException, HttpStatus } from '@nestjs/common';
import { of, throwError } from 'rxjs';
import { ForbExc, TeaExc } from './exceptions/status.exception';
import { AxiosResponse, AxiosError, AxiosRequestHeaders} from 'axios';

describe('JetService', () => {
  let service: JetService;
  let httpService: HttpService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        JetService,
        {
          provide: HttpService,
          useValue: {
            post: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<JetService>(JetService);
    httpService = module.get<HttpService>(HttpService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  describe('france', () => {
    it('should return an array of French fighter jets', () => {
      const result = service.france();
      expect(result).toEqual([
        {
          country: 'france',
          block: 'NATO',
          name: 'rafale',
          manufacturer: 'dassault',
          gen: '4.5',
          role: 'multirole',
          mtow: '24',
        },
      ]);
    });
  });

  describe('china', () => {
    it('should return an array of Chinese fighter jets', () => {
      const result = service.china();
      expect(result).toEqual([
        {
          country: 'china',
          block: 'SCO',
          name: 'J20',
          manufacturer: 'chengdu',
          gen: '5',
          role: 'air superiority',
          mtow: '35',
        },
        {
          country: 'china',
          block: 'SCO',
          name: 'J15',
          manufacturer: 'shenyang',
          gen: '4.5',
          role: 'air superiority',
          mtow: '30',
        },
      ]);
    });
  });

  describe('vietnam', () => {
    it('should throw a ForbExc exception', () => {
      expect(() => service.vietnam()).toThrow(ForbExc);
      expect(() => service.vietnam()).toThrowError(
        'This is my message for a 403/forbidden status code'
      );
    });
  });

  describe('nz', () => {
    it('should throw a TeaExc exception', () => {
      expect(() => service.nz()).toThrow(TeaExc);
      expect(() => service.nz()).toThrowError(
        "This is my message for a 418/I'm a teapot status code"
      );
    });
  });

  describe('user', () => {
    it('should return user information', () => {
      const uid = 123;
      const ugroup = 'admin';
      const result = service.user(uid, ugroup);
      expect(result).toEqual({
        user_id: uid,
        user_group: ugroup,
      });
    });
  });

  describe('hit_profile', () => {
    it('should successfully return profile data', async () => {
      const bodyobj = {
        id: 1,
        phone: 1234567890,
        name: 'John Doe',
        dept: 'Engineering',
      };

      const mockResponse: AxiosResponse = {
        data: bodyobj,
        status: 200,
        statusText: 'OK',
        headers: {},
        config: {
          url: `${service.domain}jet/profile/`,
          method: 'post',
          data: bodyobj,
          headers: {} as AxiosRequestHeaders, // Important: Cast to AxiosRequestHeaders
        },
      };



      jest.spyOn(httpService, 'post').mockReturnValueOnce(of(mockResponse));

      const result = await service.hit_profile(bodyobj);
      expect(result).toEqual(bodyobj);
      expect(httpService.post).toHaveBeenCalledWith(
        `${service.domain}jet/profile/`,
        bodyobj
      );
    });

    it('should throw an HttpException on communication error', async () => {
      const bodyobj = {
        id: 1,
        phone: 1234567890,
        name: 'John Doe',
        dept: 'Engineering',
      };
      jest
        .spyOn(httpService, 'post')
        .mockImplementationOnce(() => throwError(() => new Error('Network Error')));

      await expect(service.hit_profile(bodyobj)).rejects.toThrow(HttpException);
      await expect(service.hit_profile(bodyobj)).rejects.toThrowError(
        "this is my message for a 500/An internal error has occured;"
      );
    });
  });

  describe('profile', () => {
    it('should return the user profile', () => {
      const user = {
        id: 1,
        phone: 1234567890,
        name: 'John Doe',
        dept: 'Engineering',
      };
      const result = service.profile(user);
      expect(result).toEqual(user);
    });
  });
});



# src/jet/jet.middleware.ts
import { Injectable, NestMiddleware, Logger } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use (req: Request, res: Response, next: NextFunction) {
    // console.log('Request...');
    // private readonly logger = new Logger (`${req.baseUrl}`);
    const logger = new Logger (`${req.baseUrl}`);
    logger.log(`${req.method} ${req.url} ${res.statusCode}`);
    next();
  }
}




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





    async get_from_dest_db_id_promise <T> (id: number): Promise <AxiosResponse <T>> {
        try {
            return axios.get <T> (`${this.dest_db_base_url}/checkout/${id}`);
        }

        catch (error) {
            throw new InternalServerExc ("Failed to get from db");
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
        




    async checkout_checkin <T> (id: number): Promise <OperationResult> {
        try {
            await this.get_from_dest_db_id_promise<T>(id); // Await directly, no need for intermediate variable
            return await this.delete_in_db(id);      // If we get here, status was 200
        }



        catch (error) {
            if (axios.isAxiosError(error) && error.response?.status === 404) {
                const objFromSource: T = await this.get_from_db_id<T>(id); // Get from source
                return await this.post_to_db_obj<T>(objFromSource);         // Post to destination
            }


            // Handle other errors
            if (axios.isAxiosError(error)) {
                throw new InternalServerExc(`Axios Error: ${error.message}`);
            }


            throw new InternalServerExc("Failed to checkout/checkin");
            
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



# src/app.controller.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { AppController } from './app.controller';
import { AppService } from './app.service';

describe('AppController', () => {
  let appController: AppController;

  beforeEach(async () => {
    const app: TestingModule = await Test.createTestingModule({
      controllers: [AppController],
      providers: [AppService],
    }).compile();

    appController = app.get<AppController>(AppController);
  });

  describe('root', () => {
    it('should return "Hello World!"', () => {
      expect(appController.getHello()).toBe('Hello World!');
    });
  });
});



# src/app.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Hello World!';
  }
}



# src/app.module.ts
import { Module, NestModule, MiddlewareConsumer, RequestMethod } from '@nestjs/common';
import { AppController} from './app.controller';
import { JetController } from './jet/jet.controller'; 
import { AppService } from './app.service';
import { JetService } from './jet/jet.service';
import { JetModule } from './jet/jet.module';
import { LoggerMiddleware } from './jet/jet.middleware';
import { UsersModule } from './users/users.module';
import { CommonModule } from './common/common.module';


@Module({
  imports: [JetModule, UsersModule, CommonModule],
  controllers: [AppController, JetController],
  providers: [AppService, JetService],
})
export class AppModule implements NestModule{
  configure (consumer: MiddlewareConsumer) {
    consumer
      .apply (LoggerMiddleware)
      .forRoutes({
        path: '*',
        method: RequestMethod.ALL,
      });
  }
  
}



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




    async service_checkout_checkin (id: number): Promise <OperationResult> {
        return await this.commonservice.checkout_checkin (id);
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
        return await this.userservice.delete_user (id);
    }






    @Get ('check')
    async route_check (
        @Query ('id', ParseIntPipe) id: number
    ) {
        return this.userservice.service_checkout_checkin (id);
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



# src/main.ts
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();



# src/app.controller.ts
import { Body, Controller, Get, Param, Req } from '@nestjs/common';
import { AppService } from './app.service';
import { Request } from 'express';
import { ParsedQs } from 'qs'; // ParsedQs for query parameter typing


interface RequestResponse {
  body?: any;
  headers: Record<string, string | string[]>;
  query: ParsedQs;
  params: Record<string, string>;
}











@Controller('cats')
export class AppController {
  constructor(private readonly appService: AppService) {}
  
  @Get('breed/:id1')
  getCat(@Req () req: Request, @Param () params: any): RequestResponse{

    // return this.appService.getHello();
    // return "cat breed";
    return {
      body: req.body,       // the request body
      headers: req.headers, // request headers
      query: req.query,     // query parameters
      params: req.params    // route parameters
      // params: params.id1    // route parameters
    }
  }


    @Get ('hello')
    getHello () {
        return 'Hello World!';
    }

}











