
import { TestEventConsumer } from './services/TestEventConsumer';
import { runTestSuite } from './runner/TestRunner';
import { testSuite } from './tests/suite';
import { createTestInstance } from './factory/CarinaeFactory';

async function main() {
  // 1. Create a fresh instance of Carinae and its dependencies
  const { carinae, keyService, eventBus } = createTestInstance();

  // 2. Create and start the event consumer
  const eventConsumer = new TestEventConsumer(eventBus);
  eventConsumer.startListening();

  // 3. Define the context object to be passed to every test
  const testContext = {
    carinae,
    keyService,
    eventConsumer,
  };

  // 4. Run the entire test suite
  await runTestSuite(testSuite, testContext);
}

main().catch(error => {
  console.error("A critical error occurred while running the test suite:", error);
  process.exit(1);
});