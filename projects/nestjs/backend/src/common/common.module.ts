import { Module } from '@nestjs/common';
import { CommonService } from './common.service';
import { CommonController } from './common.controller';

@Module({
  providers: [CommonService],
  controllers: [CommonController],
  exports: [CommonService]
})
export class CommonModule {}
