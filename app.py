import csv
import os
from flask import Flask, jsonify, render_template_string

import hashlib
import base64
import itertools





# use this to encrypt the cashu note

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
import hashlib

# Function to compute SHA-256 hash
def sha256(input):
    return hashlib.sha256(input.encode()).hexdigest()

# Encryption function with PKCS7 padding
def encrypt_data(text, key):
    print("encrypting: " + text)
    print("with this key (string):")
    print (key)
    print("sha256")
    print(sha256(key))
    key = sha256(key)[:32]  # Limit key size to 32 bytes (256 bits)
    print(key)

    # Create a cipher object with AES and ECB mode
    cipher = Cipher(algorithms.AES(key.encode()), modes.ECB(), backend=default_backend())

    # Create a padder using PKCS7
    padder = padding.PKCS7(algorithms.AES.block_size).padder()

    # Encrypt the padded data
    encryptor = cipher.encryptor()
    padded_data = padder.update(text.encode()) + padder.finalize()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return b64encode(ciphertext).decode()

# Decryption function with PKCS7 unpadding
def decrypt_data(ciphertext, key):
    key = sha256(key)[:32]  # Limit key size to 32 bytes (256 bits)

    # Create a cipher object with AES and ECB mode
    cipher = Cipher(algorithms.AES(key.encode()), modes.ECB(), backend=default_backend())

    # Decrypt the data
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(b64decode(ciphertext)) + decryptor.finalize()

    # Create an unpadder using PKCS7
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    # Unpad the decrypted data
    original_text = unpadder.update(decrypted_data) + unpadder.finalize()

    return original_text.decode()

# Example usage
secret_key = "your_secret_key"
plain_text = "Hello, World!"

encrypted_text = encrypt_data(plain_text, secret_key)
print("Encrypted:", encrypted_text)

decrypted_text = decrypt_data(encrypted_text, secret_key)
print("Decrypted:", decrypted_text)

print(encrypt_data("cashuAeyJ0b2tlbiI6IFt7InByb29mcyI6IFt7ImlkIjogIkkyeU4raVJZZmt6VCIsICJhbW91bnQiOiAxLCAic2VjcmV0IjogIjQzZDgyMGY4NDViNjMyZmNmYThlNjk2YTgzMDRhZTZmMmYwMjE5OWM3Yzg3MTg5YTY3YTA4NzIwZTFkNTlkNzQiLCAiQyI6ICIwM2M5OTg1ZmM0ODIyM2IyMTkwMmU0NjBjN2QxMzcxMDc5MzhjYmU2ZGJiYTVjYmUwYWFkZjNiZDAzNmQ4NTg0M2UifV0sICJtaW50IjogImh0dHBzOi8vODMzMy5zcGFjZTozMzM4LyJ9XX0=", "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AMKJARGV3EXZAE0V9CXJTMKXYHKCMN4WFKZ7DT5WU6HZ4ZXG35K7MJKDG6HX3T4GEGHW4F59AF8JU2TGSMYV6Z3VD58G625WDQ5ZNJDXDU8ZMRH2K0"))

#print(decrypt_data("84qShBFxgmuqNSL6IVCJEhz4kIKvQwbaFJ7ZkrOGfhtVk8qz677FGFBQ08mm+US+EpTBLJDPWlNNts1cGcrdONMgHOlIAcnTI2nPUB9ZBNFfpdLZiUtxOIUvnuCddGIKUHKupu4EGrv1UC8pO0faZCSGeaf+SsYtJZi1PBiaEzMjoRMbujo/ALYElnCH9lnv+1JQkGvVyw0/nqNalqc4pVeMnVDT+bqdNVJE8jCuwCVs+vEVo2nZSHqnIsTUibQz3WGGCDGN1M7JaER9n86+4qXIdSBsgZTa+9a+pVMbc1SWd/54sAqdULUWQ5MUZAfpkFEO6w4dNylm1MDS47RcORk4tNDhUMvP4Sbgcg6QBoN79l6On4r1qh8OD0wXfB485dpu0f3azTEFizzBs0a0geraxj0kYsU0YFBSCKX70drCnO7mcgkKDOCaJE2LaH4iAagYRe4tSXt502/zbdOeOQ==", "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AMKJARGV3EXZAE0V9CXJTMKXYHKCMN4WFKZ7DT5WU6HZ4ZXG35K7MJKDG6HX3T4GEGHW4F59AF8JU2TGSMYV6Z3VD58G625WDQ5ZNJDXDU8ZMRH2K0"))

