import { Injectable } from '@nestjs/common';
import axios, { AxiosResponse } from 'axios';
import { fighterjet } from 'src/jet/interfaces/jet.interface';
import { User } from 'src/users/interfaces/user.interface';
import { InternalServerExc } from './exceptions/status.exception';
import { OperationResult } from './interfaces/operation_result.interface';





@Injectable()
export class CommonService {
    public hello_world_html_string = `
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Hello World</title>
                <style>
                    body {
                    background-color: black;
                    color: white;
                    font-family: 'Courier New', Courier, monospace;
                    }
                </style>
            </head>
            <body>
                <h1>Hello World</h1>
            </body>
        </html>
    `;

    public src_db_base_url = "http://localhost:7000";
    public dest_db_base_url = "http://localhost:8000";
    public self_base_url = "http://localhost:3000";



    async jets_france_from_route (): Promise <fighterjet []> {
        const response_france: AxiosResponse <fighterjet []> = await axios.get <fighterjet[]> (`${this.self_base_url}/jet/france/`);
        return response_france.data;
    }


    async jets_china_from_db (): Promise <fighterjet []> {
        const response_china_1: AxiosResponse <fighterjet> = await axios.get <fighterjet> (`${this.src_db_base_url}/1`);
        const response_china_2: AxiosResponse <fighterjet> = await axios.get <fighterjet> (`${this.src_db_base_url}/2`);



        return [
            response_china_1.data,
            response_china_2.data
        ]
    }


    async get_from_db_id <T> (id: number): Promise <T> {
        try {
            const obj_promise: Promise <AxiosResponse <T>> = axios.get <T> (`${this.src_db_base_url}/${id}`);
            const await_promise: AxiosResponse <T> = await obj_promise;
       
            return await_promise.data;
        }

    catch (error) {
        throw new InternalServerExc ("Failed to get from db");
    }

    
    }



    async get_from_db_id_batch <T> (ids: number []): Promise <T []> {
        try {
            const all_promises: Promise <AxiosResponse <T>> [] = ids.map (id =>
                axios.get <T> (`${this.src_db_base_url}/${id}`)
            );


            const await_promises: AxiosResponse <T> [] = await Promise.all (all_promises);

            const all_objs: T [] = await_promises.map (obj => obj.data);

            // console.log (`The fetched objs are: ${all_objs}`);

            return all_objs;

            
        }

        
        catch (error) {
            throw new InternalServerExc ("Error fetching the objs");
        }
    }





    async post_to_db_obj <T> (obj: T): Promise <OperationResult> {
        const a: OperationResult = {
            message: "hi",
            StatusCode: 200,
        }


        try {
            const obj_promise = await axios.post (`${this.dest_db_base_url}/checkout`, obj);

            return {
                message: "success",
                StatusCode: 200
            }
        }
        
        catch (error) {
            throw new InternalServerExc ("Failed to create/update object");
        }


    }






  
    async delete_in_db (id: number): Promise <OperationResult> {
        try {
            const promise = await axios.delete (`${this.dest_db_base_url}/checkout/${id}`);


            return {
                message: "successfully deleted",
                StatusCode: 200
                
            }
        }



        catch (error) {
            // console.log (error);
            throw new InternalServerExc ("Failed to delete");
        }
    }
        
        
        

}
