# Unit I: Attacks on Computers and Computer Security

## Computer Security Fundamentals

### Question: What is computer security? Why do we require passwords?
- Computer Security Definition:
    - Protecting computer systems and data.
    - Protection from: Damage, theft, unauthorized access.
- Need for Passwords:
    - Protect sensitive data.
    - Ensure only authorized users access systems.
    - Maintain overall system security and accountability.

## Principles of Security

### Question: Explain the principles of security.
- Core Principles (CIA Triad +):
    - Confidentiality: Keep data secret, prevent unauthorized disclosure.
    - Integrity: Keep data correct and unchanged, prevent unauthorized modification.
    - Availability: Ensure data and services are accessible to authorized users when needed.
    - Authentication: Confirm the identity of users or systems.
    - Non-repudiation: Prove that a specific action (like sending a message) was taken by a specific entity, preventing denial.

## Security Attacks

### Question: Name two types of security attacks.
- Passive Attacks:
    - Goal: Observe or monitor transmissions.
    - Examples: Eavesdropping, traffic analysis (spying on data).
    - Difficult to detect.
- Active Attacks:
    - Goal: Modify data stream or create false stream.
    - Examples: Masquerade, replay, modification of messages, denial of service (changing data).
    - Easier to detect.

## Network Security Model

### Question: Describe a model for network security & its components.
- Basic Model Components:
    - Sender: Originator of the message.
    - Receiver: Intended recipient of the message.
    - Message: Data being transmitted.
    - Channel: Medium used for transmission.
    - Security Mechanisms: Methods applied to protect the message (e.g., encryption, authentication).
        - Encryption Algorithm: Used by sender.
        - Decryption Algorithm: Used by receiver.
        - Key: Secret information used by algorithms.
    - Secure Path: Logical path between sender and receiver ensuring security services.
- Purpose: To provide secure communication by applying security services (Confidentiality, Integrity, etc.) using security mechanisms, protecting against threats over the channel.

# Unit II: Cryptography-Concepts and Techniques

## Core Cryptography Concepts

### Question: What is cryptography? What is plaintext and ciphertext? What is encryption and decryption?
- Cryptography:
    - Science of secret communication.
    - Techniques for securing information, primarily through codes and ciphers.
- Plaintext:
    - Original, readable message or data.
- Ciphertext:
    - Encrypted, unreadable message or data (secret coded text).
- Encryption:
    - Process of converting plaintext into ciphertext using an algorithm and a key.
- Decryption:
    - Process of converting ciphertext back into plaintext using an algorithm and a key.

### Question: What is a cipher? Why do we need ciphers?
- Cipher:
    - An algorithm used for performing encryption or decryption.
- Need for Ciphers:
    - To protect data confidentiality from unauthorized access during transmission or storage.
    - To ensure data integrity and authenticity.

## Cryptographic Techniques

### Question: Explain substitution and transposition techniques. What is a Caesar Cipher?
- Substitution Techniques:
    - Replace plaintext elements (letters, bits) with other elements.
    - Key determines the specific mapping.
    - Example: Caesar Cipher.
        - Each letter shifted by a fixed number of positions down the alphabet (e.g., shift 3: A -> D, B -> E).
- Transposition Techniques:
    - Rearrange the order of plaintext elements.
    - Letters themselves are not changed, only their positions.
    - Key determines the permutation rule.
    - Example: Rail Fence Cipher.

## Symmetric vs. Asymmetric Cryptography

### Question: Compare symmetric and asymmetric key cryptography.
- Symmetric Key Cryptography:
    - Uses a single, shared secret key for both encryption and decryption.
    - Key must be securely exchanged beforehand.
    - Algorithms: DES, AES, RC4, Blowfish.
    - Advantage: Generally faster.
    - Disadvantage: Secure key distribution is challenging.
