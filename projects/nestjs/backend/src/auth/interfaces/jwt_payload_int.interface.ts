export interface jwt_payload_int {
	role: string,
	exp: number,
	nbf: number,
	aud: string,
	sub: string,


	jti?: string,
	iat?: number,
	iss?: string
}
