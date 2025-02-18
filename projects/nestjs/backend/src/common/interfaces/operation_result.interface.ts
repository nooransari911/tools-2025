export class OperationResult {
  // HTTP-Style Status codes (e.g., 200, 404, 500)
  StatusCode: number;
  
  // Response message (e.g., success or error description)
  message: string;

  // Data returned in the response (optional)
  data?: any;

}
