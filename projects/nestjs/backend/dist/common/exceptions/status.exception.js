"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.BadReqExc = exports.InternalServerExc = exports.TeaExc = exports.ForbExc = void 0;
const common_1 = require("@nestjs/common");
class ForbExc extends common_1.HttpException {
    constructor(message) {
        super({
            status: common_1.HttpStatus.FORBIDDEN,
            status_string: "Forbidden Request;",
            timestamp: new Date().toISOString(),
            message: "This is my message for a 403/forbidden status code",
            requested_resource: message
        }, common_1.HttpStatus.FORBIDDEN);
        this.logger = new common_1.Logger('JetController');
        this.logger.error(`Exception:: message:  ${message}`);
    }
}
exports.ForbExc = ForbExc;
class TeaExc extends common_1.HttpException {
    constructor(message) {
        super({
            status: common_1.HttpStatus.I_AM_A_TEAPOT,
            status_string: "I'm a Teapot;",
            timestamp: new Date().toISOString(),
            message: "This is my message for a 418/I'm a teapot status code",
            requested_resource: message
        }, common_1.HttpStatus.I_AM_A_TEAPOT);
        this.logger = new common_1.Logger('JetController');
        this.logger.error(`Exception:: message:  ${message}`);
    }
}
exports.TeaExc = TeaExc;
class InternalServerExc extends common_1.HttpException {
    constructor(message) {
        super({
            status: common_1.HttpStatus.INTERNAL_SERVER_ERROR,
            status_string: "An internal error has occured;",
            timestamp: new Date().toISOString(),
            message: "this is my message for a 500/An internal error has occured;",
            requested_resource: message
        }, common_1.HttpStatus.INTERNAL_SERVER_ERROR);
        this.logger = new common_1.Logger('JetController');
        this.logger.error(`Exception:: message:  ${message}`);
    }
}
exports.InternalServerExc = InternalServerExc;
class BadReqExc extends common_1.HttpException {
    constructor(message) {
        super({
            status: common_1.HttpStatus.BAD_REQUEST,
            status_string: "Invalidation Failed;",
            timestamp: new Date().toISOString(),
            message: "Invalidation Failed;",
            requested_resource: message
        }, common_1.HttpStatus.BAD_REQUEST);
        this.logger = new common_1.Logger('JetController');
        this.logger.error(`Exception:: message:  ${message}`);
    }
}
exports.BadReqExc = BadReqExc;
//# sourceMappingURL=status.exception.js.map