# Unit I: Attacks on Computers and Computer Security

## Security Fundamentals

### Question: What is computer security?
- Protecting computer systems, networks, and data.
- Against: Unauthorized access, damage, theft, disruption.
- Goals: Ensure confidentiality, integrity, availability.

### Question: Why do we require security / passwords?
- Protect sensitive data from unauthorized viewing or modification.
- Ensure only authorized users access systems and resources.
- Maintain overall system integrity and availability.
- Prevent misuse or damage to systems.

### Question: Explain the principles of security.
- Confidentiality: Preventing unauthorized disclosure of information. (Keeping secrets secret).
- Integrity: Ensuring data and systems are not altered improperly and are trustworthy. (Accuracy and consistency).
- Availability: Ensuring authorized users can access information and resources when needed. (System is usable).
- Authentication: Verifying the identity of users or systems. (Proving who you are).
- Non-repudiation: Ensuring a party cannot deny having sent/received a message or performed an action. (Proof of origin/action).

## Security Attacks

### Question: Name types of security attacks.
- Passive Attacks: Monitoring/eavesdropping on communications. (e.g., traffic analysis, release of message contents). Difficult to detect. Focus on prevention (encryption).
- Active Attacks: Modifying data streams or creating false streams. (e.g., Masquerade, Replay, Modification of messages, Denial of Service). Difficult to prevent. Focus on detection and recovery.

## Network Security Model

### Question: Describe a model for network security and its components.
- Basic Model Elements:
    - Sender & Receiver: Principals wishing to communicate securely.
    - Message: Data being transmitted.
    - Secure Channel / Logical Path: The path information takes; assumed insecure.
    - Security Mechanisms: Encryption, Authentication, Digital Signatures, Access Control, etc. applied to protect the message.
    - Trusted Third Party (Optional): May be needed for distributing keys or verifying identities (e.g., Key Distribution Center, Certificate Authority).
    - Attacker: Threat attempting to compromise security.
- Goal: Protect information transfer from sender to receiver from attacks.

## Related Concepts

### Question: What is the problem with using default passwords?
- Widely known or easily guessable (published online, simple patterns).
- Provide easy entry point for attackers to gain unauthorized access.
- First thing attackers try when targeting systems.

### Question: What is the risk of sending passwords in plain text? / Why is it dangerous to print passwords on paper?
- Plain text transmission: Passwords can be intercepted (sniffed) over the network.
- Printed passwords: Can be lost, stolen, or viewed by unauthorized individuals, compromising account security.

### Question: Explain mobile IP. How many bits in IPv4/IPv6?
- Mobile IP: Protocol allowing mobile devices (nodes) to maintain the same IP address while moving between different networks. Facilitates seamless connectivity. Uses concepts like Home Agent, Foreign Agent, Care-of Address.
- IPv4: 32 bits.
- IPv6: 128 bits.

### Question: Wireless components?
- Basic components for wireless networking:
    - Router: Network traffic management, often includes firewall and wireless capabilities.
    - Modem: Connects network to Internet Service Provider.
    - Wireless Access Point (WAP): Allows wireless devices to connect to a wired network.
    - Antenna: Transmits and receives radio waves.
    - Wireless Network Interface Card (WNIC): Hardware in device enabling wireless connection.

# Unit II: Cryptography-Concepts and Techniques

## Basic Terminology

### Question: What is cryptography?
- Science of techniques for secure communication in the presence of adversaries.
- Involves encrypting plaintext into ciphertext and decrypting back.
- Aims to ensure confidentiality, integrity, authentication, non-repudiation.

### Question: What is plaintext and ciphertext?
- Plaintext: Original, readable message or data before encryption.
- Ciphertext: Encrypted message or data, appears unintelligible without the key.

### Question: What is a cipher? Why do we need ciphers?
- Cipher: An algorithm used for performing encryption or decryption.
- Need: To protect data confidentiality by transforming it into a form unreadable by unauthorized parties.

## Cryptographic Techniques

### Question: Explain substitution and transposition techniques.
- Substitution: Each unit of plaintext (letter, group of letters) is replaced by another unit according to a defined scheme. (e.g., Caesar cipher). Order maintained, identity changed.
- Transposition: The order of plaintext units is rearranged according to a specific permutation. Letters themselves are unchanged, position changed. (e.g., Rail Fence cipher).

### Question: What is a Caesar Cipher?
- A simple substitution cipher.
- Each letter in the plaintext is shifted a fixed number of positions down the alphabet.
- Example: Shift of 3: A -> D, B -> E, etc.

