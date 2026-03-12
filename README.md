# Cashucacher

**Lightning as a key distribution mechanism.**

Encrypt Cashu ecash tokens using LNURL-withdraw codes as keys, then use Lightning to deliver those keys.

## The Core Idea

Consider this scenario:
- You want to give someone a Cashu token worth **1000 sats**
- But they're offline, or you want to schedule the delivery
- You publish an **encrypted token** publicly (anyone can see it)
- When ready, you send them an **LNURLw worth 1 sat** via Lightning
- That 1 sat LNURLw is **ALSO the decryption key** for the 1000 sat Cashu token

The "aha" moment: **LNURLw codes are human-readable strings that can be transmitted over Lightning**. Lightning becomes the key distribution channel.

## Why This Is Interesting

| Aspect | Description |
|--------|-------------|
| **Steganographic key** | An LNURLw looks like a withdraw code (which it is!) but it's also a decryption key |
| **Lightning as notification** | Sending 1 sat over Lightning signals "your key is ready" |
| **Asymmetric value** | The LNURLw might be worth 1 sat, but it unlocks 1000 sats |
| **No new infrastructure** | Uses existing Lightning/LNURL tooling |

## Use Cases

### 1. Scheduled Gifting
Pre-encrypt tokens and publish them. On someone's birthday, send the LNURLw keys via Lightning.

### 2. Offline Recipients
Encrypt tokens now, deliver keys later when recipient is online.

### 3. Dead Man's Switch
Publish encrypted tokens. If something happens to you, trusted parties receive the LNURLw keys.

### 4. Deniable Value Storage
Store "encrypted data" publicly. Only those who receive Lightning payments know it's Cashu.

### 5. Multi-Party Distribution
Give each person a different LNURLw. Each code decrypts a different token from the same public pool.

## What This Is Not

- **Not a wallet** - This is a key distribution mechanism, not a Cashu wallet
- **Not production-ready** - Proof-of-concept for exploring offline payment concepts
- **Not for high-value tokens** - The security model assumes low-value experimentation

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
│   ├── encryption_module.py  # AES-256-GCM encryption
│   ├── security_utils.py   # Cryptographic utilities
│   ├── utils.py           # File/CSV utilities
│   └── config.py          # Configuration
├── decrypt.py             # CLI decryption tool
├── tests/                # Unit tests
├── LNURLw.csv             # LNURL-withdraw codes
├── cashu_data/            # Cashu token files
├── docker-compose.yml     # Docker orchestration
└── Dockerfile             # Container definition
```

## Running Tests

```bash
# In Docker (recommended, has correct file paths)
docker-compose run cashucacher python -m pytest tests/test_encryption.py -v

# Locally (requires cashu notes in /root/.cashu/)
source .venv/bin/activate
PYTHONPATH=. python -m pytest tests/test_encryption.py -v
```

## Security Considerations

⚠️ **This is a proof-of-concept. Not recommended for high-value tokens.**

### Encryption (Updated March 2025)

The project now uses **AES-256-GCM** with **PBKDF2-HMAC-SHA256** key derivation:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| **Algorithm** | AES-256-GCM | Authenticated encryption (confidentiality + integrity) |
| **Key Derivation** | PBKDF2-HMAC-SHA256 | Prevents brute force attacks |
| **Iterations** | 100,000 | NIST-recommended work factor |
| **Salt** | 32 bytes random | Prevents rainbow table attacks |
| **Nonce** | 12 bytes random | Prevents replay attacks |
| **Tag** | 16 bytes GMAC | Ensures data integrity |

### Remaining Considerations

1. **No authentication**: The API has no authentication — anyone can query all encrypted notes.

2. **LNURLw exposure**: The LNURLw codes (which are the decryption keys) are returned in the API response. Security through obscurity.

3. **Cashu note storage**: Notes are stored as plain text files. Ensure proper file permissions.

4. **Key strength**: Security depends on the entropy of LNURLw codes. Use unique, unpredictable codes.
## License

MIT License - See [LICENSE](LICENSE) for details.
