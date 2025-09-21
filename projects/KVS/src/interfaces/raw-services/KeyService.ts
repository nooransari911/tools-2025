import { KvsKeyInterface } from "../core/Key/KvsKeyInterface";

export interface KeyServiceInterface {
  Encode(key: KvsKeyInterface): string;
  Decode(keyString: string): KvsKeyInterface;
  Parse(Key: KvsKeyInterface): string [];
}