## Keys

### Question: What are the guidelines to generate keys?
- Randomness: Use cryptographically secure random number generators. Avoid predictable patterns.
- Length: Sufficient key length to resist brute-force attacks (depends on algorithm and security requirements, e.g., AES 128/256 bits).
- Protection: Secure storage and handling of keys to prevent compromise. Regular key updates (key lifecycle management).

## Steganography

### Question: What is steganography?
- The practice of concealing a secret message or data within another non-secret file or message (the cover medium).
- Goal: Hide the very existence of the secret communication. Differs from cryptography, which hides the content.
- Examples: Hiding text in image pixels, audio data, or network packets.

### Question: What are applications of steganography?
- Covert communication: Sending secret messages undetected.
- Watermarking: Embedding copyright or ownership information invisibly.
- Copyright protection: Proving ownership of digital media.

## Symmetric vs. Asymmetric Cryptography (Intro)

### Question: Compare symmetric and asymmetric key cryptography.
- Symmetric Key Cryptography:
    - Uses a single, shared secret key for both encryption and decryption.
    - Faster computation.
    - Challenge: Secure key distribution.
    - Examples: DES, AES, Blowfish, RC4.
- Asymmetric Key Cryptography (Public-Key Cryptography):
    - Uses a pair of keys: a public key (shared openly) for encryption and a private key (kept secret) for decryption.
    - Slower computation.
    - Solves key distribution problem; facilitates digital signatures.
    - Examples: RSA, Diffie-Hellman, ECC.

# Unit III: Symmetric and Asymmetric key for Ciphers

## Block Ciphers

### Question: Explain block cipher working steps.
- Plaintext is divided into fixed-size blocks (e.g., 64 bits for DES, 128 bits for AES).
- Each block is encrypted independently (in basic ECB mode) or using feedback from previous blocks (other modes like CBC, CFB, OFB).
- Encryption process typically involves multiple rounds of substitution and permutation operations, controlled by the symmetric key.
- Decryption reverses the process using the same key.

### Question: Is AES/DES a block cipher or not?
- Yes, both AES (Advanced Encryption Standard) and DES (Data Encryption Standard) are block ciphers.

## Symmetric Algorithms

### Question: What is DES? What is its use? Long form?
- Long form: Data Encryption Standard.
- What: An early, influential symmetric block cipher.
- Characteristics: Uses a 64-bit block size and a 56-bit effective key size.
- Use: Formerly widely used, now considered insecure due to the small key size making it vulnerable to brute-force attacks. Largely replaced by AES. Used to encrypt/decrypt data.

### Question: What is AES? Long form?
- Long form: Advanced Encryption Standard.
- What: Current standard symmetric block cipher, replacing DES.
- Characteristics: Uses a 128-bit block size. Key sizes can be 128, 192, or 256 bits. Operates using substitution-permutation network principles.
- Use: Widely used for secure data encryption in hardware and software (e.g., file encryption, secure connections).

### Question: Explain DES, AES, and Blowfish.
- DES: 64-bit block, 56-bit key, Feistel network structure. Outdated due to key size.
- AES: 128-bit block, 128/192/256-bit keys, Substitution-Permutation Network. Secure, efficient, current standard.
- Blowfish: 64-bit block, variable key length (32-448 bits), Feistel network. Fast, good alternative to DES, but 64-bit block size can be a limitation (use Twofish for 128-bit blocks). Royalty-free.

### Question: Give a practical example of a symmetric algorithm.
- AES (Advanced Encryption Standard) is commonly used for encrypting files on disk (e.g., BitLocker, FileVault) or securing Wi-Fi connections (WPA2/WPA3).

## Asymmetric Algorithms

### Question: What is RSA? Long form?
- Long form: Rivest-Shamir-Adleman (named after its inventors).
- What: A widely used public-key (asymmetric) cryptosystem.
- Basis: Security relies on the computational difficulty of factoring large integers.
- Use: Used for encryption (e.g., exchanging symmetric keys) and digital signatures.

### Question: Give a practical example of an asymmetric algorithm.
- RSA is used in protocols like TLS/SSL (HTTPS) to securely exchange a symmetric session key, and for creating digital signatures to verify software authenticity.

## Key Distribution

### Question: What is key distribution?
- The process of securely delivering cryptographic keys to the parties who need them to establish secure communication.
- Symmetric Key Distribution: Challenging, requires a pre-shared secret or a trusted Key Distribution Center (KDC).
- Asymmetric Key Distribution: Simpler for public keys (can be shared openly or via certificates), but private keys must remain secret. Public Key Infrastructure (PKI) often used.

