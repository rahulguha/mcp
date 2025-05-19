import { Injectable, Logger } from '@nestjs/common';
import { promises as fs } from 'fs';
import { join } from 'path';
import { SchoolListInterface } from './interfaces/school-list.interface';

@Injectable()
export class AppService {
  getHello(): string {
    return 'Hello Rahul!';
  }
}

@Injectable()
export class SchoolListService {
  private readonly logger = new Logger(SchoolListService.name);

  // For loading from local file (Node.js environment)
  async loadLocalJson<T extends object>(
    filePath: string,
    dtoClass: new () => T,
  ): Promise<T> {
    try {
      const absolutePath = join(process.cwd(), filePath);
      const rawData = await fs.readFile(absolutePath, 'utf8');
      // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
      const parsedData = JSON.parse(rawData);

      const dto = new dtoClass();
      Object.assign(dto, parsedData);
      // return JSON.parse(rawData) as T;
      return dto;
    } catch (error) {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      this.logger.error(`Failed to load JSON from ${filePath}`, error.stack);
      throw error;
    }
  }

  // For loading from URL (HTTP endpoint)
  async loadRemoteJson<T>(url: string): Promise<T> {
    try {
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return (await response.json()) as T;
    } catch (error) {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      this.logger.error(`Failed to load JSON from ${url}`, error.stack);
      throw error;
    }
  }
}
