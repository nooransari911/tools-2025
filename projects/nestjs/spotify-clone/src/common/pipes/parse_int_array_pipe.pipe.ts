import { Injectable, PipeTransform, ArgumentMetadata} from '@nestjs/common';
import { InternalServerExc } from '../exceptions/status.exception';
import { privateEncrypt } from 'node:crypto';

@Injectable()
export class ParseIntArrayPipe implements PipeTransform {
  transform(value: any, metadata: ArgumentMetadata) {
    // If the value is a string, try parsing it as a JSON array
    if (typeof value === 'string') {
      try {
        // Try to parse it as a JSON array
        value = JSON.parse(value);
        // console.log (value);
      } catch (e) {
        throw new InternalServerExc ('Invalid array format');
      }
    }

    // Check if the value is now an array
    if (!Array.isArray(value)) {
      throw new InternalServerExc ('Query parameter should be an array');
    }

    // Validate that each item in the array is a valid integer
    const parsedArray = value.map((item) => {
      const parsedValue = parseInt(item, 10);
      if (isNaN(parsedValue)) {
        throw new InternalServerExc ('All elements must be valid integers');
      }
      return parsedValue;
    });

    // console.log (`The parsed array is: ${parsedArray}`)
    return parsedArray;
  }
}
