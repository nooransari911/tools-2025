import { Logger } from "@nestjs/common";
import { HttpService } from "@nestjs/axios";
import { fighterjet, user_profile } from "./interfaces/jet.interface";
export declare class JetService {
    private readonly httpservice;
    readonly logger: Logger;
    readonly domain = "http://localhost:3000/";
    constructor(httpservice: HttpService);
    france(): fighterjet[];
    china(): fighterjet[];
    vietnam(): void;
    nz(): void;
    user(uid: number, ugroup: string): {
        user_id: number;
        user_group: string;
    };
    hit_profile(bodyobj: user_profile): Promise<any>;
    post_user_profile(bodyobj: user_profile): Promise<any>;
    profile(user: user_profile): user_profile;
}
