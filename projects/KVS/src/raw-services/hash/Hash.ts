import { createHash } from 'crypto';
import stringify from 'json-stable-stringify';
import { HashingServiceInterface } from '../../interfaces/raw-services/HashingService';

export class HashingService implements HashingServiceInterface {
  /**
   * Serializes data into a consistent, deterministic string format for hashing.
   * - Objects are stringified with sorted keys to ensure hash consistency.
   * - Primitives are converted to their direct string representation.
   */
  private serialize(data: any): string {
    if (typeof data === 'object' && data !== null) {
      return stringify(data) ?? "null";
    }
    // For non-objects (string, number, boolean), direct string conversion is deterministic.
    return String(data);
  }

  /**
   * Hashes the given data using the SHA-256 algorithm.
   */
  public async Hash(data: any): Promise<string> {
    const serializedData = this.serialize(data);
    return createHash('sha256').update(serializedData).digest('hex');
  }

  /**
   * Verifies if the provided data matches a given SHA-256 hash.
   */
  public async Verify(data: any, hash: string): Promise<boolean> {
    const newHash = await this.Hash(data);
    return newHash === hash;
  }
}