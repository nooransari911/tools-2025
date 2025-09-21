## Rich Key-Value Store - Part 1: The Pluggable Core & Data Foundation

### Vision & Purpose

To establish the foundational layer of the system, comprising a set of sharply defined, single-responsibility services governed by clear interfaces. This layer provides the core guarantees of data integrity, auditability, and concurrency. The architecture is designed for **maximum composability**, allowing a pure orchestrator (`KeyValueStore`) to be assembled from these independent, swappable components.

### Core Principles

1.  **Sharp Isolation & Single Responsibility:** Every component (metadata generation, hashing, locking, storage) has exactly one job and is defined by a strict interface.
2.  **Pure Orchestration:** The top-level `KeyValueStore` class contains **no implementation logic**. It is a pure orchestrator that coordinates the flow of data and calls between the specialized services it depends on.
3.  **Dependency Inversion:** The high-level orchestrator depends on abstractions (interfaces), not on concrete implementations, making the entire system pluggable and testable.
4.  **Implementation Agnosticism:** The lowest-level physical storage (`CoreStorageInterface`) is a swappable "driver," allowing the system to run on a JS `Map` or a remote C++ server without changing any other component.

### Core Data Model Interfaces

These interfaces are the universal, immutable language of the entire system.

```typescript
/**
 * Represents the unique identifier for an entry in the store. It uses a hierarchical namespace
 * for addressing, similar to a file system path.
 */
export interface StoreKeyInterface {
  Key: string;
  Namespace?: string[];
}

/**
 * The foundational metadata properties shared by both the current state and historical revisions.
 */
export interface BaseMetadataInterface {
  Version: number;
  ModifiedBy?: string | number;
  DataHash: string;
  SchemaHash?: string;
}

/**
 * An immutable snapshot of an entry's metadata at a specific point in its history.
 */
export interface HistoricalMetadataInterface extends BaseMetadataInterface {
  Timestamp: number;
  Comment?: string;
}

/**
 * The full, "living" metadata for the current state of an entry.
 */
export interface MetadataInterface extends BaseMetadataInterface {
  CreatedAt: number;
  UpdatedAt: number;
  ExpiresAt?: number;
  Tags: string[];
  RevisionHistory: HistoricalMetadataInterface[];
}

/**
 * The fundamental data envelope stored for every key in the system.
 */
export interface KvsEntryInterface<T = any> {
  Value: T;
  Metadata: MetadataInterface;
}
```

### Core Service Interfaces

Each component is defined by a precise contract.

```typescript
/**
 * The physical persistence layer contract. A "dumb" driver for atomic operations.
 */
export interface CoreStorageInterface {
  Get<T>(serializedKey: string): Promise<KvsEntryInterface<T> | undefined>;
  Set<T>(serializedKey: string, entry: KvsEntryInterface<T>): Promise<void>;
  Delete(serializedKey: string): Promise<boolean>;
  Keys(): Promise<string[]>;
}

/**
 * A pure, stateless service for creating cryptographic fingerprints of data.
 */
export interface HashingServiceInterface {
  CalculateDataHash(value: any): Promise<string>;
}

/**
 * The logic engine for all metadata business rules. It takes a proposed change
 * and the previous state, and returns only the new, updated metadata.
 */
export interface MetadataServiceInterface {
  /**
   * Generates the complete metadata for an entry being created for the first time.
   * @param dataHash The hash of the initial value.
   * @param options User-provided metadata for the initial version.
   * @returns A promise resolving to the complete, new MetadataInterface.
   */
  GenerateNewMetadata(
    dataHash: string,
    options: { ModifiedBy?: string | number; Comment?: string; Tags?: string[] }
  ): Promise<MetadataInterface>;

  /**
   * Generates the next version of metadata based on the previous state.
   * @param previousMetadata The complete metadata of the existing entry.
   * @param newHash The hash of the new value.
   * @param options User-provided metadata for the new version.
   * @returns A promise resolving to the complete, updated MetadataInterface.
   */
  GenerateNextVersion(
    previousMetadata: MetadataInterface,
    newHash: string,
    options: { ModifiedBy?: string | number; Comment?: string; Tags?: string[] }
  ): Promise<MetadataInterface>;
}

/**
 * The concurrency guardian. Provides a method to execute an asynchronous
 * operation within a namespace-level lock.
 */
export interface LockManagerInterface {
  WithLock<T>(namespacePath: string, operation: () => Promise<T>): Promise<T>;
}

/**
 * A utility service for managing the StoreKeyInterface.
 */
export interface KeyServiceInterface {
  /**
   * Serializes a StoreKeyInterface object into a deterministic string format.
   * @param key The StoreKeyInterface object.
   * @returns The flattened string key (e.g., 'users/active:123').
   */
  Serialize(key: StoreKeyInterface): string;

  /**
   * Parses a serialized key string back into a StoreKeyInterface object.
   * @param serializedKey The flattened string key.
   * @returns The structured StoreKeyInterface object.
   */
  Parse(serializedKey: string): StoreKeyInterface;
}
```