- Asymmetric Key Cryptography (Public-Key Cryptography):
    - Uses a pair of keys: a public key and a private key.
    - Public key: Shared openly, used for encryption (or verifying signatures).
    - Private key: Kept secret by the owner, used for decryption (or creating signatures).
    - Algorithms: RSA, Diffie-Hellman, ECC.
    - Advantage: Solves key distribution problem for confidentiality; enables digital signatures.
    - Disadvantage: Generally slower than symmetric algorithms.

## Steganography

### Question: What is steganography? What are its applications?
- Steganography Definition:
    - Practice of hiding secret data within other non-secret files or messages (the "cover" medium).
    - Goal: Conceal the very existence of the secret communication.
    - Examples: Hiding text in image pixels, audio data, or network packet headers.
- Applications:
    - Covert communication (hiding messages).
    - Watermarking (embedding copyright or ownership information).
    - Copyright protection.

# Unit III: Symmetric and Asymmetric key for Ciphers

## Symmetric Key Algorithms (Block Ciphers)

### Question: Explain DES, AES, and Blowfish. Are AES/DES block ciphers?
- Block Cipher Definition:
    - Encrypts data in fixed-size blocks using a symmetric key.
    - Yes, DES and AES are block ciphers.
- Block Cipher Working Steps:
    1. Plaintext is divided into fixed-size blocks (e.g., 64 bits for DES, 128 bits for AES).
    2. Each block is encrypted independently (in basic ECB mode) or dependently (other modes like CBC) using the symmetric key and the algorithm's rounds of substitution and permutation.
    3. Resulting ciphertext blocks are combined.
- DES (Data Encryption Standard):
    - Block Size: 64 bits.
    - Key Size: 56 bits (effectively).
    - Status: Considered outdated and insecure due to small key size (vulnerable to brute-force).
    - Use: Legacy systems, educational purposes.
- AES (Advanced Encryption Standard):
    - Block Size: 128 bits.
    - Key Sizes: 128, 192, or 256 bits.
    - Status: Current standard, widely used, considered secure and efficient.
    - Faster and more secure than DES.
- Blowfish:
    - Block Size: 64 bits.
    - Key Size: Variable, 32 to 448 bits.
    - Status: Secure, fast, especially good for applications where the key doesn't change often (e.g., file encryption). Royalty-free.

## Asymmetric Key Algorithms

### Question: What is RSA?
- RSA (Rivest-Shamir-Adleman):
    - Widely used public-key (asymmetric) algorithm.
    - Basis: Mathematical difficulty of factoring large numbers (product of two large primes).
    - Uses: Encryption/Decryption, Digital Signatures, Key Exchange.
    - Operation: Involves a public key (exponent `e`, modulus `n`) and a private key (exponent `d`, modulus `n`).

## Key Generation and Distribution

### Question: What is key distribution? What are guidelines to generate keys?
- Key Distribution:
    - Process of securely delivering cryptographic keys to the parties who need them.
    - Critical challenge for symmetric cryptography (requires secure channel).
    - Simplified in asymmetric cryptography (public keys can be shared openly, private keys kept secret).
- Key Generation Guidelines:
    - Randomness: Use cryptographically secure pseudo-random number generators (CSPRNGs). Avoid predictable patterns.
    - Key Length: Use a sufficiently long key size based on the algorithm and required security level (e.g., AES 128/256 bits, RSA 2048/3072 bits).
    - Key Storage: Protect keys securely (e.g., hardware security modules (HSMs), encrypted storage, proper access controls). Avoid hardcoding keys.

# Unit IV: Message Authentication Algorithms and Hash Functions

## Hash Functions

### Question: What is a hash function?
- Hash Function Definition:
    - An algorithm that takes an input message of any size and produces a fixed-size output, called a hash value, message digest, or fingerprint.
- Properties:
    - One-way: Computationally infeasible to find the input message given only the hash value (preimage resistance).
    - Collision Resistance: Computationally infeasible to find two different messages that produce the same hash value.
    - Deterministic: The same input message always produces the same hash output.
- Use: Primarily for data integrity verification. Also used in password storage, digital signatures, MACs.
- Examples: SHA-256, SHA-3, MD5 (insecure).

