# AetherVault

**Secure File Encryption & Steganography System**

AetherVault is a file encryption tool that combines AES-256 encryption with LSB steganography to hide encrypted files inside 4K images. The tool works completely offline and provides a modern interface for batch processing.

---

## Features

- **AES-256-GCM Encryption** - Industry-standard encryption algorithm
- **4K Steganography** - Hide data in high-resolution images (3840x2160)
- **Argon2id Key Derivation** - Memory-hard key derivation function
- **ZLIB Compression** - Automatic data compression before encryption
- **Offline Operation** - No internet required (fallback gradient generation)
- **Batch Processing** - Handle multiple files simultaneously
- **Drag & Drop Interface** - Modern PyQt6 interface

---

## Installation

### Requirements

- Python 3.9 or higher
- Linux (tested on Kali Linux, should work on other distributions)

### Quick Install

```bash
git clone https://github.com/yourusername/aether-vault.git
cd aether-vault
pip install -r requirements.txt
python3 aether_vault.py
```

### Linux Right-Click Integration

To add AetherVault to your file manager's context menu:

```bash
# Create desktop entry
mkdir -p ~/.local/share/applications

cat > ~/.local/share/applications/aether-vault.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Aether Vault
Exec=python3 /full/path/to/aether_vault.py %F
Icon=security-high
Terminal=false
Categories=Utility;Security;
MimeType=application/octet-stream;image/png;
EOF

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

Replace `/full/path/to/aether_vault.py` with the actual path to the script.

---

## Usage

### GUI Mode

Launch the application:

```bash
python3 aether_vault.py
```

1. Add files using the "Add Files" button or drag and drop
2. Enter an encryption password
3. Click "PROCESS FILES"
4. Encrypted files will be saved as `*_VAULT.png`

### Command Line Mode

```bash
# Encrypt a file
python3 aether_vault.py /path/to/file.pdf

# Decrypt a file
python3 aether_vault.py /path/to/file_VAULT.png
```

---

## Technical Details

### Encryption

- **Algorithm**: AES-256-GCM (Authenticated Encryption)
- **Key Derivation**: Argon2id (2 iterations, 64MB memory, 4 lanes)
- **Salt**: 16 bytes (random per encryption)
- **Nonce**: 12 bytes (random per encryption)

### Steganography

- **Method**: LSB (Least Significant Bit)
- **Resolution**: 4K (3840 x 2160 pixels)
- **Capacity**: Approximately 2.5-3 MB per image
- **Format**: PNG output

### Data Flow

```
File → ZLIB Compression → AES-256 Encryption → Hex Encoding → 
4K Image Generation → LSB Embedding → PNG Output
```

---

## File Naming

- Encrypted files: `originalname_VAULT.png`
- Decrypted files: `originalname_RECOVERED.ext`

---

## Limitations

- Maximum file size: ~2.5 MB (due to steganography capacity limits)
- Output format: PNG only
- Password recovery: Not possible (use strong, memorable passwords)

---

## Security Considerations

1. **Password Strength**: Use strong passwords (12+ characters, mixed case, numbers, symbols)
2. **Backup**: Keep backups of original files before encryption
3. **No Recovery**: Lost passwords cannot be recovered
4. **PNG Modification**: Do not edit the PNG file or data will be lost

---

## Troubleshooting

### "File too large" error

Your file exceeds the 2.5 MB capacity limit. Consider:
- Compressing the file before encryption
- Splitting large files into smaller parts

### "Decryption failed" error

- Verify you're using the correct password
- Ensure the PNG file hasn't been modified or corrupted

### Module import errors

```bash
pip install --upgrade -r requirements.txt
```

---

## License

MIT License - See LICENSE file for details

---

## Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Test your changes thoroughly
4. Submit a pull request with a clear description

---

## Disclaimer

This tool is for educational and legitimate security purposes only. Users are responsible for complying with applicable laws and regulations. The developers assume no liability for misuse.

---

## Project Structure

```
aether-vault/
├── aether_vault.py      # Main application
├── crypto_manager.py    # Encryption/decryption logic
├── image_factory.py     # Image generation and steganography
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── LICENSE             # MIT License
└── .gitignore         # Git ignore rules
```

---

## Version

Current version: 2.0

For version history, see commit logs.
