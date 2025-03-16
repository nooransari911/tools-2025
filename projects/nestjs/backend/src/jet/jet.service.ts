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












