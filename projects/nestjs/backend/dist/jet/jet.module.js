"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.JetModule = void 0;
const common_1 = require("@nestjs/common");
const jet_controller_1 = require("./jet.controller");
const jet_service_1 = require("./jet.service");
const axios_1 = require("@nestjs/axios");
let JetModule = class JetModule {
};
exports.JetModule = JetModule;
exports.JetModule = JetModule = __decorate([
    (0, common_1.Module)({
        imports: [axios_1.HttpModule],
        controllers: [jet_controller_1.JetController],
        providers: [jet_service_1.JetService],
        exports: [axios_1.HttpModule]
    })
], JetModule);
//# sourceMappingURL=jet.module.js.map