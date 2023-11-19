import csv
import os
from flask import Flask, jsonify, render_template_string



# use this to encrypt the cashu note
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
#from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib
import base64

def encrypt_string(message, lnurlw):
    key = hashlib.sha256(lnurlw.encode('utf-8')).digest()  # This will be a 32-byte key for AES-256, adjust as needed
    print(key)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()

    # Use PKCS#7 padding
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode('utf-8')) + padder.finalize()

    ct = encryptor.update(padded_data) + encryptor.finalize()
    return base64.urlsafe_b64encode(ct).decode('utf-8')

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


                   #"cashu_ciphertext": encrypt_string(read_decrypted_note(i), hashlib.sha256(lnurlw.encode('utf-8')).digest()),
# Generate encrypted nuts for each lnurlw

#key = hashlib.sha256(lnurlw.encode('utf-8')).digest()  # This will be a 32-byte key for AES-256, adjust as needed

encrypted_nuts = [{"index": i,
                   "cashu_plaintext": read_decrypted_note(i),
                   "cashu_ciphertext": encrypt_string(read_decrypted_note(i), lnurlw),
                   "key" : hashlib.sha256(lnurlw.encode('utf-8')).hexdigest(),
                   "encryption_key_full": lnurlw, "encryption_key_hint": lnurlw[:-1]} for i, lnurlw in enumerate(lnurl_list)]


@app.route('/lnurlw', methods=['GET'])
def lnurlw():
    global current_index
    if current_index < len(lnurl_list) - 1:
        current_index += 1
    current_lnurlw = lnurl_list[current_index] if lnurl_list else None

    # Extract index and lnurlw for the current lnurlw
    current_info = {"index": current_index, "lnurlw": current_lnurlw}

    # Generate links to /encryptednut/$index for all future nuts
    encrypted_nuts = [
        {"index": i, "link": f"/encryptednut/{i}"} for i in range(current_index, len(lnurl_list))
    ]

    return jsonify({"current_info": current_info, "encrypted_nuts": encrypted_nuts})

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

