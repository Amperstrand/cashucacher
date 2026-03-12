"""
Encryption module for CashuCacher.

This module provides a simple interface for encrypting and decrypting data
using the secure implementations in security_utils.

Security:
    - Uses AES-256-GCM for authenticated encryption
    - PBKDF2-HMAC-SHA256 for secure key derivation with 100,000 iterations
    - Random nonces and salts for each operation
"""

from .security_utils import encrypt_data, decrypt_data

__all__ = ['encrypt_data', 'decrypt_data']
