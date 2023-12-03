import csv

def load_lnurl_list(file_path):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Assuming only one row, strip spaces from lnurlws
            return [lnurlw.strip() for lnurlw in next(reader, [])]
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} is not a file.")

def read_decrypted_note(offset):
    file_path = f"/root/.cashu/1_sat_cashu_note_at_offset_{offset}.txt"
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"No cashu note found: {file_path}. Make sure that it exists")
        return None  # Consider returning a meaningful value or raising an exception here
