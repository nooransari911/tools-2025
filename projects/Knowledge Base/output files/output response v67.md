# Unit I - Attacks on Computers and Computer Security

## Security Need and Definition

### Question: What is computer security and why is it needed?
- Definition: Protecting computer systems, networks, and data from theft, damage, unauthorized access, or disruption.
- Need:
    - Protect sensitive data (personal, financial, corporate).
    - Ensure system availability and reliability.
    - Maintain data integrity (accuracy and trustworthiness).
    - Prevent unauthorized use of resources.
    - Comply with regulations.

## Security Principles (CIAAN)

### Question: Explain the principles of security.
- Confidentiality: Preventing unauthorized disclosure of information. Ensures only authorized users can access data. (Keeps data secret).
- Integrity: Ensuring data is accurate, complete, and has not been altered without authorization. (Keeps data correct).
- Availability: Ensuring authorized users can access information and resources when needed. (Keeps systems accessible).
- Authentication: Verifying the identity of a user, system, or entity. (Confirms identity).
- Non-repudiation: Providing proof that a specific party performed an action (e.g., sent a message), preventing them from denying it later. (Provides proof of origin/action).

## Types of Security Attacks

### Question: Name two types of security attacks.
- Passive Attacks: Involve monitoring or eavesdropping on communications or system activities without altering data. Difficult to detect.
    - Examples: Traffic analysis, eavesdropping on unencrypted data.
- Active Attacks: Involve modifying data, creating false data, or disrupting system services. Easier to detect but harder to prevent.
    - Examples: Masquerade (impersonation), replay, modification of messages, denial of service (DoS).

## Network Security Model

### Question: Describe a model for network security.
- Core Components:
    - Sender: Originator of the message.
    - Receiver: Intended recipient of the message.
    - Message: Data being transmitted.
    - Channel: Medium used for transmission (e.g., internet, wireless).
- Security Aspects:
    - Adversary (Threat): Entity attempting to compromise security (e.g., intercept, modify, disrupt).
    - Security Mechanisms: Techniques used to protect the communication (e.g., encryption, authentication protocols).
    - Trusted Third Party (Optional): Entity relied upon for certain security functions (e.g., key distribution center, certificate authority).
- Goal: To ensure secure transfer of information between sender and receiver, protecting against threats using security services and mechanisms.

## Passwords and Authentication Basics

### Question: Why do we require passwords?
- Purpose: Primary mechanism for user authentication.
- Function: Verifies a user's claimed identity, granting access only to authorized individuals. Protects resources and data from unauthorized access.

### Question: What are types of passwords/authenticators?
- Knowledge-based: Something the user knows (e.g., simple password, complex password, PIN).
- Possession-based: Something the user has (e.g., OTP token, smart card).
- Inherence-based: Something the user is (e.g., biometric data like fingerprint, iris scan).
- Graphical password: Using patterns or images.
- OTP (One-Time Password): Password valid for only one login session or transaction.

### Question: How do you decide if a password is strong or weak?
- Strong Password Characteristics:
    - Length: Sufficiently long (e.g., 12+ characters recommended).
    - Complexity: Uses a mix of character types (uppercase, lowercase, numbers, special symbols).
    - Randomness: Avoids dictionary words, common names, personal information, simple patterns.
    - Uniqueness: Not reused across different accounts.
- Weak Password Characteristics: Short, simple, uses common words/patterns, easily guessable personal info.

### Question: What is the problem with using default passwords?
- Risk: Default passwords are often publicly known or easily guessed.
- Consequence: Failure to change them leaves systems highly vulnerable to immediate unauthorized access upon deployment.

### Question: Why is it dangerous to print passwords on paper?
- Risk: Physical security breach.
- Consequence: If the paper is found, lost, or stolen, the password and associated account/data are compromised.

### Question: What is the risk of sending passwords in plain text?
- Risk: Eavesdropping during transmission.
- Consequence: Attackers monitoring the network can easily capture the password, leading to unauthorized access. Encryption is required during transmission.

# Unit II - Cryptography-Concepts and Techniques

## Cryptography, Plaintext, Ciphertext

### Question: What is cryptography?
- Definition: The science and practice of techniques for secure communication in the presence of adversaries.
- Core Functions: Enables confidentiality, integrity, authentication, and non-repudiation of information. Involves encryption, decryption, hashing, digital signatures, etc.

