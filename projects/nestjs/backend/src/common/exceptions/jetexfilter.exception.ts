import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Logger } from "@nestjs/common";
import { Request, Response } from "express";




@Catch (HttpException)
export class JetExFilter implements ExceptionFilter {
  // public readonly logger = new Logger ('JetController')


  catch(exception: HttpException, host: ArgumentsHost) {
      const ctx = host.switchToHttp ();
      const response = ctx.getResponse<Response> ();
      const request = ctx.getRequest<Request> ();
      const status = exception.getStatus ();
      const standard_exc_body = exception.getResponse ();




      response
        .status (status)
        .json ({
          standard_exc_body,
          // path: request.url,
        })
  }

}
