import csv
import os
from flask import Flask, jsonify, render_template_string

import hashlib
import base64
import itertools





# use this to encrypt the cashu note
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
    print("With this key (string):")
    print(key)
    print("SHA256:")
    key_hash = sha256(key)

    #not this:
    ## Limit key size to 32 bytes (256 bits)
    #key = key_hash[:32]
    #print('2')
    #print(key.hex())

    #this works:
    #key=bytes.fromhex("198a1a4ee777d059d5f8e255deaa7f17")
    #print(key_hash[:16])
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

print(encrypt_data("cashuAeyJ0b2tlbiI6IFt7InByb29mcyI6IFt7ImlkIjogIkkyeU4raVJZZmt6VCIsICJhbW91bnQiOiAxLCAic2VjcmV0IjogIjQzZDgyMGY4NDViNjMyZmNmYThlNjk2YTgzMDRhZTZmMmYwMjE5OWM3Yzg3MTg5YTY3YTA4NzIwZTFkNTlkNzQiLCAiQyI6ICIwM2M5OTg1ZmM0ODIyM2IyMTkwMmU0NjBjN2QxMzcxMDc5MzhjYmU2ZGJiYTVjYmUwYWFkZjNiZDAzNmQ4NTg0M2UifV0sICJtaW50IjogImh0dHBzOi8vODMzMy5zcGFjZTozMzM4LyJ9XX0=", "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AMKJARGV3EXZAE0V9CXJTMKXYHKCMN4WFKZ7DT5WU6HZ4ZXG35K7MJKDG6HX3T4GEGHW4F59AF8JU2TGSMYV6Z3VD58G625WDQ5ZNJDXDU8ZMRH2K0"))

print(decrypt_data("CF4/NQPxqsw4+mCPPgA9+RkfICCLdvU4xS5SFnjUPG8xG3AEv5yVw3kFLItKpbP1/h6Yf7nJt+nEdHHQ7h4ZJIWeB6iDka+Nr9fQRxOkZid4R+mwkywomq2JsfcvySSjuAI8ZU2IZANBZVxrg9E596C1V8EOlH4GCAyXMKdr2viSoOns/1ejOu/yPRjXlkYLllIZIh5uc822D5ghUU9GilYlCYfa7BeDBT8m9ki6Eswu7Nr4HWbFHDjMDUnE+VD2xZdpYIXt6Bnm4ip4MbaSAX/fA8J6tcmmOhkn0x//oOkhFHBfEK/b2vB+Ph9zGIWKpIk9WIH1q/5Fdjm579Tq5zahP65jDK5C7pryX260o/THORtBCJ0/2R2WL/qPqPx5pFMGFshc2YcgmWCk/grcvvuf3nyZdWbF/K5NjicPAz9G4oazHvKrpbC0mOiIaKxmASUDbVZ7lqzjyjOYsrYP3Q==", "LNURL1DP68GURN8GHJ7MR9VAJKUEPWD3HXY6T5WVHXXMMD9AMKJARGV3EXZAE0V9CXJTMKXYHKCMN4WFKZ7DT5WU6HZ4ZXG35K7MJKDG6HX3T4GEGHW4F59AF8JU2TGSMYV6Z3VD58G625WDQ5ZNJDXDU8ZMRH2K0"))

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
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"No cashu note found: {file_path}. make sure that it exists")

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
    debug_info = [
        {
            "index": i,
            "lnurlw": lnurlw,
            "partial_lnurlw": lnurlw[:-1],
            "cashu_plaintext": read_decrypted_note(i),
            "cashu_ciphertext": encrypted_nuts[i]["cashu_ciphertext"]
        } for i, lnurlw in enumerate(lnurl_list)
    ]
    return jsonify(debug_info)

# New endpoint to show debug information for a specific index
@app.route('/debug/<int:index>', methods=['GET'])
def debug_index(index):
    if 0 <= index < len(lnurl_list):
        debug_info = {
            "index": index,
            "lnurlw": lnurl_list[index],
            "partial_lnurlw": lnurl_list[index][:-1],
            "cashu_plaintext": read_decrypted_note(index),
            "cashu_ciphertext": encrypted_nuts[index]["cashu_ciphertext"]
        }
        return jsonify(debug_info)
    else:
        return jsonify({"error": "Invalid index"}), 404

# New endpoint to show all encrypted Cashu information as a list
@app.route('/encrypted_cashu/', methods=['GET'])
def all_encrypted_cashu():
    all_encrypted_info = []
    for index in range(len(lnurl_list)):
        encrypted_info = {
            "index": index,
            "cashu_ciphertext": encrypted_nuts[index]["cashu_ciphertext"],
            "partial_lnurlw": lnurl_list[index][:-1]
        }
        all_encrypted_info.append(encrypted_info)

    return jsonify(all_encrypted_info)

# New endpoint to show encrypted Cashu information for a specific index
@app.route('/encrypted_cashu/<int:index>', methods=['GET'])
def encrypted_cashu_index(index):
    if 0 <= index < len(lnurl_list):
        encrypted_info = {
            "index": index,
            "cashu_ciphertext": encrypted_nuts[index]["cashu_ciphertext"],
            "partial_lnurlw": lnurl_list[index][:-1]
        }
        return jsonify(encrypted_info)
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

