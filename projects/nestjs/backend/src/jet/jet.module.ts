import { Module } from "@nestjs/common";
import { JetController } from "./jet.controller"; 
import { JetService } from "./jet.service"; 
import { HttpModule } from "@nestjs/axios";



@Module({
  imports: [HttpModule],
  controllers: [JetController],
  providers: [JetService],
  exports: [HttpModule]
})
export class JetModule {}