## Message Authentication Codes (MACs)

### Question: Explain message authentication codes (MACs). What are common types?
- MAC Definition:
    - A short piece of information used to authenticate a message.
    - Verifies both data integrity (message wasn't changed) and authenticity (message came from the expected sender).
- How it works:
    - Generated using the message content and a shared secret key between sender and receiver.
    - Sender computes MAC, appends it to message.
    - Receiver recomputes MAC using the received message and the shared key, compares it to the received MAC.
- Types:
    - HMAC (Hash-based MAC): Uses a cryptographic hash function (like SHA-256) combined with the secret key.
    - CMAC (Cipher-based MAC): Uses a block cipher algorithm (like AES) combined with the secret key.

## Digital Signatures

### Question: What is a digital signature? How can the validity of documents be checked?
- Digital Signature Definition:
    - An electronic, cryptographic mechanism used to verify the authenticity (originator) and integrity (unchanged content) of digital messages or documents.
    - Provides non-repudiation (sender cannot deny sending).
- How it works (using asymmetric crypto):
    1. Sender calculates hash of the message.
    2. Sender encrypts the hash value with their private key. This encrypted hash is the digital signature.
    3. Sender attaches the signature to the message.
    4. Receiver decrypts the signature using the sender's public key to retrieve the original hash.
    5. Receiver calculates the hash of the received message independently.
    6. If the decrypted hash matches the calculated hash, the signature is valid (authenticity and integrity verified).
- Checking Document Validity:
    - Digital Signature Verification: As described above. Requires sender's public key, often obtained via a digital certificate.
    - Hash Verification: If a known secure hash of the original document is available, calculate hash of the received document and compare.
    - Digital Certificate Check: Verify the digital certificate associated with the signature. Check if it's issued by a trusted Certificate Authority (CA), if it's expired, or if it has been revoked.

## Authentication Applications

### Question: Describe Kerberos and X.509.
- Kerberos:
    - Network authentication protocol.
    - Provides strong authentication for client/server applications using symmetric key cryptography.
    - Uses a trusted third party: Key Distribution Center (KDC).
    - Issues tickets to users (clients) allowing them to access specific services without re-entering passwords.
    - Protects against eavesdropping and replay attacks.
- X.509:
    - A standard defining the format for public key certificates.
    - Certificates bind a public key to a specific identity (person, organization, server).
    - Issued by a Certificate Authority (CA).
    - Basis for Public Key Infrastructure (PKI).
    - Used in SSL/TLS (HTTPS), S/MIME, IPsec, digital signatures.

# Unit V: E-Mail Security

## Email Security Protocols

### Question: Which protocol is used for email & process of email/email server?
- Sending Email:
    - SMTP (Simple Mail Transfer Protocol): Standard protocol for sending emails from a client to a server, and between mail servers.
- Receiving Email:
    - POP3 (Post Office Protocol version 3): Downloads email from server to client (usually deleting from server). Simple, less suitable for multiple devices.
    - IMAP (Internet Message Access Protocol): Allows client to access and manage email stored on the server. Suitable for multiple devices, more complex.
- Email Process Overview:
    1. Sender composes email using Mail User Agent (MUA - e.g., Outlook, Gmail web).
    2. Sender's MUA sends email via SMTP to their Mail Transfer Agent (MTA - mail server).
    3. Sender's MTA relays email via SMTP to Receiver's MTA (using DNS MX records to find it).
    4. Receiver's MTA stores the email.
    5. Receiver uses their MUA to retrieve the email from their MTA using POP3 or IMAP.

### Question: What is PGP?
- PGP (Pretty Good Privacy):
    - Popular program/standard for email encryption and signing.
    - Provides confidentiality (encryption), integrity, authentication (digital signatures), and non-repudiation for emails and files.
    - Often uses a "Web of Trust" model for key verification, in addition to hierarchical PKI.
    - Uses a combination of symmetric (for bulk encryption) and asymmetric (for key exchange and signing) cryptography.

### Question: Explain S/MIME.
- S/MIME (Secure/Multipurpose Internet Mail Extensions):
    - Standard for public key encryption and signing of MIME data (email content).
    - Provides confidentiality, integrity, authentication, non-repudiation.
    - Relies on a hierarchical Public Key Infrastructure (PKI) with trusted Certificate Authorities (CAs) to issue X.509 certificates.
    - Integrated into many modern email clients (e.g., Outlook, Apple Mail).

## IP Security (IPsec)

### Question: Explain IPsec - header, frame format. What is an Authentication Header? How many bits in IPv4/IPv6?
- IPsec (Internet Protocol Security):
    - A suite of protocols for securing IP communications at the network layer.
    - Provides authentication, integrity, confidentiality, and anti-replay protection for IP packets.
    - Operates in two modes: Transport mode (protects payload) and Tunnel mode (protects entire IP packet).
- Core IPsec Protocols/Headers:
    - Authentication Header (AH):
        - Provides data origin authentication and connectionless integrity for IP packets.
        - Protects against replay attacks.
        - Does NOT provide confidentiality (no encryption).
        - Authenticates parts of the IP header as well as the payload.
    - Encapsulating Security Payload (ESP):
        - Provides confidentiality (encryption).
        - Can optionally provide data origin authentication and integrity (features overlap with AH).
        - Does not typically protect the outer IP header in tunnel mode.
- IP Address Bits:
    - IPv4: 32 bits.
    - IPv6: 128 bits.

## Key Management in Email Security

### Question: What is key management in email security?
- Key Management Importance:
    - Securely creating, storing, distributing, using, and revoking cryptographic keys (both symmetric and asymmetric) used for email encryption and signing (PGP, S/MIME).
- Aspects:
    - Key Generation: Creating strong key pairs (public/private).
    - Key Distribution: Sharing public keys reliably (e.g., via certificates, key servers, web of trust).
    - Key Storage: Protecting private keys from compromise.
    - Key Revocation: Handling compromised or outdated keys (e.g., Certificate Revocation Lists - CRLs, Online Certificate Status Protocol - OCSP).

# Unit VI: Web Security

## Firewalls

### Question: What is the definition of a firewall? What are its types? What is its purpose in Windows? Why isolate WLAN traffic?
- Firewall Definition:
    - A network security system (hardware or software).
    - Monitors and controls incoming and outgoing network traffic based on predetermined security rules.
    - Establishes a barrier between a trusted internal network and untrusted external networks (like the Internet).
- Purpose:
    - Block unwanted/malicious traffic.
    - Prevent unauthorized access to or from the protected network/system.
    - Enforce network access policies.
    - Purpose in Windows (Windows Firewall): Protect the individual computer from network threats by filtering traffic to/from it.
- Why Isolate WLAN Traffic (using Firewall/VLANs):
    - Wireless networks are inherently less secure due to broadcast nature.
    - Isolate Wi-Fi traffic (especially guest networks) from sensitive wired networks to prevent breaches originating from less trusted wireless devices.
    - Protect VPN traffic passing through a potentially shared WLAN from other devices on that same WLAN.
- Types of Firewalls:
    - Packet-Filtering Firewall: Examines packet headers (IP address, port). Simple, fast.
    - Stateful Inspection Firewall: Tracks the state of active connections, makes decisions based on context. More secure than packet filtering.
    - Proxy Firewall (Application-Level Gateway): Acts as an intermediary for specific applications (e.g., HTTP, FTP). Deep inspection possible.
    - Next-Generation Firewall (NGFW): Integrates traditional firewall functions with other security services like intrusion prevention (IPS), deep packet inspection (DPI), application awareness, malware filtering.

## SSL/TLS

### Question: What is SSL? How to check the authentication of a website?
- SSL (Secure Sockets Layer):
    - Predecessor to TLS (Transport Layer Security). Often used interchangeably, but TLS is the modern standard.
    - Cryptographic protocol designed to provide secure communication over a computer network (primarily between web browser and server).
    - Establishes an encrypted link, ensuring confidentiality and integrity of data exchanged.
    - Uses asymmetric cryptography for handshake (key exchange, authentication) and symmetric cryptography for bulk data encryption.
- Checking Website Authentication (via SSL/TLS):
    - Check for HTTPS: URL starts with `https://` instead of `http://`.
    - Padlock Icon: Look for a padlock icon in the browser's address bar. Indicates a secure connection.
    - SSL/TLS Certificate: Click the padlock icon to view the website's certificate details.
        - Check Issued To: Verify it matches the website domain.
        - Check Issued By: Verify it's issued by a trusted Certificate Authority (CA).
        - Check Validity Dates: Ensure the certificate is not expired.

## Common Web Attacks and Defenses

### Question: What is cross-site scripting (XSS)?
- Cross-Site Scripting (XSS):
    - A type of web security vulnerability.
    - Allows attackers to inject malicious scripts (usually JavaScript) into content from trusted websites that is then delivered to and executed by victims' browsers.
    - Goals: Steal user data (cookies, session tokens), deface websites, redirect users, install malware.
    - Types: Stored XSS, Reflected XSS, DOM-based XSS.

### Question: What is intrusion detection?
- Intrusion Detection System (IDS):
    - A device or software application that monitors network or system activities for malicious activity or policy violations.
    - Goal: Detect unauthorized access or attacks.
    - Actions: Typically logs the event and sends an alert; doesn't actively block (that's an Intrusion Prevention System - IPS).
    - Importance: Helps identify attacks early, enables response, provides forensic data.

