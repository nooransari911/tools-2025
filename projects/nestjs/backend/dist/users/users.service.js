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
exports.UsersService = void 0;
const common_1 = require("@nestjs/common");
const common_service_1 = require("../common/common.service");
let UsersService = class UsersService {
    constructor(commonservice) {
        this.commonservice = commonservice;
    }
    async get_user_id(id) {
        return this.commonservice.get_from_db_id(id);
    }
    async get_user_batch(ids) {
        return this.commonservice.get_from_db_id_batch(ids);
    }
    async post_user_id(id) {
        const user = await this.commonservice.get_from_db_id(id);
        const opres = await this.commonservice.post_to_db_obj(user);
        return opres;
    }
    async post_user(user) {
        const opres = await this.commonservice.post_to_db_obj(user);
        return opres;
    }
    async post_user_batch(user) {
        const opres = await this.commonservice.post_to_db_obj_batch(user);
        return opres;
    }
    async delete_user(id) {
        const opres = await this.commonservice.delete_in_db(id);
        return opres;
    }
    async service_checkout_checkin(id) {
        return await this.commonservice.checkout_checkin(id);
    }
};
exports.UsersService = UsersService;
exports.UsersService = UsersService = __decorate([
    (0, common_1.Injectable)(),
    __metadata("design:paramtypes", [common_service_1.CommonService])
], UsersService);
//# sourceMappingURL=users.service.js.map