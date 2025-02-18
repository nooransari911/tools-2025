"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.JetService = void 0;
const common_1 = require("@nestjs/common");
const axios_1 = require("@nestjs/axios");
const status_exception_1 = require("./exceptions/status.exception");
const rxjs_1 = require("rxjs");
let JetService = class JetService {
    constructor(httpservice) {
        this.httpservice = httpservice;
        this.logger = new common_1.Logger('JetController');
        this.domain = "http://localhost:3000/";
    }
    france() {
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
        ];
    }
    china() {
        return [
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
        ];
    }
    vietnam() {
        throw new status_exception_1.ForbExc('vietnam');
    }
    nz() {
        throw new status_exception_1.TeaExc('NZ');
    }
    user(uid, ugroup) {
        return {
            user_id: uid,
            user_group: ugroup
        };
    }
    async hit_profile(bodyobj) {
        try {
            const profile_response = await (0, rxjs_1.lastValueFrom)(this.httpservice.post(`${this.domain}jet/profile/`, bodyobj));
            return profile_response.data;
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("[JetService] Hitting Profile;");
        }
    }
    async post_user_profile(bodyobj) {
        try {
            const profile_response = await (0, rxjs_1.lastValueFrom)(this.httpservice.post(`${this.domain}jet/profile/`, bodyobj));
            return profile_response.data;
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("[JetService] Error when Post to Profile;");
        }
    }
    profile(user) {
        this.logger.log(user);
        return user;
    }
};
exports.JetService = JetService;
exports.JetService = JetService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [axios_1.HttpService])
], JetService);
//# sourceMappingURL=jet.service.js.map