# QR Code Secret Messages

A complete Python application for encrypting secret messages using AES-GCM encryption and converting them into QR codes. Decrypt QR codes back into readable text using a password.

## Features

### Core Features
- **AES-GCM Encryption**: Secure encryption using AES in Galois/Counter Mode
- **SHA-256 Key Derivation**: Password-based key derivation using SHA-256
- **QR Code Generation**: Convert encrypted messages into scannable QR codes
- **QR Code Scanning**: Decode QR codes from image files
- **Error Handling**: Robust error handling for wrong passwords or corrupted data

### Input Options
- Type messages manually in the text area
- Load messages from `.txt` files

### Output Options
- Display QR code preview in the GUI
- Save QR code as PNG image
- Save encrypted payload as `.bin` file

### 🖥 GUI Features
- Clean, beginner-friendly interface using Tkinter
- Tabbed interface with separate Encrypt and Decrypt sections
- Real-time QR code preview
- Password-protected encryption/decryption

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps

1. **Clone or download this project**
   ```bash
   cd qr_secret_messages
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install pycryptodome qrcode[pil] pyzbar Pillow
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage

### Encrypting a Message

1. Open the **Encrypt** tab
2. Enter your secret message in the text area, or click "Load from .txt File" to load from a file
3. Enter a password in the password field
4. Click "Generate QR Code"
5. The QR code will appear in the preview area
6. Optionally:
   - Click "Save QR as PNG" to save the QR code image
   - Click "Save Encrypted Data (.bin)" to save the raw encrypted data

### Decrypting a QR Code

1. Open the **Decrypt** tab
2. Click "Load QR Code Image" and select the QR code image file
3. Enter the password used for encryption
4. Click "Decrypt Message"
5. The decrypted message will appear in the text area below

## Project Structure

```
qr_secret_messages/
│
├── main.py              # Tkinter GUI application
├── crypto_utils.py      # AES encryption/decryption functions
├── qr_utils.py          # QR code generation and reading functions
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Technical Details

### Encryption Process

1. **Key Derivation**: Password → SHA-256 → 32-byte AES key
2. **Encryption**: Message → AES-GCM encryption → (nonce + tag + ciphertext)
3. **Encoding**: Binary payload → Base64 encoding
4. **QR Generation**: Base64 string → QR code image

### Payload Format

The encrypted payload structure:
```
[16 bytes nonce][16 bytes tag][variable bytes ciphertext]
```

This is then Base64-encoded before being placed in the QR code.

### Security Features

- **AES-GCM Mode**: Provides authenticated encryption (confidentiality + integrity)
- **Random Nonce**: Each encryption uses a unique nonce
- **Authentication Tag**: Prevents tampering with encrypted data
- **Password-based**: Simple password-based key derivation

## Dependencies

- **pycryptodome**: AES encryption implementation
- **qrcode**: QR code generation
- **pyzbar**: QR code reading/decoding
- **Pillow**: Image processing

## Example Workflow

1. **Encrypt**:
   ```
   Message: "Hello, this is a secret!"
   Password: "mySecurePassword123"
   → Generates QR code
   → Save QR code as secret.png
   ```

2. **Decrypt**:
   ```
   Load: secret.png
   Password: "mySecurePassword123"
   → Decrypted: "Hello, this is a secret!"
   ```

## Error Handling

The application handles various error scenarios:
- Wrong password during decryption
- Corrupted or invalid QR code images
- Missing files or invalid file formats
- Empty messages or passwords

## Limitations & Future Improvements

### Current Limitations
- Maximum QR code data size is limited (typically ~3KB for standard QR codes)
- Password strength is not enforced (users should use strong passwords)
- No password recovery mechanism

### Suggested Improvements

1. **Larger QR Data Support**
   - Implement QR code version selection based on data size
   - Use higher error correction levels for larger payloads
   - Split large messages across multiple QR codes

2. **Stronger Key Derivation**
   - Implement PBKDF2 or Argon2 for key derivation (with salt)
   - Add key stretching with multiple iterations
   - Store salt in the payload for better security

3. **Enhanced Features**
   - Password strength indicator
   - QR code size/quality options
   - Batch encryption/decryption
   - Command-line interface (CLI) support
   - Export/import encrypted data in JSON format

4. **Security Enhancements**
   - Add salt to key derivation (currently uses plain SHA-256)
   - Implement key derivation iterations (PBKDF2)
   - Add metadata (timestamp, version) to payload
   - Support for different encryption algorithms

5. **User Experience**
   - Drag-and-drop file loading
   - QR code scanning via webcam
   - Dark mode theme
   - Multi-language support

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'Crypto'`
- **Solution**: Install pycryptodome: `pip install pycryptodome`

**Issue**: `ModuleNotFoundError: No module named 'pyzbar'`
- **Solution**: Install pyzbar: `pip install pyzbar`
- **Note**: On Windows, you may also need to install zbar DLLs

**Issue**: QR code cannot be read
- **Solution**: Ensure the QR code image is clear and not distorted
- Try increasing the QR code size when generating

**Issue**: Decryption fails with correct password
- **Solution**: Ensure you're using the exact same password (case-sensitive)
- Check that the QR code wasn't corrupted or modified

## License

This project is provided as-is for educational purposes.

## Author

Created for Cryptography Project - Semester 7

## Acknowledgments

- Uses PyCryptodome for cryptographic operations
- Uses qrcode library for QR code generation
- Uses pyzbar for QR code reading