# Unit IV: Message Authentication Algorithms and Hash Functions

## Hash Functions

### Question: What is a hash function?
- An algorithm that takes an arbitrary-sized input (message) and produces a fixed-size output string (hash value, message digest).
- Properties:
    - One-way: Computationally infeasible to find the input given the output (preimage resistance).
    - Collision resistant: Computationally infeasible to find two different inputs that produce the same output.
- Use: Data integrity verification, password storage, digital signatures.

## Message Authentication Codes (MAC)

### Question: What is MAC? Full form & Types.
- Full form: Message Authentication Code.
- What: A short piece of information used to authenticate a message—verifies the message came from the stated sender (authenticity) and has not been changed (integrity).
- How: Generated using a secret key shared between sender and receiver, applied to the message data (often using a hash function).
- Types:
    - HMAC (Hash-based MAC): Uses a cryptographic hash function (e.g., SHA-256) combined with a secret key. Standard, widely used.
    - CMAC (Cipher-based MAC): Uses a block cipher (e.g., AES) with a secret key.

### Question: Explain message authentication codes (MACs).
- Purpose: Provide message integrity and authentication using a shared secret key.
- Process:
    1. Sender calculates MAC value for the message using the shared secret key.
    2. Sender sends the message + MAC value to the receiver.
    3. Receiver recalculates the MAC value on the received message using the same shared secret key.
    4. If the calculated MAC matches the received MAC, the receiver verifies the message integrity and authenticity.

## Digital Signatures

### Question: What is a digital signature?
- An electronic mechanism used to demonstrate the authenticity of a digital message or document.
- Provides:
    - Authentication: Verifies the sender's identity.
    - Integrity: Verifies the data has not been altered since signing.
    - Non-repudiation: Prevents the sender from denying they sent the message.
- How: Typically created by hashing the message and then encrypting the hash with the sender's private key (asymmetric cryptography). Verified using the sender's public key.

### Question: What are the types of digital signatures?
- Classification based on level of assurance/technology (often context-dependent, e.g., EU eIDAS):
    - Basic/Simple: Basic electronic signature concept (e.g., scanned signature image). Low legal standing.
    - Advanced: Linked uniquely to signatory, capable of identifying signatory, created using data signatory controls, linked to data such that subsequent change is detectable. Uses PKI.
    - Qualified: An advanced signature created with a secure signature creation device and based on a qualified certificate. Highest legal standing in some jurisdictions.

### Question: Which software used for digital signature?
- Common examples:
    - Adobe Acrobat / Reader (for PDF documents).
    - DocuSign (cloud-based signature platform).
    - eMudhra (Certificate Authority providing digital signature solutions).
    - Government portals often integrate digital signature capabilities for official submissions.
    - Email clients (using S/MIME or PGP).

### Question: How to check the validity of documents?
- Using Digital Signatures: Verify the signature attached to the document using the sender's public key. Software (like Adobe Reader) often does this automatically, checking the signature status and the associated certificate's trust chain and validity period.
- Using Hash Verification: If a known hash value of the original document is available, recalculate the hash of the received document and compare the values. A mismatch indicates tampering.
- Checking Digital Certificates: Examine the certificate associated with the signature or website for validity period, issuer trust, and revocation status.

## Authentication Services & Standards

### Question: Describe Kerberos and X.509.
- Kerberos:
    - Network authentication protocol.
    - Provides strong authentication for client/server applications using secret-key cryptography.
    - Uses a trusted third party: Key Distribution Center (KDC), composed of Authentication Server (AS) and Ticket-Granting Server (TGS).
    - Works based on issuing 'tickets' to users, allowing them to access services without exposing passwords directly over the network. Avoids sending passwords.
- X.509:
    - A standard defining the format of public key certificates.
    - Certificates bind a public key to a specific identity (person, organization, server) and are signed by a trusted Certificate Authority (CA).
    - Foundation of Public Key Infrastructure (PKI).
    - Used in TLS/SSL (for websites), S/MIME (email), code signing, etc.

# Unit V: E-Mail Security

## Email Protocols

### Question: Which protocol is used for email & process of email/email server?
- Sending Email: SMTP (Simple Mail Transfer Protocol) is used by email clients to send emails to an email server, and between servers.
- Receiving Email:
    - POP3 (Post Office Protocol 3): Downloads emails from server to client, typically removing them from the server. Simpler.
    - IMAP (Internet Message Access Protocol): Allows clients to access and manage emails stored on the server. Synchronizes state across multiple clients. More flexible.
