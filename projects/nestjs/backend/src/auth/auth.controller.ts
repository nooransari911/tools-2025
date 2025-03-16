import { Body, Controller, Get, Post, Query } from '@nestjs/common';
import { AuthService } from './auth.service';
import { jwt_payload_int } from './interfaces/jwt_payload_int.interface';
import { OperationResult } from 'src/common/interfaces/operation_result.interface';

@Controller('auth')
export class AuthController {
    constructor (private authservice: AuthService) {}




    @Post ('show-token')
    async function_show_token (
        @Body () jwt_token: {
            token: string
        }
    ) {
        return this.authservice.gen_verify_html (jwt_token.token);
    }




    @Get ('show-token-query')
    async function_show_token_query (
        @Query ('jwt') jwt: string 
    ) {
        const jwt_obj = JSON.parse (jwt);
        return this.authservice.gen_verify_html (jwt_obj.token);
    }





    @Post ('gen-token')
    async function_gen_token (
        @Body () body: {
            role: string,
            aud:  string,
            sub:  string
        }
    ) {
        // const role = "production";
        // const audience = "hostel";
        // const userid = "my-user-id";
        const body_role = body.role ?? 'production'; // Default value for 'role'
        const body_audience = body.aud ?? 'hostel'; // Default value for 'audience'
        const body_userid = body.sub ?? 'my-user-id'; // Default value for 'userid'



        const jwt_payload = await this.authservice.gen_payload (
            body_role,
            body_audience,
            body_userid
        )



        const jwt = this.authservice.sign_payload (jwt_payload);


        return jwt;
    }


    @Post ('verify-token')
    async function_verify_token (
        @Body () jwt_token: {
            token: string
        }
    ): Promise <OperationResult> {

        // console.log('Received jwt_token:', jwt_token); // Add this line
        // console.log('Type of jwt_token:', typeof jwt_token); // Add this line

        const validate: OperationResult = await this.authservice.verify_payload (jwt_token.token);

        return validate;
    }


    @Post ('test-token')
    async function_test_token (
        @Body () body: Partial <jwt_payload_int>
    ) {
        return this.authservice.gen_verify (body);
    }

}
