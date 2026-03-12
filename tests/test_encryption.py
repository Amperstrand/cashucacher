import unittest
import base64
import importlib.util
import os
import sys

# Direct module import to avoid triggering app/__init__.py
def load_module_directly(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Get the app directory path
app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'app')
security_utils_path = os.path.join(app_dir, 'security_utils.py')

# Load security_utils directly
security_utils = load_module_directly('security_utils', security_utils_path)
encrypt_data = security_utils.encrypt_data
decrypt_data = security_utils.decrypt_data


class EncryptionTest(unittest.TestCase):
    """Tests for the AES-256-GCM encryption module."""

    def setUp(self):
        self.lnurlw_key = "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AMKJARGV3EXZAE0V9CXJTMKXYHKCMN4WFKZ7DT5WU6HZ4ZXG35K7MJKDG6HX3T4GEGHW4F59AF8JU2TGSMYV6Z3VD58G625WDQ5ZNJDXDU8ZMRH2K0"
        self.plaintext = "cashuAeyJ0b2tlbiI6IFt7InByb29mcyI6IFt7ImlkIjogIkkyeU4raVJZZmt6VCIsICJhbW91bnQiOiAxLCAic2VjcmV0IjogIjQzZDgyMGY4NDViNjMyZmNmYThlNjk2YTgzMDRhZTZmMmYwMjE5OWM3Yzg3MTg5YTY3YTA4NzIwZTFkNTlkNzQiLCAiQyI6ICIwM2M5OTg1ZmM0ODIyM2IyMTkwMmU0NjBjN2QxMzcxMDc5MzhjYmU2ZGJiYTVjYmUwYWFkZjNiZDAzNmQ4NTg0M2UifV0sICJtaW50IjogImh0dHBzOi8vODMzMy5zcGFjZTozMzM4LyJ9XX0=="

    def test_encryption_produces_valid_base64(self):
        """Encryption should produce a valid base64 string."""
        ciphertext = encrypt_data(self.plaintext, self.lnurlw_key)
        self.assertIsInstance(ciphertext, str)
        # Should be valid base64
        try:
            decoded = base64.urlsafe_b64decode(ciphertext)
            self.assertGreater(len(decoded), 0)
        except Exception as e:
            self.fail(f"Encrypted data is not valid base64: {e}")

    def test_encryption_is_non_deterministic(self):
        """Each encryption should produce different ciphertext (random salt/nonce)."""
        ciphertext1 = encrypt_data(self.plaintext, self.lnurlw_key)
        ciphertext2 = encrypt_data(self.plaintext, self.lnurlw_key)
        self.assertNotEqual(ciphertext1, ciphertext2,
                            "Encryption should be non-deterministic due to random salt/nonce")

    def test_encryption_decryption_roundtrip(self):
        """Encrypting then decrypting should return the original plaintext."""
        ciphertext = encrypt_data(self.plaintext, self.lnurlw_key)
        decrypted = decrypt_data(ciphertext, self.lnurlw_key)
        self.assertEqual(decrypted, self.plaintext)

    def test_wrong_key_fails(self):
        """Decrypting with the wrong key should fail."""
        ciphertext = encrypt_data(self.plaintext, self.lnurlw_key)
        wrong_key = "WRONG_KEY_12345"
        with self.assertRaises(ValueError):
            decrypt_data(ciphertext, wrong_key)

    def test_empty_plaintext(self):
        """Encrypting empty string should work."""
        ciphertext = encrypt_data("", self.lnurlw_key)
        decrypted = decrypt_data(ciphertext, self.lnurlw_key)
        self.assertEqual(decrypted, "")

    def test_ciphertext_contains_salt_nonce_tag(self):
        """Ciphertext should contain salt (32 bytes) + nonce (12 bytes) + tag (16 bytes)."""
        ciphertext = encrypt_data(self.plaintext, self.lnurlw_key)
        decoded = base64.urlsafe_b64decode(ciphertext)
        # Minimum size: 32 (salt) + 12 (nonce) + plaintext + 16 (tag)
        self.assertGreater(len(decoded), 32 + 12 + 16)


if __name__ == '__main__':
    unittest.main()
