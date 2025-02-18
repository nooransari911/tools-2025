import { fighterjet } from 'src/jet/interfaces/jet.interface';
import { CommonService } from 'src/common/common.service';
import { Request, Response } from 'express';
export declare class CommonController {
    private readonly commonservice;
    constructor(commonservice: CommonService);
    function_get_hello(req: Request, res: Response): string;
    function_get_france(): Promise<fighterjet[]>;
    function_get_china(): Promise<fighterjet[]>;
}
