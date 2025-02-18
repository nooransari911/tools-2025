"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.ParseIntArrayPipe = void 0;
const common_1 = require("@nestjs/common");
const status_exception_1 = require("../exceptions/status.exception");
let ParseIntArrayPipe = class ParseIntArrayPipe {
    transform(value, metadata) {
        if (typeof value === 'string') {
            try {
                value = JSON.parse(value);
            }
            catch (e) {
                throw new status_exception_1.InternalServerExc('Invalid array format');
            }
        }
        if (!Array.isArray(value)) {
            throw new status_exception_1.InternalServerExc('Query parameter should be an array');
        }
        const parsedArray = value.map((item) => {
            const parsedValue = parseInt(item, 10);
            if (isNaN(parsedValue)) {
                throw new status_exception_1.InternalServerExc('All elements must be valid integers');
            }
            return parsedValue;
        });
        return parsedArray;
    }
};
exports.ParseIntArrayPipe = ParseIntArrayPipe;
exports.ParseIntArrayPipe = ParseIntArrayPipe = __decorate([
    (0, common_1.Injectable)()
], ParseIntArrayPipe);
//# sourceMappingURL=parse_int_array_pipe.pipe.js.map