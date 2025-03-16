import { Injectable, NestMiddleware, Logger } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class LoggerMiddleware implements NestMiddleware {
  use (req: Request, res: Response, next: NextFunction) {
    // console.log('Request...');
    // private readonly logger = new Logger (`${req.baseUrl}`);
    const logger = new Logger (`${req.baseUrl}`);
    logger.log(`${req.method} ${req.url} ${res.statusCode}`);
    next();
  }
}