### Question: What is plaintext and ciphertext?
- Plaintext: The original, readable message or data before encryption.
- Ciphertext: The unreadable, scrambled message or data resulting from applying an encryption algorithm to plaintext. Requires a key to decrypt back to plaintext.

## Symmetric vs Asymmetric Key Cryptography

### Question: Compare symmetric and asymmetric key cryptography.
- Symmetric Key Cryptography:
    - Keys: Uses a single, shared secret key for both encryption and decryption.
    - Speed: Generally faster algorithms.
    - Key Management: Secure distribution of the shared key is a major challenge.
    - Use Cases: Bulk data encryption (e.g., file encryption, secure communication sessions after key exchange).
    - Examples: DES, AES, RC4.
- Asymmetric Key Cryptography (Public Key Cryptography):
    - Keys: Uses a pair of keys: a public key (shared openly) and a private key (kept secret). One key encrypts, the other decrypts.
    - Speed: Generally slower algorithms.
    - Key Management: Simplifies key distribution (public key can be shared freely); requires methods to verify public key authenticity (e.g., PKI).
    - Use Cases: Digital signatures, secure key exchange, encryption of small amounts of data (like symmetric keys).
    - Examples: RSA, Diffie-Hellman, ECC.

## Cipher Types: Substitution and Transposition

### Question: What is a cipher? Why do we need ciphers?
- Definition: A cipher is an algorithm or method used for performing encryption or decryption.
- Need: To transform plaintext into ciphertext to ensure confidentiality, protecting data from being understood by unauthorized parties.

### Question: Explain substitution and transposition techniques. What is a Caesar Cipher?
- Substitution Technique:
    - Method: Replaces units of plaintext (letters, pairs of letters, etc.) with corresponding units of ciphertext according to a defined scheme.
    - Example: Caesar Cipher - Each letter in the plaintext is shifted a fixed number of positions down the alphabet (e.g., shift 3: A becomes D, B becomes E).
- Transposition Technique:
    - Method: Rearranges the positions of the plaintext units (letters, bits) according to a specific permutation. The letters themselves are not changed.
    - Example: Rail Fence Cipher - Writing plaintext letters in a zig-zag pattern across several 'rails' and reading off rail by rail.

## Steganography

### Question: What is steganography? What are its applications?
- Definition: The practice of concealing a secret message or data within another non-secret file or message (the "cover" object, e.g., image, audio file) to hide the very existence of the secret communication. Different from cryptography, which hides the content but not the existence.
- Applications:
    - Covert communication (hiding messages).
    - Watermarking (embedding copyright or ownership information invisibly).
    - Tamper detection (changes to the cover object might disrupt the hidden data).

# Unit III - Symmetric and Asymmetric Key for Ciphers

## Block Cipher Principles and Modes

### Question: What are the steps in block cipher working?
- Principle: Encrypts plaintext in fixed-size blocks (e.g., 64 bits, 128 bits).
- Steps (Simplified):
    1. Padding (if needed): If the last block of plaintext is smaller than the required block size, padding is added to fill it.
    2. Division: Plaintext is divided into fixed-size blocks.
    3. Encryption: Each block is encrypted using the symmetric key and the chosen algorithm (e.g., AES, DES).
    4. Mode of Operation: A specific mode (e.g., ECB, CBC, CTR) is used to handle multiple blocks, defining how the encryption of one block relates to the next (e.g., using Initialization Vectors (IVs), chaining).

## Symmetric Algorithms: DES, AES, Blowfish

### Question: What is DES? What is its use? Is it a block cipher?
- Full Form: Data Encryption Standard.
- What: An early, influential symmetric block cipher algorithm.
- Characteristics: Uses a 56-bit key and operates on 64-bit blocks.
- Use/Status: Now considered insecure due to the small key size (vulnerable to brute-force attacks). Largely obsolete, replaced by AES.
- Type: Yes, it is a block cipher.

### Question: What is AES? Is it a block cipher?
- Full Form: Advanced Encryption Standard.
- What: The current global standard for symmetric block encryption.
- Characteristics: Operates on 128-bit blocks. Supports key sizes of 128, 192, or 256 bits. Offers strong security and good performance.
- Type: Yes, it is a block cipher.

