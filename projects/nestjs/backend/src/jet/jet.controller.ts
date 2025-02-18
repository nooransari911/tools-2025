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
