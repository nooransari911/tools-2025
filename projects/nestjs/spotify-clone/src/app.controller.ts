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
        return '<h1>Hello World!</h1>';
    }

}