### Question: Explain DES, AES, and Blowfish.
- DES: (See above). 56-bit key, 64-bit block. Outdated.
- AES: (See above). 128/192/256-bit key, 128-bit block. Current standard, widely used, secure. Based on Rijndael algorithm.
- Blowfish: Symmetric block cipher. Variable key length (32 to 448 bits), 64-bit block size. Designed as a fast, free alternative to DES. Still considered secure but often succeeded by Twofish or AES in new applications.

## Asymmetric Algorithms: RSA

### Question: What is RSA? What is its long form?
- Full Form: Rivest-Shamir-Adleman (named after its inventors).
- What: A widely used public-key (asymmetric) cryptosystem.
- Function: Used for both encryption (using the public key) and digital signatures (using the private key).
- Security Basis: Relies on the computational difficulty of factoring large integers (the product of two large prime numbers).

## Key Generation Guidelines

### Question: What are the guidelines to generate keys?
- Randomness: Keys should be generated using cryptographically secure pseudo-random number generators (CSPRNGs) to ensure unpredictability.
- Length: Keys must be long enough to resist brute-force attacks, based on the chosen algorithm and current computational power (e.g., AES 128/256 bits, RSA 2048/3072 bits).
- Secrecy (for private/symmetric keys): Private keys and shared symmetric keys must be stored and handled securely to prevent compromise.
- Uniqueness: Keys should generally be unique per user or session where appropriate.

## Key Distribution and Management

### Question: What is key distribution/management?
- Definition: The process and infrastructure for securely handling cryptographic keys throughout their lifecycle.
- Lifecycle Includes: Generation, distribution, storage, usage, backup, revocation, and destruction of keys.
- Challenge (Symmetric): Securely sharing the initial secret key between parties without it being intercepted. Solutions include out-of-band methods, Key Distribution Centers (KDCs like Kerberos), or using asymmetric encryption to exchange the symmetric key.
- Challenge (Asymmetric): Ensuring the authenticity of public keys (that a public key truly belongs to the claimed entity). Solution is typically a Public Key Infrastructure (PKI).

# Unit IV - Message Authentication Algorithms and Hash Functions

## Hash Functions

### Question: What is a hash function?
- Definition: An algorithm that takes an input (message or data of arbitrary size) and produces a fixed-size string of characters, which is the hash value (or message digest).
- Properties:
    - One-way: Computationally infeasible to reverse the process (find the input from the hash output).
    - Deterministic: The same input always produces the same hash output.
    - Collision Resistance: Computationally infeasible to find two different inputs that produce the same hash output.
    - Fixed-Size Output: Output length is constant regardless of input length (e.g., SHA-256 always produces 256 bits).
- Use: Primarily for verifying data integrity (checking if data has been altered). Also used in password storage, digital signatures, etc.

## Message Authentication Codes (MACs)

### Question: Explain Message Authentication Codes (MACs). What are types? What is the full form?
- Full Form: Message Authentication Code.
- What: A short piece of information used to authenticate a message and ensure its integrity. It verifies that the message came from the alleged sender and has not been changed.
- How it Works: Generated using a cryptographic hash function applied to the message content combined with a shared secret key between the sender and receiver. The resulting hash (the MAC) is sent with the message. The receiver performs the same computation using the message and the shared key and compares the result.
- Provides: Integrity and Authentication (but not non-repudiation, as both sender and receiver share the key).
- Types:
    - HMAC (Hash-based MAC): A specific construction using hash functions like SHA-256. Widely used standard.
    - CMAC (Cipher-based MAC): Based on symmetric block ciphers like AES.

## Digital Signatures

### Question: What is a digital signature? What are its types? Which software is used?
- Definition: An electronic, encrypted stamp of authentication on digital information (like email, documents). It uses asymmetric cryptography.
- How it Works:
    1. Sender calculates a hash of the message.
    2. Sender encrypts the hash value with their private key. This encrypted hash is the digital signature.
    3. Signature is attached to the message and sent.
    4. Receiver decrypts the signature using the sender's public key to recover the original hash.
    5. Receiver calculates their own hash of the received message.
    6. If the two hashes match, the signature is valid.
- Provides:
    - Authentication: Verifies the sender's identity (only the owner of the private key could create it).
    - Integrity: Ensures the message was not altered after signing (hash would not match).
    - Non-repudiation: Sender cannot deny sending the message (as only they have the private key).
