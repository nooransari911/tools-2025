import { Module } from '@nestjs/common';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtModule } from '@nestjs/jwt';
import * as fs from 'fs';



@Module({
    imports: [
        JwtModule.register({
            privateKey: fs.readFileSync('./private/private_key.pem'),  // Load private key
            publicKey: fs.readFileSync('./private/public_key.pem'),  // Load public key
            signOptions: { algorithm: 'RS256', expiresIn: '20s' }, // Use RS256 (RSA+SHA) for signing; You can also use ES256 (ECC P-256 (eq to RSA3072)+SHA-256)
    }),
    ],
    controllers: [AuthController],
    providers: [AuthService],
    exports: [AuthService]
})
export class AuthModule {}
