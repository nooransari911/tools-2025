import { KvsKeyInterface } from "../../interfaces/core/Key/KvsKeyInterface";
import { KeyServiceInterface } from "../../interfaces/raw-services/KeyService";



export class KeyService implements KeyServiceInterface {
  private readonly NAMESPACE_SEPARATOR = '/';
  private readonly FILE_SEPARATOR = ':';

  /**
   * Encodes a KvsKeyInterface object into a single string representation.
   * Format: "Namespace1/Namespace2:File"
   */
  public Encode(key: KvsKeyInterface): string {
    if (!key.Namespace || key.Namespace.length === 0) {
      return key.File;
    }

    const namespacePath = key.Namespace.join(this.NAMESPACE_SEPARATOR);
    return `${namespacePath}${this.FILE_SEPARATOR}${key.File}`;
  }

  /**
   * Decodes a key string back into a KvsKeyInterface object.
   */
  public Decode(keyString: string): KvsKeyInterface {
    const lastSeparatorIndex = keyString.lastIndexOf(this.FILE_SEPARATOR);

    if (lastSeparatorIndex === -1) {
      return { File: keyString };
    }

    const namespacePath = keyString.substring(0, lastSeparatorIndex);
    const file = keyString.substring(lastSeparatorIndex + 1);

    if (namespacePath === "") {
        return { File: file };
    }

    const namespace = namespacePath.split(this.NAMESPACE_SEPARATOR);
    return { Namespace: namespace, File: file };
  }

  /**
   * Parses a KvsKeyInterface object into an array of its path components.
   * @returns An array like ['Namespace1', 'Namespace2', 'File']
   */
  public Parse(key: KvsKeyInterface): string[] {
    const pathParts = [...(key.Namespace || [])];
    pathParts.push(key.File);
    return pathParts;
  }
}