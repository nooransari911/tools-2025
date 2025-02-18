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
exports.UsersController = void 0;
const common_1 = require("@nestjs/common");
const parse_int_array_pipe_pipe_1 = require("../common/pipes/parse_int_array_pipe.pipe");
const user_interface_1 = require("./interfaces/user.interface");
const users_service_1 = require("./users.service");
let UsersController = class UsersController {
    constructor(userservice) {
        this.userservice = userservice;
    }
    async function_get_user(id) {
        const response_user = await this.userservice.get_user_id(id);
        return response_user;
    }
    async function_get_user_batch(ids) {
        const response_user_batch = await this.userservice.get_user_batch(ids);
        return response_user_batch;
    }
    async function_user_post_id(id) {
        const hit_post_promise = this.userservice.post_user_id(id);
        const await_promise = await hit_post_promise;
        return await_promise;
    }
    async function_user_post_body(body) {
        const hit_post_promise = this.userservice.post_user(body);
        const await_promise = await hit_post_promise;
        return await_promise;
    }
    async function_user_post_body_batch(body) {
        const hit_post_promise = this.userservice.post_user_batch(body);
        const await_promise = await hit_post_promise;
        return await_promise;
    }
    async function_user_delete(id) {
        return await this.userservice.delete_user(id);
    }
    async route_check(id) {
        return this.userservice.service_checkout_checkin(id);
    }
};
exports.UsersController = UsersController;
__decorate([
    (0, common_1.Get)('user'),
    __param(0, (0, common_1.Query)('id', common_1.ParseIntPipe)),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number]),
    __metadata("design:returntype", Promise)
], UsersController.prototype, "function_get_user", null);
__decorate([
    (0, common_1.Get)('user-batch'),
    __param(0, (0, common_1.Query)('ids', parse_int_array_pipe_pipe_1.ParseIntArrayPipe)),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Array]),
    __metadata("design:returntype", Promise)
], UsersController.prototype, "function_get_user_batch", null);
__decorate([
    (0, common_1.Get)('post-user'),
    __param(0, (0, common_1.Query)('id', common_1.ParseIntPipe)),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number]),
    __metadata("design:returntype", Promise)
], UsersController.prototype, "function_user_post_id", null);
__decorate([
    (0, common_1.Post)('post-user'),
    __param(0, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [user_interface_1.User]),
    __metadata("design:returntype", Promise)
], UsersController.prototype, "function_user_post_body", null);
__decorate([
    (0, common_1.Post)('post-user-batch'),
    __param(0, (0, common_1.Body)()),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Array]),
    __metadata("design:returntype", Promise)
], UsersController.prototype, "function_user_post_body_batch", null);
__decorate([
    (0, common_1.Delete)('delete-user'),
    __param(0, (0, common_1.Query)('id', common_1.ParseIntPipe)),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number]),
    __metadata("design:returntype", Promise)
], UsersController.prototype, "function_user_delete", null);
__decorate([
    (0, common_1.Get)('check'),
    __param(0, (0, common_1.Query)('id', common_1.ParseIntPipe)),
    __metadata("design:type", Function),
    __metadata("design:paramtypes", [Number]),
    __metadata("design:returntype", Promise)
], UsersController.prototype, "route_check", null);
exports.UsersController = UsersController = __decorate([
    (0, common_1.Controller)('users'),
    __metadata("design:paramtypes", [users_service_1.UsersService])
], UsersController);
//# sourceMappingURL=users.controller.js.map