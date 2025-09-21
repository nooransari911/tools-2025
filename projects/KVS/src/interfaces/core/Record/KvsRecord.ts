import { KvsEntryInterface } from "../Data/KvsEntryInterface";
import { KvsKeyInterface } from "../Key/KvsKeyInterface";




export interface KvsRecord <T = any> {
    Key: KvsKeyInterface;
    Value: KvsEntryInterface <T>
}