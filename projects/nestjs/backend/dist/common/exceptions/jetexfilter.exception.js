"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.JetExFilter = void 0;
const common_1 = require("@nestjs/common");
let JetExFilter = class JetExFilter {
    catch(exception, host) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse();
        const request = ctx.getRequest();
        const status = exception.getStatus();
        const standard_exc_body = exception.getResponse();
        response
            .status(status)
            .json({
            standard_exc_body,
        });
    }
};
exports.JetExFilter = JetExFilter;
exports.JetExFilter = JetExFilter = __decorate([
    (0, common_1.Catch)(common_1.HttpException)
], JetExFilter);
//# sourceMappingURL=jetexfilter.exception.js.map