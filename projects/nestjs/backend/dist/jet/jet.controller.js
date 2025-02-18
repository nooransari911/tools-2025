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
var __param = (this && this.__param) || function (paramIndex, decorator) {
    return function (target, key) { decorator(target, key, paramIndex); }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.JetController = void 0;
const common_1 = require("@nestjs/common");
const jet_interface_1 = require("./interfaces/jet.interface");
const jet_service_1 = require("./jet.service");
const jetexfilter_exception_1 = require("./exceptions/jetexfilter.exception");
const status_exception_1 = require("./exceptions/status.exception");
const primtive_ex_filter_exception_1 = require("./exceptions/primtive_ex_filter.exception");
let JetController = class JetController {
    constructor(jetservice) {
        this.jetservice = jetservice;
    }
    france(req, body) {
        return this.jetservice.france();
    }
    china(req, body) {
        return this.jetservice.china();
    }
    viet() {
        return this.jetservice.vietnam();
    }
    nz() {
        return this.jetservice.nz();
    }
    user(id, group) {
        return this.jetservice.user(id, group);
    }
    async hit_profile(req, id, phone, dept, name) {
        const bodyobj = {
            id: id,
            name: name,
            dept: dept,
            phone: phone
        };
        try {
            const response = await this.jetservice.hit_profile(bodyobj);
            return response;
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("[JetController] Hitting Profile;");
        }
    }
    profile(body) {
        return this.jetservice.profile(body);
    }
    async post_user_profile(req, query) {
        try {
            const response = await this.jetservice.post_user_profile(query);
            return response;
        }
        catch (error) {
            throw new status_exception_1.InternalServerExc("[JetController] Error when Post to Profile;");
        }
    }
};
exports.JetController = JetController;
__decorate([
    (0, common_1.Get)('france'),
    __param(0, (0, common_1.Req)()),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, jet_interface_1.fighterjetrequest]),
    __metadata("design:returntype", Array)
], JetController.prototype, "france", null);
__decorate([
    (0, common_1.Get)('china'),
    __param(0, (0, common_1.Req)()),
    __param(1, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, jet_interface_1.fighterjetrequest]),
    __metadata("design:returntype", Array)
], JetController.prototype, "china", null);
__decorate([
    (0, common_1.Get)('viet'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", void 0)
], JetController.prototype, "viet", null);
__decorate([
    (0, common_1.Get)('nz'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", void 0)
], JetController.prototype, "nz", null);
__decorate([
    (0, common_1.Get)('user'),
    __param(0, (0, common_1.Query)('uid', common_1.ParseIntPipe)),
    __param(1, (0, common_1.Query)('ugroup', common_1.ValidationPipe)),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number, String]),
    __metadata("design:returntype", void 0)
], JetController.prototype, "user", null);
__decorate([
    (0, common_1.Get)('hit-profile'),
    __param(0, (0, common_1.Req)()),
    __param(1, (0, common_1.Query)('id', common_1.ParseIntPipe)),
    __param(2, (0, common_1.Query)('phone', common_1.ParseIntPipe)),
    __param(3, (0, common_1.Query)('dept', common_1.ValidationPipe)),
    __param(4, (0, common_1.Query)('name', common_1.ValidationPipe)),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Number, Number, String, String]),
    __metadata("design:returntype", Promise)
], JetController.prototype, "hit_profile", null);
__decorate([
    (0, common_1.Post)('profile'),
    __param(0, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [jet_interface_1.user_profile]),
    __metadata("design:returntype", void 0)
], JetController.prototype, "profile", null);
__decorate([
    (0, common_1.Get)('post_user_profile'),
    __param(0, (0, common_1.Req)()),
    __param(1, (0, common_1.Query)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, jet_interface_1.user_profile]),
    __metadata("design:returntype", Promise)
], JetController.prototype, "post_user_profile", null);
exports.JetController = JetController = __decorate([
    (0, common_1.Controller)('jet'),
    (0, common_1.UseFilters)(jetexfilter_exception_1.JetExFilter, primtive_ex_filter_exception_1.ValidationExceptionFilter, primtive_ex_filter_exception_1.AllExceptionsFilter),
    __metadata("design:paramtypes", [jet_service_1.JetService])
], JetController);
//# sourceMappingURL=jet.controller.js.map