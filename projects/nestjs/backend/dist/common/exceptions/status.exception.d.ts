import { HttpException, Logger } from "@nestjs/common";
export declare class ForbExc extends HttpException {
    readonly logger: Logger;
    constructor(message: string);
}
export declare class TeaExc extends HttpException {
    readonly logger: Logger;
    constructor(message: string);
}
export declare class InternalServerExc extends HttpException {
    readonly logger: Logger;
    constructor(message: string);
}
export declare class BadReqExc extends HttpException {
    readonly logger: Logger;
    constructor(message: string);
}
