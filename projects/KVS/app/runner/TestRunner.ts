import { CarinaeServiceInterface } from "@src/interfaces/public-services/CarinaeInterface";
import { KeyServiceInterface } from "@src/interfaces/raw-services/KeyService";
import { TestEventConsumer } from "app/services/TestEventConsumer";

// TestContext provides a standardized way to pass dependencies to each test.
export interface TestContext {
  carinae: CarinaeServiceInterface;
  keyService: KeyServiceInterface;
  eventConsumer: TestEventConsumer;
}


// TestCase defines the structure for a single test.
export interface TestCase {
    title: string;
    testFn: (context: TestContext) => Promise<void>;
}

export async function runTestSuite(suite: TestCase[], context: TestContext) {
    let passed = 0;
    let failed = 0;

    console.log(`\n\n--- Starting Test Suite: ${suite.length} tests ---\n`);

    for (const testCase of suite) {
        try {
            // Pass the context to each test function
            await testCase.testFn(context);
            console.log(`🟢 PASSED: ${testCase.title}`);
            passed++;
        } catch (error: any) {
            console.error(`🔴 FAILED: ${testCase.title}`);
            console.error(`   └─ Error: ${error.message}\n`);
            failed++;
        }
    }

    console.log('\n--- Test Suite Complete ---');
    console.log(`Results: ${passed} passed, ${failed} failed.`);

    if (failed > 0) {
        process.exit(1); // Exit with a failure code
    }
}