app = Flask(__name__)

# Get the absolute path to the LNURLw.csv file
lnurl_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'LNURLw.csv')

# Check if LNURLw.csv is a file
if not os.path.isfile(lnurl_file_path):
    raise FileNotFoundError(f"{lnurl_file_path} is not a file.")

# Load lnurlws from the CSV file and strip spaces
lnurl_list = []

with open(lnurl_file_path, 'r') as file:
    reader = csv.reader(file)
    # Assuming only one row, strip spaces from lnurlws
    lnurl_list = [lnurlw.strip() for lnurlw in next(reader, [])]

# Function to read decrypted cashu note from file
def read_decrypted_note(offset):
    file_path = f"/root/.cashu/1_sat_cashu_note_at_offset_{offset}.txt"
    with open(file_path, 'r') as file:
        return file.read().strip()

# Index to keep track of the current position
current_index = 0


# Generate encrypted nuts for each lnurlw

enable_plaintext=True
#enable_plaintext=False
encrypted_nuts = [
    {
        "index": i,
        **({"plaintext": {
            "cashu_plaintext": read_decrypted_note(i),
            "full_lnurlw": lnurlw,
            "sha256sum(full_lnurlw) (encryption key)": hashlib.sha256(lnurlw.encode('utf-8')).hexdigest(),
        }} if enable_plaintext else {}),
        "cashu_ciphertext": encrypt_data(read_decrypted_note(i), lnurlw),
        "partial_lnurlw": lnurlw[:-1]
    } for i, lnurlw in enumerate(lnurl_list)
]


@app.route('/lnurlw', methods=['GET'])
def lnurlw():
    global current_index
    current_lnurlw = lnurl_list[current_index] if lnurl_list else None

    # Extract index and lnurlw for the current lnurlw
    current_lnurlw = {"index": current_index, "lnurlw": current_lnurlw}

    # Generate links to /encryptednut/$index for all future nuts
    encrypted_nut_urls = [
            {"index": i, "partial_lnurlw": lnurl_list[i][:-1], "link": f"/encryptednut/{i}"} for i in range(current_index, len(lnurl_list))
    ]

    if current_index < len(lnurl_list) - 1:
        current_index += 1

    return jsonify({"current_lnurlw": current_lnurlw, "encrypted_nut_urls" : encrypted_nut_urls, "encrypted_nuts": encrypted_nuts})

#not really usefull
@app.route('/encryptednut', methods=['GET'])
def encryptednut():
    return jsonify(encrypted_nuts[current_index])

@app.route('/encryptednut/<index>', methods=['GET'])
def get_encryptednut_by_index(index):
    try:
        index = int(index)
        encrypted_nut = encrypted_nuts[index]
        return jsonify(encrypted_nut)
    except (ValueError, IndexError):
        return jsonify({"error": "Invalid index"}), 404

# Routes for debugging
@app.route('/debug', methods=['GET'])
def debug():
    debug_info = [{"index": i, "lnurlw": lnurlw, "encrypted_nut": encrypted_nuts[i]} for i, lnurlw in enumerate(lnurl_list)]
    return jsonify(debug_info)

@app.route('/debug/<int:index>', methods=['GET'])
def debug_index(index):
    if 0 <= index < len(lnurl_list):
        debug_info = {
            "encrypted_nut": encrypted_nuts[index],
            "index": index,
            "lnurlw": lnurl_list[index]
        }
        return jsonify(debug_info)
    else:
        return jsonify({"error": "Invalid index"}), 404

# Route for the main endpoint '/'
@app.route('/', methods=['GET'])
def home():
    return render_template_string("""
    <h1>Welcome to CashuCacher!</h1>
    <ul>
        <li><a href="{{ url_for('lnurlw') }}">/lnurlw</a></li>
        <li><a href="{{ url_for('encryptednut') }}">/encryptednut</a></li>
        <li><a href="{{ url_for('get_encryptednut_by_index', index=0) }}">/encryptednut/0</a></li>
        <li><a href="{{ url_for('debug') }}">/debug</a></li>
        <li><a href="{{ url_for('debug_index', index=0) }}">/debug/0</a></li>
    </ul>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3338)

