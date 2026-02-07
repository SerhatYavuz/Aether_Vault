"""
Cryptography Manager - AES-256 Encryption with Argon2id Key Derivation
"""

import os
import json
import zlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

# Security Constants
SALT_SIZE = 16
NONCE_SIZE = 12
KEY_LEN = 32
ARGON_ITERATIONS = 2
ARGON_LANES = 4
ARGON_MEMORY = 64 * 1024


class CryptoManager:
    """Handles compression and encryption operations."""

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        """Derive encryption key from password using Argon2id."""
        kdf = Argon2id(
            salt=salt,
            length=KEY_LEN,
            iterations=ARGON_ITERATIONS,
            lanes=ARGON_LANES,
            memory_cost=ARGON_MEMORY,
            ad=None,
            secret=None
        )
        return kdf.derive(password.encode('utf-8'))

    def encrypt_data(self, file_path: str, password: str) -> bytes:
        """
        Encrypt a file with AES-256-GCM.
        
        Args:
            file_path: Path to file to encrypt
            password: Encryption password
            
        Returns:
            Encrypted payload as bytes
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Read file
        with open(file_path, 'rb') as f:
            plaintext = f.read()

        # Compress data (if beneficial)
        try:
            compressed_data = zlib.compress(plaintext, level=9)
            if len(compressed_data) < len(plaintext):
                final_data = compressed_data
                is_compressed = True
                compression_ratio = (1 - len(compressed_data) / len(plaintext)) * 100
                print(f"Compression: {compression_ratio:.1f}% reduction")
            else:
                final_data = plaintext
                is_compressed = False
                print("Compression skipped (no benefit)")
        except Exception:
            final_data = plaintext
            is_compressed = False

        # Encrypt
        salt = os.urandom(SALT_SIZE)
        nonce = os.urandom(NONCE_SIZE)
        key = self._derive_key(password, salt)
        
        aesgcm = AESGCM(key)
        ciphertext = aesgcm.encrypt(nonce, final_data, None)
        
        # Package metadata and ciphertext
        payload = {
            "salt": salt.hex(),
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex(),
            "ext": os.path.splitext(file_path)[1],
            "comp": is_compressed,
            "version": "2.0"
        }
        
        return json.dumps(payload).encode('utf-8')

    def decrypt_data(self, encrypted_payload: bytes, password: str) -> tuple:
        """
        Decrypt an encrypted payload.
        
        Args:
            encrypted_payload: Encrypted data bytes
            password: Decryption password
            
        Returns:
            Tuple of (decrypted_data, original_extension)
        """
        try:
            package = json.loads(encrypted_payload.decode('utf-8'))
            
            salt = bytes.fromhex(package['salt'])
            nonce = bytes.fromhex(package['nonce'])
            ciphertext = bytes.fromhex(package['ciphertext'])
            extension = package.get('ext', '.dat')
            is_compressed = package.get('comp', False)
            
            # Derive key and decrypt
            key = self._derive_key(password, salt)
            aesgcm = AESGCM(key)
            
            decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
            
            # Decompress if needed
            if is_compressed:
                decrypted_data = zlib.decompress(decrypted_data)
            
            return decrypted_data, extension
            
        except json.JSONDecodeError:
            raise ValueError("Invalid encrypted data format")
        except Exception as e:
            raise ValueError("Decryption failed. Incorrect password or corrupted data.")
