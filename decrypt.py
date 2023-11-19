import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def decrypt_string(ciphertext, lnurlw):
    key = hashlib.sha256(lnurlw.encode('utf-8')).digest()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()

    decoded_ct = base64.urlsafe_b64decode(ciphertext)

    decrypted_data = decryptor.update(decoded_ct) + decryptor.finalize()

    # Use PKCS#7 unpadding
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data.decode('utf-8')

# Example usage:
lnurlw_key = "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AMKJARGV3EXZAE0V9CXJTMKXYHKCMN4WFKZ7DT5WU6HZ4ZXG35K7MJKDG6HX3T4GEGHW4F59AZ52WFHGFX4V6NCGEEX7URTGFX8G6JYD4U42FUGE4K"
encrypted_message = "QP4A9aOYzP5Rwt6ek-CjFR1yZXQfvRI067Vj0XG8g-XUh6T8zWpCWTWThomG-W1rB_Jq65HEomvIrI_-enwqSl6Ao2rRHyitJMYtzkJrrvygvLLFjA3BgSBQAVxiSHP4MrTSDZa9vLSxlJItHrjFoqV-Wbt_DMGknlbHIsS1s7QWnOyiLl4DOO_VxZJJJPfySwEcGBGMl6fpn1zDZ1OtruEFmlYFFex-i19RYvB78xusXdux7eT-QQN7SHvEUhJmbxNCU_WGOlOMIc-JVWR7PzQVjG_ajq0iP8VQu6Rkfna73LJF6nUiEUjHyKAMQz1_C2wL72i1juwXGur0SKi-5JKv-q7rfm83SbZypwcBMWlo39n1afALESR9NrbE5K35z3JFXwjmYoXELFzGkJ0YhE2jhtyqNubOmZvAfB2IfNyvmwBbTgQ-M01r-lqbjv3LKT7KHxPNAle6iXa-nLwBfg=="
print("Encrypted message:", encrypted_message)

decrypted_message = decrypt_string(encrypted_message, lnurlw_key)
print("Decrypted message:", decrypted_message)
