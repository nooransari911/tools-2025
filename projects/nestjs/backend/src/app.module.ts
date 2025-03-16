import { Module, NestModule, MiddlewareConsumer, RequestMethod } from '@nestjs/common';
import { AppController} from './app.controller';
import { JetController } from './jet/jet.controller'; 
import { AppService } from './app.service';
import { JetService } from './jet/jet.service';
import { JetModule } from './jet/jet.module';
import { LoggerMiddleware } from './jet/jet.middleware';
import { UsersModule } from './users/users.module';
import { CommonModule } from './common/common.module';
import { CommonController } from './common/common.controller';
import { CommonService } from './common/common.service';
import { AuthModule } from './auth/auth.module';


@Module({
  imports: [JetModule, UsersModule, CommonModule, AuthModule],
  controllers: [AppController, JetController, CommonController],
  providers: [AppService, JetService, CommonService],
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
