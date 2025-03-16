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





