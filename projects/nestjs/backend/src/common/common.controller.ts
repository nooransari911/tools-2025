import { Controller, Get, ParseIntPipe, Query, Req, Res } from '@nestjs/common';
import axios from 'axios';
import { JetExFilter } from 'src/jet/exceptions/jetexfilter.exception';
import { fighterjet } from 'src/jet/interfaces/jet.interface';
import { CommonService } from 'src/common/common.service';
import { User } from 'src/users/interfaces/user.interface';
import { ParseIntArrayPipe } from './pipes/parse_int_array_pipe.pipe';
import { Request, Response } from 'express';




@Controller('common')
export class CommonController {
    constructor (private readonly commonservice: CommonService) {};


    @Get ('hello')
    function_get_hello (
        @Req () req: Request,
        @Res ({
            passthrough: true
        }) res: Response
    ) {
        const req_headers_string: string = this.commonservice.req_headers_string (req);
        const res_headers_string: string = this.commonservice.res_headers_string (res);
        // console.log (req_headers_string);

        const return_string: string = this.commonservice.hello_world_html_string + req_headers_string + res_headers_string;


        // console.log (return_string);
        return return_string;

        // res.setHeader('Content-Type', 'text/html'); // MUST set Content-Type
        // res.send(return_string); // Use res.send()        return return_string;
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