- Types (Legal/Regulatory Context): Basic, Advanced, Qualified (based on level of assurance and legal standing, varies by jurisdiction).
- Software Examples: Adobe Acrobat/Reader, DocuSign, cryptographic libraries (OpenSSL), email clients (PGP/S/MIME support), government portals (e.g., eMudhra in India).

## Authentication Applications: Kerberos

### Question: Describe Kerberos.
- What: A network authentication protocol designed to provide strong authentication for client/server applications using secret-key cryptography.
- Goal: Allows users (clients) to prove their identity to servers and vice versa, across an insecure network. Avoids sending passwords over the network.
- Key Components:
    - Key Distribution Center (KDC): Central trusted server, comprises Authentication Server (AS) and Ticket-Granting Server (TGS).
    - Authentication Server (AS): Verifies user credentials initially.
    - Ticket-Granting Server (TGS): Issues tickets for specific services.
- Mechanism (Simplified): User logs in once -> AS provides a Ticket-Granting Ticket (TGT) -> User uses TGT to request service tickets from TGS -> User presents service ticket to the application server for access. Uses symmetric key cryptography and timestamps to prevent replay attacks.

## Authentication Infrastructure: X.509 Certificates and PKI

### Question: Describe X.509.
- What: A standard defining the format of public key certificates. It specifies standard formats for certificates, certificate revocation lists (CRLs), attribute certificates, and a certification path validation algorithm.
- Purpose: To bind a public key to a specific identity (person, organization, device) through a digital signature from a trusted Certificate Authority (CA).
- Role: The cornerstone of most Public Key Infrastructures (PKIs). Used in SSL/TLS, S/MIME, code signing, etc.

### Question: What is PKI? (Implied by X.509 context)
- Full Form: Public Key Infrastructure.
- What: A set of roles, policies, hardware, software, and procedures needed to create, manage, distribute, use, store, and revoke digital certificates and manage public-key encryption.
- Function: Enables secure use of public key cryptography by providing mechanisms to verify the authenticity of public keys via trusted Certificate Authorities (CAs) issuing X.509 certificates.

## Checking Document Validity

