import { Controller, Get } from '@nestjs/common';
import { AppService, SchoolListService } from './app.service';
import { SchoolListInterface } from './interfaces/school-list.interface';

@Controller('hello')
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }
}

@Controller('schools')
export class SchoolListController {
  constructor(private schoolListService: SchoolListService) {}

  @Get()
  async getSchoolList(): Promise<SchoolListInterface> {
    return this.schoolListService.loadLocalJson<SchoolListInterface>(
      'data/school_url.json',
      // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
      SchoolListInterface,
    );
  }
}
