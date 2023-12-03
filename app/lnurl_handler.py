from flask import Blueprint, jsonify, render_template
from .encryption_module import encrypt_data, decrypt_data
from .utils import load_lnurl_list, read_decrypted_note

lnurl_routes = Blueprint('lnurl', __name__)

LNURL_FILE_PATH = "./LNURLw.csv"

lnurl_list = load_lnurl_list(LNURL_FILE_PATH)
current_index = 0

class EncryptedNut:
    def __init__(self, index, cashu_ciphertext, lnurlw):
        self.index = index
        self.cashu_ciphertext = cashu_ciphertext
        self.lnurlw = lnurlw
        characters_to_remove = 1
        self.partial_lnurlw = lnurlw[:-characters_to_remove]

    def to_json(self):
        return {"index": self.index, "cashu_ciphertext": self.cashu_ciphertext, "lnurlw": self.lnurlw}

def create_encrypted_nuts(lnurl_list):
    encrypted_nuts = [
        EncryptedNut(
            index=i,
            cashu_ciphertext=encrypt_data(read_decrypted_note(i), lnurlw),
            lnurlw=lnurlw
        ) for i, lnurlw in enumerate(lnurl_list)
    ]
    return encrypted_nuts

encrypted_nuts = create_encrypted_nuts(lnurl_list)

@lnurl_routes.route('/lnurlw', methods=['GET'])
def lnurlw():
    global current_index
    current_lnurlw = lnurl_list[current_index] if lnurl_list else None
    current_lnurlw = {"index": current_index, "lnurlw": current_lnurlw}

    encrypted_nut_urls = [
        {"index": i, "partial_lnurlw": lnurl_list[i][:-1], "link": f"/encryptednut/{i}"} for i in range(current_index, len(lnurl_list))
    ]

    if current_index < len(lnurl_list) - 1:
        current_index += 1

    return jsonify({"current_lnurlw": current_lnurlw, "encrypted_nut_urls": encrypted_nut_urls, "encrypted_nuts": [nut.to_json() for nut in encrypted_nuts]})
