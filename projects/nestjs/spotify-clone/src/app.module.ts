import { Module, NestModule, MiddlewareConsumer, RequestMethod } from '@nestjs/common';
import { AppController} from './app.controller';
import { JetController } from './jet/jet.controller'; 
import { AppService } from './app.service';
import { JetService } from './jet/jet.service';
import { JetModule } from './jet/jet.module';
import { LoggerMiddleware } from './jet/jet.middleware';


@Module({
  imports: [JetModule],
  controllers: [AppController, JetController],
  providers: [AppService, JetService],
})
export class AppModule implements NestModule{
  configure (consumer: MiddlewareConsumer) {
    consumer
      .apply (LoggerMiddleware)
      .forRoutes({
        path: '*',
        method: RequestMethod.ALL,
      });
  }
  
}