### The `KeyValueStore` (Pure Orchestrator)

The `KeyValueStore` is a simple, high-level class that is assembled from the service implementations. It owns the flow control but delegates all the work.

**Dependencies (Injected via Constructor):**
-   `coreStorage: CoreStorageInterface`
-   `metadataService: MetadataServiceInterface`
-   `hashingService: HashingServiceInterface`
-   `lockManager: LockManagerInterface`
-   `keyService: KeyServiceInterface`

**Responsibilities:**
-   Provide the clean, public-facing API (`Get`, `Set`, `Delete`).
-   **For a `Set` operation, it executes a pure sequence of calls to its injected services, containing no business logic of its own.**

### Core Operation Flow: A `Set` Mutation (The Orchestration)

This flow now perfectly illustrates the sharp separation of concerns.

1.  Application calls the public method: `kvs.Set(storeKey, newValue, options)`.
2.  The `KeyValueStore` orchestrator begins.
3.  It delegates to the `KeyService` to get the storable key: `const serializedKey = this.keyService.Serialize(storeKey)`.
4.  It delegates to the `LockManager`: `this.lockManager.WithLock(serializedKey_namespace_part, async () => { ... })`.
5.  **Inside the lock's callback, the orchestration continues:**
    a. It delegates to `CoreStorage` to get the current state: `const oldEntry = await this.coreStorage.Get(serializedKey)`.
    b. It delegates to the `HashingService` to fingerprint the new data: `const newHash = await this.hashingService.CalculateDataHash(newValue)`.
    c. **Decision Point & Metadata Delegation:**
        -   If `oldEntry` exists, it delegates to the `MetadataService` to generate the updated metadata: `const newMetadata = await this.metadataService.GenerateNextVersion(oldEntry.Metadata, newHash, options)`.
        -   If `oldEntry` does not exist, it delegates to generate the initial metadata: `const newMetadata = await this.metadataService.GenerateNewMetadata(newHash, options)`.
    d. **Final Assembly (Orchestrator's Responsibility):** The orchestrator now performs its one simple assembly task:
        ```typescript
        const newEntry: KvsEntryInterface = {
            Value: newValue,
            Metadata: newMetadata
        };
        ```
    e. It delegates to `CoreStorage` to persist the final, assembled result: `await this.coreStorage.Set(serializedKey, newEntry)`.
6.  The lock is released, and the operation's `Promise` resolves, returning the `newEntry` to the caller.

This architecture is now a pristine example of Dependency Inversion and the Single Responsibility Principle. The `KeyValueStore` is a readable, high-level script, and every complex piece of logic is isolated within a dedicated, testable, and swappable service.

## Reactive Key-Value Store - Part 2: Core Extensions & Application Integration

### Vision & Purpose

To layer the essential application-facing services on top of the high-integrity core. This layer introduces the "batteries-included" functionality required for modern software development: a powerful event system for reactivity, structured logging for observability, a seamless React integration for UI development, and utilities for interacting with external systems.

These extensions are designed as decorators or consumers of the core `KeyValueStore` orchestrator, ensuring the core's principles of isolation and purity are never violated.

### Core Extensions Architecture

This diagram illustrates how the new services wrap or consume the core from Part 1. The application interacts with the outermost layer, which adds behavior before delegating to the inner, pure orchestrator.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Application Layer                        │
│                (e.g., React Components & Hooks)                 │
└─────────────────────────────────────────────────────────────────┘
                                ▲
                                │ (Consumes Events)
┌─────────────────────────────────────────────────────────────────┐
│                 EventfulKeyValueStore (Decorator)              │
│      (Implements KeyValueStoreInterface, emits events)          │
├─────────────────────────────────────────────────────────────────┤
│                 LoggingKeyValueStore (Decorator)               │
│      (Implements KeyValueStoreInterface, adds logging)          │
├─────────────────────────────────────────────────────────────────┤
│                 KeyValueStore (Pure Orchestrator)              │
│                  (The final, unmodified core from Part 1)       │
└─────────────────────────────────────────────────────────────────┘
```

### Core Extension Interfaces

These contracts define the functionality of the new, higher-level services.

```typescript
/**
 * The primary, high-level interface for the entire KVS system that
 * application code will interact with. All decorators and the core
 * orchestrator implement this contract.
 */
export interface KeyValueStoreInterface {
  Get<T>(key: StoreKeyInterface): Promise<KvsEntryInterface<T> | undefined>;
  Set<T>(key: StoreKeyInterface, value: T, options?: { ModifiedBy?: string | number; Comment?: string; Tags?: string[] }): Promise<KvsEntryInterface<T>>;
  Delete(key: StoreKeyInterface): Promise<boolean>;
}

/**
 * The pub/sub engine for broadcasting state changes.
 */
export interface EventServiceInterface {
  /**
   * Emits an event to all interested subscribers.
   * @param eventName A namespaced event name (e.g., 'users/active:123').
   * @param payload The rich event data.
   */
  Emit(eventName: string, payload: KvsEventPayloadInterface): void;

  /**
   * Subscribes a listener to a specific key or a wildcard pattern.
   * @param pattern The pattern to subscribe to (e.g., 'users/#').
   * @param listener The callback function to execute.
   * @returns An unsubscribe function.
   */
  Subscribe(pattern: string, listener: (payload: KvsEventPayloadInterface) => void): () => void;
}

/**
 * The payload for every event emitted by the system.
 */
export interface KvsEventPayloadInterface {
  StoreKey: StoreKeyInterface;
  SerializedKey: string;
  Operation: 'set' | 'delete';
  NewEntry?: KvsEntryInterface<any>; // The state after the change
  PreviousEntry?: KvsEntryInterface<any>; // The state before the change
}

/**
 * The observability layer for logging store operations.
 */
export interface LoggingServiceInterface {
  LogStart(operation: string, key: StoreKeyInterface): string; // Returns a transaction ID
  LogEnd(transactionId: string, result: { success: boolean; error?: Error }): void;
}

/**
 * A utility for creating coarse-grained payloads from fine-grained state.
 */
export interface PayloadFormationServiceInterface {
  CreatePayload<T extends Record<string, any>>(mapping: Record<keyof T, StoreKeyInterface>): Promise<T>;
}
```

### Core Extension Components

#### 1. The Decorator Pattern

To maintain the purity of the core `KeyValueStore` orchestrator, new cross-cutting concerns like logging and eventing are added via **Decorators**. A decorator is a wrapper class that implements the same `KeyValueStoreInterface` as the core. It adds its specific behavior (e.g., logging) and then calls the corresponding method on the inner "wrapped" instance. This allows us to compose a fully-featured store from discrete, single-responsibility layers.

#### 2. Event System (The Reactive Engine)

This is the pub/sub engine that powers all real-time functionality. An `EventfulKeyValueStore` decorator wraps the core orchestrator.

-   **Operation:** After the inner orchestrator's `Set` or `Delete` method successfully completes, the decorator's `Set` method calls `eventService.Emit()`.
-   **Rich Payloads:** The emitted event payload is rich with context, containing the `StoreKey`, the complete `NewEntry`, and the `PreviousEntry`. This gives subscribers all the information they need without requiring them to make a follow-up `Get` call.
-   **Hierarchical Subscriptions:** The service supports expressive, hierarchical wildcard subscriptions (e.g., `users/active/#` or `users/+/settings`), leveraging the `Namespace` in the `StoreKeyInterface`.

#### 3. Logging System (The Observer)

This provides structured, queryable logs. A `LoggingKeyValueStore` decorator wraps the core (or the eventful) orchestrator.

-   **Operation:** The decorator's `Set` method calls `logger.LogStart()` before delegating to the inner instance. In a `try/catch/finally` block, it calls `logger.LogEnd()` with the outcome (success or failure), allowing it to calculate and record the operation's duration.

#### 4. React Integration Layer (The UI Bridge)

This layer provides a set of React hooks that create a seamless bridge between the KVS and the UI. It is the primary **consumer** of the `EventServiceInterface`.

-   **`useKVSValue(key: StoreKeyInterface)`:** The main reactive hook. It uses React's `useSyncExternalStore` hook, which is purpose-built for subscribing to external stores.
    -   The `subscribe` function passed to `useSyncExternalStore` is simply a call to `eventService.Subscribe()`.
    -   The `getSnapshot` function is a call to the core `keyValueStore.Get()`.
-   **Version-Aware Reconciliation:** This is the critical mechanism that guarantees UI consistency. When a hook's event listener is triggered, it performs a check: `if (event.NewEntry.Metadata.Version > displayedVersion)`. This simple, robust check prevents stale data overwrites and optimizes re-renders, as it only triggers a UI update if the incoming event is definitively newer than what is currently displayed.

#### 5. Payload Formation Utility (The Data Aggregator)

This is a standalone service that decouples fine-grained application state from coarse-grained external data models.

-   **Operation:** A developer defines a mapping object that declares which `StoreKeyInterface` in the KVS corresponds to which field in a target payload. The `CreatePayload` method then asynchronously fetches all required values and assembles the final object, ready to be sent to a database or external API.

### Updated Operation Flow: A Reactive `Set` Mutation

This flow shows the "call stack" through the decorated layers.

1.  Application code (e.g., a React component) calls `kvs.Set(storeKey, newValue)`. The `kvs` instance here is the outermost decorator (`EventfulKeyValueStore`).
2.  The `EventfulKeyValueStore.Set` method is invoked. It wraps the core logic in a `try/catch`.
3.  It calls the `Set` method of the instance it wraps, the `LoggingKeyValueStore`.
4.  The `LoggingKeyValueStore.Set` method is invoked. It calls `logger.LogStart()` to get a transaction ID.
5.  It calls the `Set` method of the instance it wraps, the **pure `KeyValueStore` orchestrator from Part 1**.
6.  **The core orchestrator executes the entire logical flow from Part 1:** locking, fetching the old entry, delegating to the `MetadataService`, assembling the final `KvsEntry`, and persisting it via the `ICoreStorage`. It then returns the successful `newEntry`.
7.  Control returns to the `LoggingKeyValueStore`. It calls `logger.LogEnd()` with the success status and the transaction ID. It passes the `newEntry` result up the chain.
8.  Control returns to the `EventfulKeyValueStore`. It now has the final `newEntry` and the `oldEntry`. It constructs a rich `KvsEventPayloadInterface` and calls `eventService.Emit()`.
9.  The `EventService` broadcasts the event to all subscribers, including the `useKVSValue` hooks, which then perform their version-aware reconciliation.
10. The `EventfulKeyValueStore` returns the `newEntry` result, and the top-level promise resolves.




## Reactive Key-Value Store - Part 3: Optional Distributed Extensions

### Vision & Purpose

To provide a set of powerful, opt-in extensions that elevate the single-environment KVS into a distributed, multi-environment data platform. These extensions address the challenges of formal data validation, real-time client-server state synchronization, and persistent database integration.

These are not core features; they are plugins, decorators, or separate layers that an application can adopt when its requirements scale. They are designed to integrate seamlessly with the existing `KeyValueStoreInterface`, ensuring that application logic remains consistent whether operating in a local or distributed context.

### Optional Extensions Architecture

This diagram illustrates how the new layers integrate with the architecture from Part 2. The `SyncLayer` acts as a specialized decorator on the client and a message handler on the server, while the `SchemaPlugin` and `DatabaseAdapter` function as powerful middleware within the server's operation flow.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Client Environment                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │               Client KVS (Decorated Stack)              │    │
│  │   (Adds SyncClient & OfflineQueue to the Part 2 stack)  │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                │
                         Sync Protocol
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    Server Environment                           │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                Server KVS (Decorated Stack)             │    │
│  │(Integrates SyncBroadcaster, SchemaPlugin, DB Adapter)   │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Optional Extension Components & Interfaces

#### 1. Schema Validation Plugin (The Integrity Guardian)

This plugin introduces a formal contract layer for your data, providing verifiably correct data shapes. It is implemented as middleware that hooks into the server-side `KeyValueStore`'s orchestration flow.

-   **Schemas-as-Data:** Schemas (e.g., JSON Schema, Zod definitions) are stored as versioned entries in a reserved `__schema` namespace.
-   **Content-Addressed Schemas:** Data entries link to their schema via an immutable `SchemaHash` in their `BaseMetadataInterface`. This cryptographic link guarantees that data is always validated against the one and only correct schema definition.
-   **Two-Way Integrity Gate:**
    1.  **On `Set` (Ingress Validation):** It intercepts write operations. If a `SchemaHash` is present, it validates the incoming `Value`. If the data does not conform, the operation is rejected, guaranteeing no malformed data is ever persisted.
    2.  **On `Get` (Egress Validation & Transformation):** It intercepts read operations. If the stored data's `SchemaHash` doesn't match what the application expects, it can trigger a **lazy migration**, safely upgrading the data to the new shape before returning it. This ensures the application *never* receives data in an unexpected format.

```typescript
interface SchemaValidationServiceInterface {
  /**
   * Validates a value against a schema referenced by its hash.
   * Throws a validation error if the value does not conform.
   */
  Validate(value: any, schemaHash: string): Promise<void>;
}
```

#### 2. Synchronization Layer (The Distributed State Engine)

This layer transforms the KVS into a distributed system that achieves eventual consistency across multiple environments. It consists of a client-side and a server-side component.

-   **Client-Side `SyncKeyValueStore` Decorator:**
    -   **Optimistic Updates:** This decorator immediately applies mutations to the local store for instant UI feedback.
    -   **Offline Queuing:** It wraps the core `Set` operation. After the local `Set` succeeds, it adds the mutation details (the key, new value, and resulting entry) to an `OfflineQueue`. This queue persists changes even if the user closes the browser.
    -   **Sync Client:** A `SyncClient` service runs in the background, consuming from the `OfflineQueue` and sending the changes to the server via a pluggable transport (e.g., WebSocket). It also listens for incoming updates from the server and applies them to the local store.

-   **Server-Side `SyncMessageHandler`:**
    -   **Message Handling:** This is the server's entry point for client changes. It listens for incoming messages from the sync transport.
    -   **Coordination:** Upon receiving a mutation from a client, it invokes the server's core `KeyValueStore.Set` method. All the server-side logic (locking, validation, persistence) is executed here.
    -   **Broadcasting:** After the server's `Set` operation is successful, it uses an `EventServiceInterface` (from Part 2) to broadcast the final, authoritative `KvsEntry` to all other connected clients. This is how state converges.

-   **Conflict Resolution:** This is a critical responsibility of the server-side `KeyValueStore`. When it receives a client mutation, it compares the `Version` number in the client's payload with the `Version` currently in its storage. If they don't align, a conflict has occurred, and it is resolved using a configured strategy (e.g., Last-Write-Wins).

#### 3. Database Integration Layer (The Persistence Bridge)

This is a server-side extension that provides a seamless, optional bridge between the KVS and an external database. It's implemented as a "subscriber" that reacts to successful KVS changes.

-   **Adapter-Based Architecture:** Pluggable `DatabaseAdapterInterface` implementations (`PostgreSQLAdapter`, `MongoDBAdapter`, etc.) translate KVS data into the native format of the target database.
-   **Asynchronous Persistence:** The integration layer subscribes to the server's `EventServiceInterface`. When a `set` or `delete` event occurs for a monitored namespace, it triggers the persistence logic. This decouples the core write operation from the database write, ensuring the KVS remains fast.
-   **Bidirectional Sync:**
    1.  **KVS -> DB:** An event from the KVS triggers the adapter to perform an `INSERT` or `UPDATE`, often using the **Payload Formation Service** from Part 2 to build the database record.
    2.  **DB -> KVS:** An external change to the database (e.g., from another microservice) can be detected via database triggers or a change data capture (CDC) stream. This external event is fed into a handler that calls the server's `KeyValueStore.Set`, which in turn broadcasts the change to all connected clients.

### Multi-Environment Operation Flow: A Client Write

This flow demonstrates how all layers work in concert.

1.  A user action in the client application triggers `kvs.Set(storeKey, newValue, { SchemaHash: 'user-v2-hash' })`. The `kvs` instance is the fully decorated stack.
2.  The `SyncKeyValueStore` decorator immediately calls the inner `Set` method.
3.  The core logic (from Part 1 & 2) executes locally: locking, logging, metadata generation, and saving to the client's `ICoreStorage` (e.g., IndexedDB). **The UI re-renders instantly.**
4.  After the local `Set` succeeds, the `SyncKeyValueStore` decorator adds the mutation details to the `OfflineQueue`.
5.  The `SyncClient` picks up the mutation and sends it to the Server via WebSocket.
6.  The server's `SyncMessageHandler` receives the payload.
7.  It invokes the server's `kvs.Set` method.
8.  **The server's `SchemaPlugin` middleware intercepts the call and validates the `newValue` against its `SchemaHash`. If it fails, an error is sent back to the client.**
9.  The server's core orchestrator executes its full logical flow, resolving any version conflicts and persisting the final authoritative `KvsEntry` to its `ICoreStorage` (e.g., a C++ proxy).
10. **The server's `EventServiceInterface` emits an event for the successful mutation.**
11. **The `DatabaseAdapter`, subscribed to this event, receives it, uses the Payload Formation service to build a database record, and persists the change to PostgreSQL.**
12. **The `SyncBroadcaster`, also subscribed to this event, sends the final, authoritative `KvsEntry` to all connected clients.**
13. The original client receives this broadcast. Its `SyncClient` applies the update, and its UI reconciles the state, ensuring it converges with the server's source of truth.
