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
exports.CommonController = void 0;
const common_1 = require("@nestjs/common");
const common_service_1 = require("./common.service");
let CommonController = class CommonController {
    constructor(commonservice) {
        this.commonservice = commonservice;
    }
    ;
    function_get_hello(req, res) {
        const req_headers_string = this.commonservice.req_headers_string(req);
        const res_headers_string = this.commonservice.res_headers_string(res);
        const return_string = this.commonservice.hello_world_html_string + req_headers_string + res_headers_string;
        return return_string;
    }
    async function_get_france() {
        const response_france = await this.commonservice.jets_france_from_route();
        return response_france;
    }
    async function_get_china() {
        const response_china = await this.commonservice.jets_china_from_db();
        return response_china;
    }
};
exports.CommonController = CommonController;
__decorate([
    (0, common_1.Get)('hello'),
    __param(0, (0, common_1.Req)()),
    __param(1, (0, common_1.Res)({
        passthrough: true
    })),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Object, Object]),
    __metadata("design:returntype", void 0)
], CommonController.prototype, "function_get_hello", null);
__decorate([
    (0, common_1.Get)('france'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], CommonController.prototype, "function_get_france", null);
__decorate([
    (0, common_1.Get)('china'),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", []),
    __metadata("design:returntype", Promise)
], CommonController.prototype, "function_get_china", null);
exports.CommonController = CommonController = __decorate([
    (0, common_1.Controller)('common'),
    __metadata("design:paramtypes", [common_service_1.CommonService])
], CommonController);
//# sourceMappingURL=common.controller.js.map