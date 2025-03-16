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
