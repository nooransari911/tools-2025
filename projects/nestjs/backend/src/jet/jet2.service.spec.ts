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