- Process: Client (MUA) -> Sending Server (MTA) via SMTP -> Receiving Server (MTA) via SMTP -> Mailbox -> Client (MUA) retrieves via POP3/IMAP.

## Email Security Mechanisms

### Question: What is PGP?
- Full form: Pretty Good Privacy.
- What: A popular program/standard for email encryption and digital signatures.
- How: Uses asymmetric cryptography (public/private keys) for key exchange/signatures and symmetric cryptography for encrypting the bulk message content.
- Key Management: Often relies on a decentralized "Web of Trust" model for verifying public keys, though can also use hierarchical PKI.

### Question: Explain S/MIME.
- Full form: Secure/Multipurpose Internet Mail Extensions.
- What: A standard for public key encryption and signing of MIME data (email content).
- How: Provides confidentiality (encryption), integrity and authentication (digital signatures) for emails. Uses asymmetric cryptography for signatures/key exchange and symmetric for bulk encryption.
- Key Management: Relies on a hierarchical Public Key Infrastructure (PKI) with trusted Certificate Authorities (CAs) issuing X.509 certificates to verify identities. Integrated into many modern email clients.

### Question: What is key management in email security?
- Concerns the secure generation, distribution, storage, usage, and revocation of cryptographic keys (both public/private pairs and session keys) used in PGP or S/MIME.
- Includes:
    - Generating key pairs.
    - Distributing public keys (via certificates, web of trust, key servers).
    - Protecting private keys (password protection, secure hardware).
    - Handling key expiration and revocation.

## IP Security (IPsec)

### Question: What is IPsec overview/architecture? Header, frame format?
- Overview: A suite of protocols for securing Internet Protocol (IP) communications by authenticating and/or encrypting each IP packet. Operates at the network layer (Layer 3).
- Architecture:
    - Authentication Header (AH): Provides connectionless integrity, data origin authentication, and protection against replay attacks. Does NOT provide confidentiality (no encryption).
    - Encapsulating Security Payload (ESP): Provides confidentiality (encryption), and can optionally provide integrity, authentication, and replay protection.
    - Security Associations (SA): Define the parameters (algorithms, keys, etc.) for a secure connection between two endpoints. Managed by protocols like IKE (Internet Key Exchange).
    - Modes: Transport mode (secures payload of IP packet) and Tunnel mode (secures entire IP packet by encapsulating it in a new IP packet).
- Header/Format: IPsec adds its own headers (AH or ESP) to the IP packet. The format depends on the protocol (AH/ESP) and mode (Transport/Tunnel) used. ESP includes fields for sequence numbers, initialization vectors (IV), encrypted payload, and optional authentication data. AH includes fields for sequence numbers and integrity check value.

### Question: What is an Authentication Header (AH) in IP security?
- Purpose: Provides integrity and authentication for IP packet headers and payload. Ensures data hasn't been tampered with and originates from the expected source.
- Function: Calculates an Integrity Check Value (ICV - a MAC) over parts of the IP header and the entire payload.
- Does NOT provide encryption (confidentiality).

### Question: What is Encapsulating Security Payload (ESP)?
- Purpose: Primarily provides confidentiality (encryption) for the IP payload.
- Function: Encrypts the IP payload. Can also optionally provide integrity, authentication, and anti-replay protection (features similar to AH).
- Flexibility: Can provide encryption only, authentication only, or both. Widely used due to its ability to provide confidentiality.

# Unit VI: Web Security

## Firewalls

### Question: What is the definition of a firewall?
- A network security system.
- Monitors and controls incoming and outgoing network traffic.
- Based on predetermined security rules (policies).
- Establishes a barrier between a trusted internal network and untrusted external networks (like the Internet).

### Question: What are the types of firewalls?
- Packet-Filtering Firewall: Examines packet headers (IP address, port numbers). Simple, fast. Stateless.
- Stateful Inspection Firewall: Tracks the state of active connections. Makes decisions based on connection context in addition to packet headers. More secure than packet filtering.
- Proxy Firewall (Application-Level Gateway): Acts as an intermediary for specific applications (e.g., HTTP, FTP). Inspects payload content. Can provide fine-grained control but may impact performance.
- Next-Generation Firewall (NGFW): Combines traditional firewall features with advanced capabilities like deep packet inspection (DPI), intrusion prevention (IPS), application awareness, and threat intelligence integration.

### Question: What is the purpose of a firewall in Windows?
- Built-in host-based firewall (Windows Defender Firewall).
- Protects the individual computer from network-based threats.
- Controls which applications are allowed to send/receive traffic on specific network ports.
- Blocks unsolicited incoming traffic by default.