### Question: How to check the validity of documents?
- Method: Primarily using digital signatures and hash verification.
- Process:
    1. Check for a Digital Signature: Verify if the document has been digitally signed.
    2. Validate the Signature: Use software (like Adobe Reader for PDFs) to validate the signature. This involves:
        - Checking the integrity: Recalculating the document hash and comparing it to the hash embedded in the signature (decrypted with the sender's public key).
        - Checking authenticity: Verifying that the public key used belongs to the claimed signer, typically by checking the associated X.509 digital certificate.
        - Checking certificate validity: Ensuring the signer's certificate is trusted (issued by a recognized CA), has not expired, and has not been revoked (using CRLs or OCSP).
    3. Hash Verification (if signature absent): If a separate hash value is provided securely, recalculate the document's hash and compare it to the provided value to check integrity.

# Unit V - E-Mail Security

## Email Security Protocols: SMTP, POP3, IMAP

### Question: Which protocol is used for email & process of email/email server?
- Sending Email: SMTP (Simple Mail Transfer Protocol) is the standard protocol used for sending emails from a client to a server, and for relaying emails between mail servers.
- Receiving Email:
    - POP3 (Post Office Protocol version 3): Downloads emails from the server to the client device. Messages are often deleted from the server after download (by default). Simpler protocol.
    - IMAP (Internet Message Access Protocol): Allows clients to access and manage emails directly on the mail server. Changes (reading, deleting, organizing) are synchronized across multiple devices. More complex, keeps messages on the server.
- Email Process (Simplified): Sender Client -> Sender Mail Server (SMTP) -> [Relay via other Mail Servers (SMTP)] -> Receiver Mail Server (stores email) -> Receiver Client retrieves email (using POP3 or IMAP).

## Pretty Good Privacy (PGP)

### Question: What is PGP?
- Full Form: Pretty Good Privacy.
- What: An encryption program that provides cryptographic privacy and authentication for data communication. Widely used for signing, encrypting, and decrypting emails, files, and directories.
- Features:
    - Confidentiality: Encrypts emails/files using symmetric encryption with a session key, which is itself encrypted using the recipient's public key (hybrid approach).
    - Authentication/Integrity: Uses digital signatures (hashing + private key encryption).
- Key Management Model: Often relies on a decentralized "Web of Trust" model where users sign each other's keys, although it can also use hierarchical PKI.

## Secure/Multipurpose Internet Mail Extensions (S/MIME)

### Question: Explain S/MIME.
- Full Form: Secure/Multipurpose Internet Mail Extensions.
- What: A standard for public key encryption and digital signing of MIME data (which is the standard format for email bodies). Allows sending encrypted and/or digitally signed emails.
- Functionality: Provides confidentiality (encryption), integrity, authentication, and non-repudiation for email messages.
- How it Works: Similar hybrid approach to PGP (symmetric for bulk encryption, asymmetric for signatures and symmetric key wrapping).
- Key Management: Relies on a centralized, hierarchical Public Key Infrastructure (PKI) using X.509 certificates issued by trusted Certificate Authorities (CAs) to verify identities. Often integrated directly into email clients (e.g., Outlook, Apple Mail).

## IP Security (IPSec) Overview

### Question: What is IP security overview?
- What: A suite of protocols used to secure Internet Protocol (IP) communications by authenticating and/or encrypting each IP packet of a communication session.
- Operates at: Network Layer (Layer 3).
- Provides: Confidentiality, integrity, authentication, and anti-replay protection for IP traffic.
- Modes:
    - Transport Mode: Encrypts/authenticates only the payload of the IP packet. Used for host-to-host communication.
    - Tunnel Mode: Encrypts/authenticates the entire original IP packet (header + payload) and encapsulates it in a new IP packet. Used for site-to-site VPNs (Virtual Private Networks).

## IPSec Components: AH and ESP

### Question: What is an Authentication Header in IP security? Explain IPSec header/frame format (AH and ESP).
- Authentication Header (AH):
    - Purpose: Provides connectionless integrity, data origin authentication, and optional anti-replay protection for IP packets.
    - Does NOT provide confidentiality (no encryption).
    - How: Calculates an Integrity Check Value (ICV) or hash over parts of the IP header and the entire payload.
    - Header Fields: Includes Next Header, Payload Length, Reserved, Security Parameters Index (SPI), Sequence Number, and Authentication Data (the ICV).
- Encapsulating Security Payload (ESP):
    - Purpose: Provides confidentiality (encryption), connectionless integrity, data origin authentication, and optional anti-replay protection.
    - Can provide encryption alone, authentication alone, or both.
    - How: Encrypts the payload (and optionally parts of the header in tunnel mode). Authentication covers the encrypted payload and ESP header/trailer.
    - Header/Trailer Fields: Includes Security Parameters Index (SPI), Sequence Number, Payload Data (encrypted), Padding, Pad Length, Next Header, and Authentication Data (optional ICV).

## Key Management in Email Security

### Question: What is key management in email security?
- Definition: Refers to the secure handling of cryptographic keys used by email security protocols like PGP and S/MIME.
- Importance: Essential for the effectiveness of encryption and digital signatures. Compromised keys undermine the security provided.
- Activities:
    - Key Generation: Creating strong public/private key pairs.
    - Key Distribution/Exchange: Sharing public keys reliably (e.g., via key servers, certificates, web of trust).
    - Key Storage: Protecting private keys securely (e.g., password-protected files, hardware tokens).
    - Key Validation: Verifying the authenticity of received public keys (using PKI/certificates for S/MIME, web of trust for PGP).
    - Key Revocation: Managing compromised or expired keys (e.g., Certificate Revocation Lists (CRLs), key expirations).

# Unit VI - Web Security

## Firewall Concepts and Types

### Question: What is definition/purpose of firewall? What are firewalls and their types? Why isolate WLAN traffic with a firewall?
- Definition: A network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules.
- Purpose: To establish a barrier between a trusted internal network (or host) and untrusted external networks (like the Internet), blocking unauthorized or malicious traffic while permitting legitimate communications. Keeps the system/network safe.
- Types:
    - Packet-Filtering Firewall: Examines packet headers (IP addresses, port numbers, protocol type). Simple, fast, but limited context.
    - Stateful Inspection Firewall: Tracks the state of active connections and makes decisions based on the context of the traffic flow, not just individual packets. More secure than basic packet filtering.
    - Proxy Firewall (Application Gateway): Acts as an intermediary for specific applications (e.g., HTTP, FTP). Inspects traffic at the application layer, providing granular control and masking internal network structure, but can impact performance.
    - Next-Generation Firewall (NGFW): Combines traditional firewall features with advanced capabilities like deep packet inspection (DPI), intrusion prevention (IPS), application awareness, and threat intelligence integration.
- Isolating WLAN Traffic: Using a firewall (often integrated into routers/access points) to segment wireless traffic from wired networks or create guest networks prevents potential threats originating from less trusted wireless devices from easily spreading to critical wired infrastructure.

## Secure Sockets Layer (SSL) / Transport Layer Security (TLS)

### Question: What is SSL?
- Full Form: Secure Sockets Layer. (Note: TLS - Transport Layer Security is the successor and widely used now, though 'SSL' is often used colloquially).
- What: A standard security protocol for establishing encrypted links between a web server and a browser (or other client/server applications).
- Purpose: Ensures that data transmitted between the server and client remains private (confidentiality via encryption) and integral (integrity via MACs). Also provides server authentication (and optionally client authentication) using certificates.
- How: Uses a handshake process involving asymmetric cryptography (to authenticate the server and exchange a symmetric session key) and symmetric cryptography (to encrypt the actual data transfer).

## Website Authentication Check

### Question: How to check authentication/security of a website?
- Check for HTTPS: Look for `https://` at the beginning of the URL, not just `http://`. The 'S' indicates a secure connection using SSL/TLS.
- Look for Padlock Icon: Modern browsers display a padlock icon in the address bar for HTTPS sites. Clicking it often provides details about the connection and certificate.
- Examine the SSL/TLS Certificate:
    - Click the padlock icon to view certificate details.
    - Check who issued the certificate (the Certificate Authority - CA). Should be a trusted CA.
    - Check the 'Issued To' field to ensure it matches the website domain you expect.
    - Check the validity dates (ensure it hasn't expired).
- Browser Warnings: Pay attention to any warnings the browser displays about insecure connections or invalid certificates.

## Cross-Site Scripting (XSS)

### Question: What is cross-site scripting (XSS)?
- What: A type of security vulnerability typically found in web applications.
- How it Works: Attackers inject malicious client-side scripts (e.g., JavaScript) into web pages viewed by other users. When an unsuspecting user visits the compromised page, the malicious script executes within their browser.
- Goal: Can be used to steal sensitive information (like cookies, session tokens), hijack user sessions, redirect users to malicious sites, deface websites, or perform other unauthorized actions on behalf of the user.
- Types: Stored (persistent), Reflected (non-persistent), DOM-based.

## Intrusion Detection Systems (IDS)

### Question: Explain intrusion detection and its importance.
- Definition: A system (device or software) that monitors network or system activities for malicious activities or policy violations.
- Function: Detects potential security breaches (intrusions), logs information about them, and typically reports them to a security administrator. Does not usually block traffic itself (that's IPS - Intrusion Prevention System).
- Importance: Provides visibility into network/system security events, helps identify attacks that may bypass firewalls, aids in incident response and forensic analysis, and helps assess the effectiveness of security policies. Early detection allows for quicker response to mitigate damage.
- Detection Methods: Signature-based (looks for known attack patterns), Anomaly-based (looks for deviations from normal behavior).

## Virtual Private Network (VPN) Basics

### Question: What is a VPN?
- Full Form: Virtual Private Network.
- What: Creates a secure, encrypted connection (a "tunnel") over a public network like the Internet.
- Purpose: Allows users to send and receive data across shared or public networks as if their devices were directly connected to a private network. Enhances privacy and security.
- How: Uses tunneling protocols (like IPSec, OpenVPN, WireGuard) to encapsulate the original network packets and encrypts the data being sent through the tunnel.

## Browser Security Practices

### Question: How can we improve browser security?
- Keep Browser Updated: Install updates promptly to patch known vulnerabilities.
- Use Strong, Unique Passwords: For websites and enable multi-factor authentication where available. Use a password manager.
- Review Security Settings: Configure browser settings for privacy and security (e.g., block third-party cookies, enable phishing/malware protection, control site permissions).
- Install Extensions Cautiously: Only install extensions from trusted sources and review their permissions. Remove unused extensions.
- Check for HTTPS: Prioritize browsing HTTPS sites and be wary of HTTP connections, especially for sensitive activities.
- Be Wary of Downloads/Links: Avoid clicking suspicious links or downloading files from untrusted sources.
- Clear Cache/Cookies Periodically: Can help remove stored data that might be exploited.
- Use Privacy-Focused Browsers/Settings: Consider browsers or modes designed for enhanced privacy.
