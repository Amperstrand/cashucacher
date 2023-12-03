from flask import Blueprint, jsonify, request
from .encryption_module import encrypt_data, decrypt_data
from .utils import load_lnurl_list, read_decrypted_note
import json

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

    def to_json(self, ciphertext_only=False):
        json_output = {"index": self.index}
        if not ciphertext_only:
            json_output["cashu_ciphertext"] = self.cashu_ciphertext
            json_output["lnurlw"] = self.lnurlw
            json_output["partial_lnurlw"] = self.partial_lnurlw
        return json_output

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
def get_all_lnurlw():
    global current_index
    print(f"current_index: {current_index}")
    debug = request.args.get('debug', default=False, type=bool)

    # Fetch all lnurlw items
    lnurlw_list = []
    end_index=len(encrypted_nuts)
    for index in range(current_index, end_index):
        current_lnurlw = lnurl_list[index]
        cachedcachu_list = [encrypted_nuts[i] for i in range(index, end_index)]
        response_data = {
            "index": index,
            "current_lnurlw": current_lnurlw,
            "cachedcachu_list": [c.to_json(ciphertext_only=debug) for c in cachedcachu_list]
        }
    current_index += 1
    return json.dumps(response_data, separators=(',', ':'), sort_keys=False, indent=4)

@lnurl_routes.route('/lnurlw/<int:index>', methods=['GET'])
def get_lnurlw_by_index(index):
    cache_size = request.args.get('cache_size', default=1, type=int)
    debug = request.args.get('debug', default=False, type=bool)
    
    if 0 <= index < len(lnurl_list):
        end_index = min(index + cache_size, len(encrypted_nuts))
        current_lnurlw = lnurl_list[index] 
        cachedcachu_list = [encrypted_nuts[i] for i in range(index, end_index)]

        # Arrange the keys in the desired order
        response_data = {
            "index": index,
            "current_lnurlw": current_lnurlw,
            "cachedcachu_list": [c.to_json(ciphertext_only=debug) for c in cachedcachu_list]
        }
        return json.dumps(response_data, separators=(',', ':'), sort_keys=False, indent=4)

    else:
        return jsonify({"message": "Invalid index."}), 404