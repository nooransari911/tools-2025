import { MessageInterface, ResponseInterface } from "../../interfaces/core/Messages/Message";
import { MessageServiceInterface } from "../../interfaces/raw-services/MessageService";

async function handleSet(message: MessageInterface): Promise<ResponseInterface> {
    // Handle SET operation
    return {
        Success: true,
        Value: null,
        Error: null
    };
}

async function handleGet(message: MessageInterface): Promise<ResponseInterface> {
    // Handle GET operation
    return {
        Success: true,
        Found: true,
        Value: { /* retrieved data */ },
        Error: null
    };
}

async function handleDelete(message: MessageInterface): Promise<ResponseInterface> {
    // Handle DELETE operation
    return {
        Success: true,
        Value: null,
        Error: null
    };
}


export class Message implements MessageServiceInterface {
    private handlers = new Map<string, (message: MessageInterface) => Promise<ResponseInterface>>([
        ['SET', handleSet],
        ['GET', handleGet],
        ['DELETE', handleDelete]
    ]);

    async Handle(message: MessageInterface): Promise<ResponseInterface> {
        const handler = this.handlers.get(message.Type);
        
        if (!handler) {
            return {
                Success: false,
                Value: null,
                Error: `Unknown message type: ${message.Type}`
            };
        }

        return handler(message);
    }
}