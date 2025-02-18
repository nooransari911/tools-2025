"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AllExceptionsFilter = exports.ValidationExceptionFilter = void 0;
const common_1 = require("@nestjs/common");
let ValidationExceptionFilter = class ValidationExceptionFilter {
    catch(exception, host) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse();
        const request = ctx.getRequest();
        const status = exception.getStatus();
        const standard_exc_body = {
            status: common_1.HttpStatus.BAD_REQUEST,
            status_string: "Invalidation Failed;",
            timestamp: new Date().toISOString(),
            message: "Invalidation Failed;",
            requested_resource: request.url
        };
        response
            .status(status)
            .json({
            standard_exc_body,
        });
    }
};
exports.ValidationExceptionFilter = ValidationExceptionFilter;
exports.ValidationExceptionFilter = ValidationExceptionFilter = __decorate([
    (0, common_1.Catch)(common_1.BadRequestException)
], ValidationExceptionFilter);
let AllExceptionsFilter = class AllExceptionsFilter {
    catch(exception, host) {
        const ctx = host.switchToHttp();
        const response = ctx.getResponse();
        const request = ctx.getRequest();
        const status = exception instanceof common_1.HttpException
            ? exception.getStatus()
            : common_1.HttpStatus.INTERNAL_SERVER_ERROR;
        let status_string = "Internal Server Error";
        let message = "An unexpected error occurred.";
        if (exception instanceof common_1.HttpException) {
            const httpExceptionResponse = exception.getResponse();
            if (typeof httpExceptionResponse === 'object' && httpExceptionResponse !== null && 'status_string' in httpExceptionResponse) {
                status_string = httpExceptionResponse.status_string;
            }
            if (typeof httpExceptionResponse === 'string') {
                message = httpExceptionResponse;
            }
            else if (typeof httpExceptionResponse === 'object' && httpExceptionResponse !== null && 'message' in httpExceptionResponse) {
                message = httpExceptionResponse.message;
            }
        }
        const errorResponse = {
            standard_exc_body: {
                status: status,
                status_string: status_string,
                timestamp: new Date().toISOString(),
                message: message,
                requested_resource: request.url,
            },
        };
        console.error(exception);
        response.status(status).json(errorResponse);
    }
};
exports.AllExceptionsFilter = AllExceptionsFilter;
exports.AllExceptionsFilter = AllExceptionsFilter = __decorate([
    (0, common_1.Catch)()
], AllExceptionsFilter);
//# sourceMappingURL=primtive_ex_filter.exception.js.map