import { ArgumentsHost, BadRequestException, Catch, ExceptionFilter, HttpException, HttpStatus } from "@nestjs/common";
import { BadReqExc } from "./status.exception";
import { request, Response } from "express";

@Catch(BadRequestException)
export class ValidationExceptionFilter implements ExceptionFilter<BadRequestException> {
  public catch (exception, host: ArgumentsHost) {
    const ctx = host.switchToHttp ();
    const response = ctx.getResponse<Response> ();
    const request = ctx.getRequest<Request> ();
    const status = exception.getStatus ();
    const standard_exc_body = {
          status: HttpStatus.BAD_REQUEST,
          status_string: "Invalidation Failed;",
          timestamp: new Date ().toISOString(),
          message: "Invalidation Failed;",
          requested_resource: request.url
        }    
        
    response
      .status(status)
      .json({
        standard_exc_body,
        // path: request.url
      })
  
  }

}



@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  public catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    // Determine the status code
    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    // Determine status string and message based on the exception
    let status_string = "Internal Server Error";
    let message = "An unexpected error occurred.";

    if (exception instanceof HttpException) {
      // Attempt to extract message from HttpException response
      const httpExceptionResponse = exception.getResponse();

      if (typeof httpExceptionResponse === 'object' && httpExceptionResponse !== null && 'status_string' in httpExceptionResponse) {
        status_string = (httpExceptionResponse as { status_string: string }).status_string;
      }

      if (typeof httpExceptionResponse === 'string') {
        message = httpExceptionResponse;
      } else if (typeof httpExceptionResponse === 'object' && httpExceptionResponse !== null && 'message' in httpExceptionResponse) {
        message = (httpExceptionResponse as { message: string }).message;
      }
      
    }



    // Build the response body, closely matching your original format
    const errorResponse = {
      standard_exc_body: {
        status: status,
        status_string: status_string,
        timestamp: new Date().toISOString(),
        message: message,
        requested_resource: request.url,
      },
      // path: request.url,
    };

    // Log the error (optional but recommended)
    console.error(exception);

    // Send the response
    response.status(status).json(errorResponse);
  }
}