### Question: Why isolate WLAN traffic with a firewall?
- Wireless LANs are inherently less secure due to broadcast nature.
- A firewall (often integrated into the wireless router/AP or as a separate network device) enforces security policies between the WLAN segment and other network segments (e.g., wired LAN, Internet).
- Prevents unauthorized access from wireless clients to sensitive resources.
- Can help contain threats originating from compromised wireless devices.
- Often used to create guest networks isolated from the main internal network.

## Web Connection Security

### Question: What is SSL/TLS?
- SSL (Secure Sockets Layer): Original protocol for securing web connections (HTTPS). Now largely deprecated due to vulnerabilities.
- TLS (Transport Layer Security): Successor to SSL. Current standard protocol.
- Purpose: Provide secure communication over a computer network. Ensures confidentiality (encryption), integrity (MACs), and authentication (using X.509 certificates) for connections, commonly used for HTTPS (HTTP over TLS).

### Question: How to check the authentication of a website?
- Check for HTTPS: Ensure the URL starts with "https://" and browser shows a padlock icon.
- Examine the SSL/TLS Certificate:
    - Click the padlock icon in the browser address bar.
    - Check the identity (Common Name/Subject) the certificate was issued to. Does it match the website owner?
    - Check the Issuer (Certificate Authority). Is it a trusted CA?
    - Check the certificate's validity period (not expired).
    - Look for Extended Validation (EV) certificates which provide stronger identity verification (often show organization name in address bar).

## Web Vulnerabilities & Threats

### Question: What is cross-site scripting (XSS)?
- A type of web security vulnerability.
- Allows attackers to inject malicious client-side scripts (e.g., JavaScript) into web pages viewed by other users.
- Occurs when a web application uses input from a user within the output it generates without validating or encoding it.
- Can be used to steal session cookies, deface websites, redirect users, or perform actions on behalf of the user.

## Security Management & Practices

### Question: Explain intrusion detection and its importance.
- Intrusion Detection System (IDS): A device or software application that monitors network or system activities for malicious activities or policy violations.
- Function: Detects potential intrusions and reports them (alerts) to administrators. Does not typically block traffic itself (that's IPS - Intrusion Prevention System).
- Types: Network-based (NIDS), Host-based (HIDS). Detection methods include signature-based (known patterns) and anomaly-based (deviations from normal behavior).
- Importance: Provides visibility into security events, helps identify attacks early, enables faster response, and supports forensic analysis.

### Question: Types of password? How you decide password is strong or weak?
- Types:
    - Simple Password: Easy to guess (e.g., "123456", "password", common words). Weak.
    - Complex/Strong Password: Meets specific criteria to resist guessing and brute-force attacks.
    - Graphical Password: Using images or patterns instead of text.
    - Biometric Password: Using biological traits (fingerprint, face recognition). Authentication factor, not strictly a 'password'.
    - OTP (One-Time Password): Valid for only one login session or transaction. Often used in Multi-Factor Authentication (MFA).
- Strong Password Criteria:
    - Length: Minimum length (e.g., 12+ characters often recommended, minimum 8 as per OCR).
    - Complexity: Includes a mix of character types:
        - Uppercase letters (A-Z).
        - Lowercase letters (a-z).
        - Numbers (0-9).
        - Special characters (!@#$%^&*).
    - Uniqueness: Not reused across different accounts.
    - Randomness: Avoid dictionary words, names, dates, predictable patterns.

### Question: How can we improve browser security?
- Keep Browser Updated: Apply latest security patches.
- Use Strong, Unique Passwords: Manage with a password manager.
- Enable Security Settings: Turn on phishing/malware protection, block pop-ups, control cookies/scripts.
- Install Safe Extensions: Only install extensions from trusted sources; review permissions.
- Use HTTPS Everywhere: Use browser extensions or settings to enforce HTTPS.
- Be Cautious: Avoid suspicious links/downloads, check website authenticity.
- Consider Privacy Settings: Limit tracking, clear browsing data periodically.

### Question: What is a VPN?
- Full form: Virtual Private Network.
- Purpose: Creates a secure, encrypted connection (a "tunnel") over a public network (like the Internet).
- Use Cases:
    - Secure Remote Access: Connect securely to a private network (e.g., company network) from a remote location.
    - Privacy/Anonymity: Mask your IP address and encrypt traffic, enhancing privacy from ISPs or on public Wi-Fi.
    - Bypass Geo-restrictions: Appear as if connecting from a different location.
