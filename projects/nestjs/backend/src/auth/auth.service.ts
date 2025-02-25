import { Injectable } from '@nestjs/common';
import { jwt_payload_int } from './interfaces/jwt_payload_int.interface';
import { JwtService } from '@nestjs/jwt';
import { OperationResult } from 'src/common/interfaces/operation_result.interface';
import axios from 'axios';

@Injectable()
export class AuthService {
    public readonly token_expire_in = (10);


    public success_str                 : string    = "successful";
    public success_code                : number    = 200;

    public unauthorized_str            : string    = "unauthorized";
    public unauthorized_code           : number    = 401;

    public self_base_url = "http://localhost:3000";




    public token_html_string = `
        <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>JWT Decoder</title>
                <style>
                    body {
                        background-color: black;
                        color: white;
                        font-family: 'Courier New', Courier, monospace;
                    }
                    #container {
                        background-color: black;
                        color: white;
                        font-family: 'Courier New', Courier, monospace;
                    }
                </style>
            </head>
            <body>
    `



    constructor (private jwtservice: JwtService) {}




    async gen_payload (
        role: string,
        audience: string,
        userid: string
    ): Promise <Partial <jwt_payload_int>> {
        const jti = crypto.randomUUID ();
        // const now = Math.floor(Date.now() / 1000);

        return {
            role: role,
            aud: audience,
            sub: userid,
            iss: 'nestjs-auth-service',
            jti: jti
        }
    }







    
    async sign_payload (payload: Partial <jwt_payload_int>): Promise <string> {
        const now = Math.floor(Date.now() / 1000);

        payload.iat = now;
        // payload.exp = now + (this.token_expire_in);
        payload.nbf = now;

        return this.jwtservice.sign (payload, {
            algorithm: 'RS256'
        });
    }





    async verify_payload (jwt_string: string): Promise <OperationResult> {
        try {
            const verify = this.jwtservice.verify <jwt_payload_int> (jwt_string, {
                algorithms: ['RS256'],
                ignoreExpiration: false, // MUST be false to enforce expiration

            });
            return {
                message: this.success_str,
                StatusCode: this.success_code
            }
        }


        catch (error) {
            return {
                message: this.unauthorized_str,
                StatusCode: this.unauthorized_code,
                data: error
            }
        }
    }





    async gen_verify (payload: Partial <jwt_payload_int>): Promise <OperationResult> {
        const token = await this.sign_payload (payload);
        const opres = await this.verify_payload (token);



        return opres;
    }




    async gen_verify_html (token: string): Promise <string> {
        const [encodedHeader, encodedPayload, signature] = token.split('.');

        const header = JSON.parse(Buffer.from(encodedHeader, 'base64').toString('utf8'));
        const payload = JSON.parse(Buffer.from(encodedPayload, 'base64').toString('utf8'));


        const div_str = `
            <div class="container">

                <h1>Decoded JWT Header</h1>
                <pre>${JSON.stringify (header, null, 2)}</pre>
                <h1>Decoded JWT Payload</h1>
                <pre>${JSON.stringify (payload, null, 2)}</pre>

                <h1>Decoded JWT Signature</h1>
                <pre>${JSON.stringify (signature, null, 2)}</pre>

            </div>
            </body>
            </html>


        `




        return this.token_html_string + div_str;



    }
}
