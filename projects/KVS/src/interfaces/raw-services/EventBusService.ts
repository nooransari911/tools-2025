import { MessageInterface } from "../core/Messages/Message";

export type EventTopic = string;
export type EventCallback = (message: MessageInterface) => void;

export interface EventBusServiceInterface {
    Publish(topic: EventTopic, message: MessageInterface): void;
    Subscribe(topic: EventTopic, callback: EventCallback): () => void;
    PublishForAllTopics(key: string, operation: string, message: MessageInterface): void;
}