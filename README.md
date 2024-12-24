### SecureTextDrive

SecureTextDrive is a highly secure text file storage system, built to protect the confidentiality, integrity, and accessibility of sensitive data. It utilizes advanced cryptographic techniques like RSA and symmetric key encryption, ensuring files remain private throughout their lifecycle. Two-factor authentication (2FA) strengthens user verification, while digital signatures guarantee file integrity. The system also defends against common cyber threats, including MITM attacks, DoS attacks, and SQL injection, offering a robust solution for individuals and organizations seeking enhanced data security.

## Tech Stack

**Client:** Flask, HTML, CSS, JavaScript  
**Server:** Flask  
**Encryption Methods:** Multiplicative Symmetric, RSA  
**Hashing:** SHA-512  
**Digital Signature:** RSA  
**Attacks Tested:** Password Brute Force, DDoS, SQL Injection


## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

**API Keys**  
`API_KEY`, `ANOTHER_API_KEY`

**Database Connection Details**  
`DB_HOSTNAME`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `DB_PORT`

**Mail Configuration**  
`MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_USE_TLS`, `MAIL_USE_SSL`

**Secret Key**  
`SECRET_KEY`

### Installation Instructions

1. **Install Backend Dependencies**

   Navigate to the `SecureTextDrive-Backend` directory and install the required Python dependencies:

   ```bash
   cd SecureTextDrive-Backend
   pip install -r requirements.txt
   ```

   Then, run the backend application:

   ```bash
   python app.py
   ```

2. **Install Frontend Dependencies**

   Navigate to the `SecureTextDrive-FrontEnd` directory and install the Python dependencies as well:

   ```bash
   cd SecureTextDrive-FrontEnd
   pip install -r requirements.txt
   ```

   Run the frontend application:

   ```bash
   python app.py
   ```

## Screenshots
![App Screenshot](https://i.postimg.cc/yND3Bttt/Screenshot-2024-12-25-011552.png)

![App Screenshot](https://i.postimg.cc/cHYKtYsc/Screenshot-2024-12-25-011800.png)

![App Screenshot](https://i.postimg.cc/jjBwjvr5/Screenshot-2024-12-25-011922.png)



