import { Module } from '@nestjs/common';
import { AppController, SchoolListController } from './app.controller';
import { AppService, SchoolListService } from './app.service';

@Module({
  imports: [],
  controllers: [AppController, SchoolListController],
  providers: [AppService, SchoolListService],
})
export class AppModule {}
