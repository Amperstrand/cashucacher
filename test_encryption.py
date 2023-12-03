import unittest
from encryption_module import encrypt_data, decrypt_data

class EncryptionTest(unittest.TestCase):

    def setUp(self):
        self.lnurlw_key = "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AMKJARGV3EXZAE0V9CXJTMKXYHKCMN4WFKZ7DT5WU6HZ4ZXG35K7MJKDG6HX3T4GEGHW4F59AF8JU2TGSMYV6Z3VD58G625WDQ5ZNJDXDU8ZMRH2K0"
        self.plaintext = "cashuAeyJ0b2tlbiI6IFt7InByb29mcyI6IFt7ImlkIjogIkkyeU4raVJZZmt6VCIsICJhbW91bnQiOiAxLCAic2VjcmV0IjogIjQzZDgyMGY4NDViNjMyZmNmYThlNjk2YTgzMDRhZTZmMmYwMjE5OWM3Yzg3MTg5YTY3YTA4NzIwZTFkNTlkNzQiLCAiQyI6ICIwM2M5OTg1ZmM0ODIyM2IyMTkwMmU0NjBjN2QxMzcxMDc5MzhjYmU2ZGJiYTVjYmUwYWFkZjNiZDAzNmQ4NTg0M2UifV0sICJtaW50IjogImh0dHBzOi8vODMzMy5zcGFjZTozMzM4LyJ9XX0=="
        self.ciphertext = "cCF4/NQPxqsw4+mCPPgA9+RkfICCLdvU4xS5SFnjUPG8xG3AEv5yVw3kFLItKpbP1/h6Yf7nJt+nEdHHQ7h4ZJIWeB6iDka+Nr9fQRxOkZid4R+mwkywomq2JsfcvySSjuAI8ZU2IZANBZVxrg9E596C1V8EOlH4GCAyXMKdr2viSoOns/1ejOu/yPRjXlkYLllIZIh5uc822D5ghUU9GilYlCYfa7BeDBT8m9ki6Eswu7Nr4HWbFHDjMDUnE+VD2xZdpYIXt6Bnm4ip4MbaSAX/fA8J6tcmmOhkn0x//oOkhFHBfEK/b2vB+Ph9zGIWKpIk9WIH1q/5Fdjm579Tq5zahP65jDK5C7pryX260o/THORtBCJ0/2R2WL/qPqPx5pFMGFshc2YcgmWCk/grcvvuf3nyZdWbF/K5NjicPAz9G4oazHvKrpbC0mOiIaKxmASUDbVZ7lqzjyjOYsrYP3Q=="

    def test_encryption(self):
        print (encrypt_data(self.plaintext, self.lnurlw_key))
        self.assertEqual(encrypt_data(self.plaintext, self.lnurlw_key), self.ciphertext)

    def test_decryption(self):
        print (decrypt_data(self.ciphertext, self.lnurlw_key))
        self.assertEqual(decrypt_data(self.ciphertext, self.lnurlw_key), self.plaintext)

if __name__ == '__main__':
    unittest.main()