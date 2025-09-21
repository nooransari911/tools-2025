import { TestCase } from "../runner/TestRunner";
import { basicCrudTests } from "./basicCRUD.test.ts";

export const testSuite: TestCase[] = [
    ...basicCrudTests,
    // ... you can add other test suites here later
];