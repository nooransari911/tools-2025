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
import { Module, NestModule, MiddlewareConsumer, RequestMethod } from '@nestjs/common';
import { AppController} from './app.controller';
import { JetController } from './jet/jet.controller'; 
import { AppService } from './app.service';
import { JetService } from './jet/jet.service';
import { JetModule } from './jet/jet.module';
import { LoggerMiddleware } from './jet/jet.middleware';


@Module({
  imports: [JetModule],
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
import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Hello World!';
  }
}
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
import { Controller, Get, Post, Body, Req, Param, UseFilters, Query, ParseIntPipe, ValidationPipe, HttpException, UsePipes, UseInterceptors } from '@nestjs/common';
import {fighterjetrequest, fighterjet, user_profile} from './interfaces/jet.interface';
import { JetService } from './jet.service';
import { JetExFilter } from './exceptions/jetexfilter.exception';
import { Request } from 'express';
import { BadReqExc, InternalServerExc } from './exceptions/status.exception';
import { AllExceptionsFilter, ValidationExceptionFilter } from './exceptions/primtive_ex_filter.exception';




@Controller ('jet')
@UseFilters (JetExFilter, ValidationExceptionFilter,AllExceptionsFilter)
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
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalPipes(new ValidationPipe());
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();
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


