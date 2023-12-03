from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from base64 import b64encode, b64decode


def sha256(input_str):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(input_str.encode('utf-8'))
    return digest.finalize()

def encrypt_data(text, key):
    print("Encrypting:", text)
    print("With this key (string):" + key)

    #not this:
    ## Limit key size to 32 bytes (256 bits)
    #key = key_hash[:32]
    #print('2')
    #print(key.hex())

    #this works:
    #key=bytes.fromhex("198a1a4ee777d059d5f8e255deaa7f17")
    #print(key_hash[:16])

    key_hash = sha256(key)
    key=key_hash[:16]
    print(key)


    # Pad the data using PKCS7
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(text.encode('utf-8')) + padder.finalize()

    # Encrypt the data using AES with ECB mode

    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return b64encode(ciphertext).decode('utf-8')

def decrypt_data(encrypted_text, key):
    print("Decrypting:", encrypted_text)
    print("With this key (string):")
    print(key)
    print("SHA256:")
    key_hash = sha256(key)
    key = key_hash[:16]
    print(key)

    # Decode the Base64 encoded ciphertext
    ciphertext = b64decode(encrypted_text.encode('utf-8'))

    # Decrypt the data using AES with ECB mode
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the data using PKCS7
    unpadder = padding.PKCS7(128).unpadder()
    original_text = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    return original_text.decode('utf-8')
