import {
    MessageInterface,
    ResponseInterface
} from '../../interfaces/core/Messages/Message';


export interface MessageServiceInterface {
    Handle(message: MessageInterface): Promise<ResponseInterface>;
}