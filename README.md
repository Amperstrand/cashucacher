# Cashucacher

**Hide your nuts.** A proof-of-concept for encrypting Cashu ecash tokens using LNURL-withdraw codes as encryption keys.

## What It Does

Cashucacher encrypts Cashu ecash tokens (V1) using AES-128-ECB with a key derived from an LNURL-withdraw code. The encrypted tokens can be served publicly alongside their LNURLw "keys" — only someone who knows to use the LNURLw as the decryption key can recover the Cashu token.

Use case: Distribute encrypted Cashu tokens "in plain sight" where the decryption keys are also withdraw codes.

## Quick Start

### Prerequisites

- Python 3.8+ or Docker
- Cashu notes (stored in `cashu_data/`)
- LNURL-withdraw codes (stored in `LNURLw.csv`)

### Option 1: Docker (Recommended)

```bash
# Build and run
docker-compose up

# Service will be available at http://localhost:3338
```

This starts:
- **cashucacher** on port 3338 (Flask API)
- **nutshell-wallet** on port 4448 (Cashu wallet for creating notes)

### Option 2: Local Python

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python run.py

# Service will be available at http://localhost:3338
```

## API Endpoints

### GET /lnurlw

Returns all encrypted cashu notes with their LNURLw keys.

### GET /lnurlw/&lt;index&gt;

Returns a specific encrypted cashu note by index.

Query parameters:
- `cache_size` (int, default=1): Number of notes to return
- `debug` (bool, default=false): Include full ciphertext in response

### Example Response

```json
{
  "index": 0,
  "current_lnurlw": "LNURL1DP68GURN8GHJ7...",
  "cachedcachu_list": [
    {
      "index": 0,
      "cashu_ciphertext": "cCF4/NQPxqsw4+mC...",
      "lnurlw": "LNURL1DP68GURN8GHJ7...",
      "partial_lnurlw": "LNURL1DP68GURN8GHJ7..."
    }
  ]
}
```

## Decryption

Use the provided `decrypt.py` CLI tool:

```bash
# Decrypt from URL
python decrypt.py "http://localhost:3338/lnurlw/0"

# The LNURLw code serves as the decryption key
```

## Project Structure

```
cashucacher/
├── run.py                 # Flask entry point
├── app/
│   ├── __init__.py        # Flask app setup
│   ├── lnurl_handler.py   # API routes
│   ├── encryption_module.py  # AES encryption
│   ├── utils.py           # File/CSV utilities
│   └── config.py          # Configuration
├── decrypt.py             # CLI decryption tool
├── test_encryption.py     # Unit tests
├── LNURLw.csv             # LNURL-withdraw codes
├── cashu_data/            # Cashu token files
├── docker-compose.yml     # Docker orchestration
└── Dockerfile             # Container definition
```

## Running Tests

```bash
# In Docker (recommended, has correct file paths)
docker-compose run cashucacher python -m pytest test_encryption.py -v

# Locally (requires cashu notes in /root/.cashu/)
source .venv/bin/activate
PYTHONPATH=. python -m pytest test_encryption.py -v
```

## Security Considerations

⚠️ **This is a proof-of-concept. Not recommended for production use.**

1. **AES-ECB mode**: The encryption uses AES-128-ECB, which is not semantically secure. Consider upgrading to AES-GCM for production.

2. **Key derivation**: Keys are derived by taking the first 16 bytes of SHA256(LNURLw). This is deterministic but not standard KDF.

3. **No authentication**: The API has no authentication — anyone can query all encrypted notes.

4. **LNURLw exposure**: The LNURLw codes (which are the decryption keys) are returned in the API response. Security through obscurity.

5. **Cashu note storage**: Notes are stored as plain text files. Ensure proper file permissions.

## License

MIT License - See [LICENSE](LICENSE) for details.
