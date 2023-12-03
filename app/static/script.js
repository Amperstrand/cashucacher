// Function to compute SHA-256 hash
function sha256(input) {
    return CryptoJS.SHA256(input).toString();
}


// Encryption function with PKCS7 padding
function encrypt_data(text, key) {
    console.log("encrypting: " + text);
    console.log("with this key (string):");
    console.log(key);
    console.log("sha256");
    console.log(sha256(key));
    key = sha256(key).substring(0, 32);  // Limit key size to 32 bytes (256 bits)
    console.log(key);

    // Encrypt the data using AES with ECB mode and PKCS7 padding
    var ciphertext = CryptoJS.AES.encrypt(text, CryptoJS.enc.Hex.parse(key), {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });

    return ciphertext.toString();
}

// Decryption function with PKCS7 unpadding
function decrypt_data(ciphertext, key) {
    key = sha256(key).substring(0, 32);  // Limit key size to 32 bytes (256 bits)

    // Decrypt the data using AES with ECB mode and PKCS7 padding
    var decrypted = CryptoJS.AES.decrypt(ciphertext, CryptoJS.enc.Hex.parse(key), {
        mode: CryptoJS.mode.ECB,
        padding: CryptoJS.pad.Pkcs7
    });

    return decrypted.toString(CryptoJS.enc.Utf8);
}


// Function to handle encryption form submission
function encryptAndShowResult() {
    const plaintext = document.getElementById("encryptInput").value;
    const key = document.getElementById("encryptionKey").value;
    const encryptedText = encrypt_data(plaintext, key);
    document.getElementById("result").innerHTML = `<p>Encrypted Text: ${encryptedText}</p>`;
}

// Function to handle decryption form submission
function decryptAndShowResult() {
    const ciphertext = document.getElementById("decryptInput").value;
    const key = document.getElementById("decryptionKey").value;
    const decryptedText = decrypt_data(ciphertext, key);
    document.getElementById("result").innerHTML = `<p>Decrypted Text: ${decryptedText}</p>`;
}
