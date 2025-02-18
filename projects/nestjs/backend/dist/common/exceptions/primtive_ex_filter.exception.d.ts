import { ArgumentsHost, BadRequestException, ExceptionFilter } from "@nestjs/common";
export declare class ValidationExceptionFilter implements ExceptionFilter<BadRequestException> {
    catch(exception: any, host: ArgumentsHost): void;
}
export declare class AllExceptionsFilter implements ExceptionFilter {
    catch(exception: unknown, host: ArgumentsHost): void;
}
