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
