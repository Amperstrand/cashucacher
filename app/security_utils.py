"""
Security utilities for cryptographic operations in CashuCacher.

This module provides secure cryptographic utilities including AES-256-GCM
encryption, PBKDF2 key derivation, and related security functions.

Security:
    - Uses AES-256-GCM for authenticated encryption
    - PBKDF2-HMAC-SHA256 for secure key derivation
    - Random nonces and salts for each operation
    - Proper error handling for security failures
"""

import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64


class SecurityUtils:
    """
    Cryptographic utilities for secure encryption and key derivation.
    
    This class provides static methods for:
        - PBKDF2 key derivation with secure parameters
        - AES-256-GCM authenticated encryption
        - Secure random value generation
    
    Security Parameters:
        - SALT_LENGTH: 32 bytes (sufficient entropy)
        - NONCE_LENGTH: 12 bytes (GCM standard)
        - ITERATIONS: 100,000 (NIST recommendation)
    """
    
    SALT_LENGTH = 32
    NONCE_LENGTH = 12
    ITERATIONS = 100000
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        """
        Derive encryption key using PBKDF2-HMAC-SHA256.
        
        This method implements secure key derivation to prevent brute force
        attacks and rainbow table attacks against encrypted data.
        
        Args:
            password: The password/passphrase for key derivation
            salt: Optional salt (randomly generated if None)
            
        Returns:
            tuple: (derived_key, salt_used)
            
        Security:
            - Uses 100,000 iterations to prevent brute force attacks
            - 32-byte salt provides sufficient entropy
            - SHA256 provides collision resistance
            - Random salt generation if not provided
            
        Raises:
            ValueError: If password is None or empty
        """
        if not password:
            raise ValueError("Password cannot be empty")
            
        if salt is None:
            salt = os.urandom(SecurityUtils.SALT_LENGTH)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=SecurityUtils.ITERATIONS,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))
        return key, salt
    
    @staticmethod
    def encrypt_data_gcm(plaintext: str, password: str) -> str:
        """
        Encrypt plaintext data using AES-256-GCM.
        
        This method provides authenticated encryption with:
        - AES-256 for strong confidentiality
        - GCM mode for authentication and integrity
        - Random nonce for semantic security
        - Secure key derivation
        
        Args:
            plaintext: Data to encrypt (must be string)
            password: Password for key derivation
            
        Returns:
            str: Base64-encoded encrypted data (salt + nonce + ciphertext + tag)
            
        Security:
            - Uses AES-256-GCM (NIST approved)
            - Random nonce per encryption prevents replay attacks
            - GMAC tag ensures data integrity
            - PBKDF2 key derivation prevents brute force attacks
            
        Raises:
            ValueError: If plaintext is None
        """
        if plaintext is None:
            raise ValueError("Plaintext cannot be None")
        
        key, salt = SecurityUtils.derive_key(password)
        nonce = os.urandom(SecurityUtils.NONCE_LENGTH)
        
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        
        ciphertext = encryptor.update(plaintext.encode('utf-8')) + encryptor.finalize()
        
        combined = salt + nonce + ciphertext + encryptor.tag
        return base64.urlsafe_b64encode(combined).decode('utf-8')
    
    @staticmethod
    def decrypt_data_gcm(encrypted_data: str, password: str) -> str:
        """
        Decrypt data using AES-256-GCM with authentication verification.
        
        This method provides secure decryption with:
        - GMAC tag verification before decryption
        - Secure key derivation
        - Proper error handling for authentication failures
        
        Args:
            encrypted_data: Base64-encoded encrypted data (salt + nonce + ciphertext + tag)
            password: Password for key derivation
            
        Returns:
            str: Decrypted plaintext data
            
        Security:
            - Verifies GMAC tag before decryption (prevents tampering)
            - Uses constant-time operations (security against timing attacks)
            - Proper error handling doesn't leak sensitive information
            - Authentication ensures data integrity
            
        Raises:
            ValueError: If decryption fails due to authentication failure or invalid data
        """
        try:
            combined = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            
            salt = combined[:SecurityUtils.SALT_LENGTH]
            nonce = combined[SecurityUtils.SALT_LENGTH:SecurityUtils.SALT_LENGTH + SecurityUtils.NONCE_LENGTH]
            tag = combined[-16:]
            ciphertext = combined[SecurityUtils.SALT_LENGTH + SecurityUtils.NONCE_LENGTH:-16]
            
            key, _ = SecurityUtils.derive_key(password, salt)
            
            cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            return plaintext.decode('utf-8')
        
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

def encrypt_data(plaintext: str, password: str) -> str:
    return SecurityUtils.encrypt_data_gcm(plaintext, password)

def decrypt_data(encrypted_data: str, password: str) -> str:
    return SecurityUtils.decrypt_data_gcm(encrypted_data, password)