## Password and Browser Security

### Question: What are the risks/problems with default, printed, or plain text passwords?
- Default Passwords:
    - Often publicly known or easily guessed.
    - Failure to change allows trivial unauthorized access.
- Printed Passwords:
    - Physical security risk. Easily stolen or seen if the paper is found.
- Plain Text Passwords:
    - Transmission Risk: If sent unencrypted over a network, easily intercepted by eavesdroppers.
    - Storage Risk: If stored unhashed/unencrypted in a database, a single data breach exposes all passwords.

### Question: What are types of passwords? How do you decide if a password is strong or weak?
- Types of Password/Authentication Factors:
    - Something you know: Simple password, complex password, passphrase, PIN.
    - Something you have: OTP (One-Time Password) generator (hardware token, app), smart card.
    - Something you are: Biometric password (fingerprint, facial recognition, iris scan).
    - Graphical password: Pattern unlock on phones.
- Strong vs. Weak Password Characteristics:
    - Strong:
        - Length: Long (e.g., 12+ characters, ideally more).
        - Complexity: Uses a mix of uppercase letters, lowercase letters, numbers, and special characters (!@#$%^&*).
        - Unpredictability: Avoids dictionary words, common names, dates, personal information, simple patterns (qwerty, 123456).
        - Uniqueness: Different password used for different accounts.
    - Weak: Fails on one or more of the above points (short, simple, predictable, reused).

### Question: How can we improve browser security?
- Update Browser: Keep the browser and its plugins up-to-date to patch vulnerabilities.
- Strong Passwords & Management: Use strong, unique passwords for websites; consider a password manager.
- Enable Security Settings: Configure browser security/privacy settings (e.g., block pop-ups, limit tracking, control cookies, enable phishing/malware protection).
- Safe Extensions: Only install browser extensions from trusted sources; review permissions requested.
- Be Cautious: Avoid clicking suspicious links or downloading unknown files. Check for HTTPS.
- Use VPN (Optional): Encrypts traffic between browser and VPN server, especially on public Wi-Fi.

## VPN

### Question: What is a VPN?
- VPN (Virtual Private Network):
    - Creates a secure, encrypted connection (a "tunnel") over a public network like the Internet.
    - Allows users to send and receive data as if their devices were directly connected to a private network.
    - Uses: Secure remote access to corporate networks, enhancing privacy and security on public Wi-Fi, bypassing geo-restrictions (with limitations).
