import { PipeTransform, ArgumentMetadata } from '@nestjs/common';
export declare class ParseIntArrayPipe implements PipeTransform {
    transform(value: any, metadata: ArgumentMetadata): number[];
}
