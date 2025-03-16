import { ArgumentsHost, HttpException, HttpStatus, Logger } from "@nestjs/common";




export class ForbExc extends HttpException {
  public readonly logger = new Logger ('JetController')

  constructor (message: string) {
    super ({
      status: HttpStatus.FORBIDDEN,
      status_string: "Forbidden Request;",
      timestamp: new Date ().toISOString(),
      message: "This is my message for a 403/forbidden status code",
      requested_resource: message
    }, HttpStatus.FORBIDDEN)

    
    this.logger.error (`Exception:: message:  ${message}`);
  }
}



export class TeaExc extends HttpException {
  public readonly logger = new Logger ('JetController')


  constructor (message: string) {
    super ({
      status: HttpStatus.I_AM_A_TEAPOT,
      status_string: "I'm a Teapot;",
      timestamp: new Date ().toISOString(),
      message: "This is my message for a 418/I'm a teapot status code",
      requested_resource: message
    }, HttpStatus.I_AM_A_TEAPOT)


    this.logger.error (`Exception:: message:  ${message}`);
  }
}



export class InternalServerExc extends HttpException {
  public readonly logger = new Logger ('JetController')


  constructor (message: string) {
    super ({
      status: HttpStatus.INTERNAL_SERVER_ERROR,
      status_string: "An internal error has occured;",
      timestamp: new Date ().toISOString(),
      message: "this is my message for a 500/An internal error has occured;",
      requested_resource: message
    }, HttpStatus.INTERNAL_SERVER_ERROR)


    this.logger.error (`Exception:: message:  ${message}`);
  }
}





export class BadReqExc extends HttpException {
  public readonly logger = new Logger ('JetController')


  constructor (message: string) {
    super ({
      status: HttpStatus.BAD_REQUEST,
      status_string: "Invalidation Failed;",
      timestamp: new Date ().toISOString(),
      message: "Invalidation Failed;",
      requested_resource: message
    }, HttpStatus.BAD_REQUEST)  


    this.logger.error (`Exception:: message:  ${message}`);
  }
}


