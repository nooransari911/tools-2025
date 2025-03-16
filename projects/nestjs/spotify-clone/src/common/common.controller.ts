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


    @Get ('hello')
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
