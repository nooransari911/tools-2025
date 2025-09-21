import { EventEmitter } from 'events';
import { MessageInterface } from '../../interfaces/core/Messages/Message';
import { EventBusServiceInterface, EventCallback, EventTopic } from '../../interfaces/raw-services/EventBusService';

export class EventBus implements EventBusServiceInterface {
    private emitter: EventEmitter;
    private namespacesDepth: number;

    constructor (eventBusConfig?: {
        namespacesDepth?: number
    }) {
        this.emitter = new EventEmitter();
        this.emitter.setMaxListeners(100);
        this.namespacesDepth = eventBusConfig?.namespacesDepth ?? 4;
    }

    /**
     * Publishes a message to all subscribers of a given topic.
     */
    public Publish(topic: EventTopic, message: MessageInterface): void {
        this.emitter.emit(topic, message);
    }

    /**
     * Subscribes a listener to a topic.
     * @returns A function that can be called to unsubscribe the listener.
     */
    public Subscribe(topic: EventTopic, callback: EventCallback): () => void {
        this.emitter.on(topic, callback);

        // Return an "unsubscribe" function for cleanup
        return () => {
            this.emitter.off(topic, callback);
        };
    }


    /**
     * Generates a list of topics for a given key and operation.
     * This logic is now properly encapsulated within the EventBus.
     * It is generic and works with any string 'operation'.
     */
    private _generateTopicsForKey(key: string, operation: string): string[] {
        const topics: string[] = [
            operation
        ];

        if (this.namespacesDepth <= 0) {
            return topics;
        }

        const keyParts = key.split(':', 2);
        if (keyParts.length === 2) {
            // Namespaces path exists; convert it to a list and iterate upto first depth keys to form topics
            const namespacePath = keyParts[0];
            const namespaceParts = namespacePath.split('/');
            let currentPath = '';
            const depth = Math.min(this.namespacesDepth, namespaceParts.length);

            for (let i = 0; i < depth; i++) {
                const part = namespaceParts[i];
                currentPath = currentPath ? `${currentPath}/${part}` : part;
                topics.push(`${currentPath}#${operation}`);
            }
        }
        // No namespace path exists; topics is simply the {operation, key#operation}
        else {
            topics.push (`${key}#${operation}`);
        }
        return topics;
    }

    /**
     * Publishes a message related to a KVS key to all relevant hierarchical topics.
     */
    public PublishForAllTopics(key: string, operation: string, message: MessageInterface): void {
        const topics = this._generateTopicsForKey(key, operation);
        for (const topic of topics) {
            this.emitter.emit(topic, message);
        }
    }
}