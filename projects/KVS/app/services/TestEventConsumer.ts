import { EventBusServiceInterface } from '@src/interfaces/raw-services/EventBusService';
import { MessageInterface } from '@src/interfaces/core/Messages/Message';

export class TestEventConsumer {
    private receivedMessages: MessageInterface[] = [];
    private eventBus: EventBusServiceInterface;

    constructor(eventBus: EventBusServiceInterface) {
        this.eventBus = eventBus;
    }

    /**
     * Subscribes to all relevant topics to start capturing events.
     */
    public startListening(): void {
        this.eventBus.Subscribe('SET', this.handleEvent.bind(this));
        this.eventBus.Subscribe('DELETE', this.handleEvent.bind(this));
        // We can add more generic topics here later
    }

    private handleEvent(message: MessageInterface): void {
        console.log(`[EVENT CONSUMER] Received event: Type='${message.Type}', Key='${message.Key}'`);
        this.receivedMessages.push(message);
    }

    /**
     * Waits for a specific event based on its key and type.
     * Throws an error if the event is not received within the timeout.
     */
    public async waitForEvent(type: 'SET' | 'DELETE', key: string, timeout = 500): Promise<MessageInterface> {
        return new Promise((resolve, reject) => {
            const checkInterval = setInterval(() => {
                const foundEvent = this.receivedMessages.find(
                    msg => msg.Type === type && msg.Key === key
                );
                if (foundEvent) {
                    clearTimeout(timer);
                    clearInterval(checkInterval);
                    resolve(foundEvent);
                }
            }, 10); // Check for the event every 10ms

            const timer = setTimeout(() => {
                clearInterval(checkInterval);
                reject(new Error(`Timeout: Event Type='${type}' for Key='${key}' not received.`));
            }, timeout);
        });
    }

    /**
     * Clears all captured events to ensure a clean state for the next test.
     */
    public clear(): void {
        this.receivedMessages = [];
    }
}