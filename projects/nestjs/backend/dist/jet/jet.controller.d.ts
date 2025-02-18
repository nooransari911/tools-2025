import { fighterjetrequest, fighterjet, user_profile } from './interfaces/jet.interface';
import { JetService } from './jet.service';
import { Request } from 'express';
export declare class JetController {
    private jetservice;
    constructor(jetservice: JetService);
    france(req: Request, body: fighterjetrequest): fighterjet[];
    china(req: Request, body: fighterjetrequest): fighterjet[];
    viet(): void;
    nz(): void;
    user(id: number, group: string): {
        user_id: number;
        user_group: string;
    };
    hit_profile(req: Request, id: number, phone: number, dept: string, name: string): Promise<any>;
    profile(body: user_profile): user_profile;
    post_user_profile(req: Request, query: user_profile): Promise<any>;
}
