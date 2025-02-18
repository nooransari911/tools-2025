"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AppModule = void 0;
const common_1 = require("@nestjs/common");
const app_controller_1 = require("./app.controller");
const jet_controller_1 = require("./jet/jet.controller");
const app_service_1 = require("./app.service");
const jet_service_1 = require("./jet/jet.service");
const jet_module_1 = require("./jet/jet.module");
const jet_middleware_1 = require("./jet/jet.middleware");
const users_module_1 = require("./users/users.module");
const common_module_1 = require("./common/common.module");
const common_controller_1 = require("./common/common.controller");
const common_service_1 = require("./common/common.service");
let AppModule = class AppModule {
    configure(consumer) {
        consumer
            .apply(jet_middleware_1.LoggerMiddleware)
            .forRoutes({
            path: '*',
            method: common_1.RequestMethod.ALL,
        });
    }
};
exports.AppModule = AppModule;
exports.AppModule = AppModule = __decorate([
    (0, common_1.Module)({
        imports: [jet_module_1.JetModule, users_module_1.UsersModule, common_module_1.CommonModule],
        controllers: [app_controller_1.AppController, jet_controller_1.JetController, common_controller_1.CommonController],
        providers: [app_service_1.AppService, jet_service_1.JetService, common_service_1.CommonService],
    })
], AppModule);
//# sourceMappingURL=app.module.js.map