const CryptoJS = window.CryptoJS;

function encryptAndShowResult() {
  const { value: plaintext } = document.getElementById('encryptInput');
  const { value: encryptionKey } = document.getElementById('encryptionKey');

  try {
    const encryptedData = encryptData(plaintext, encryptionKey);
    document.getElementById('result').innerHTML = `<strong>Encrypted Data:</strong><br>${encryptedData}`;
  } catch (error) {
    console.error('Encryption Error:', error.message);
  }
}

function decryptAndShowResult() {
  const { value: encryptedData } = document.getElementById('decryptInput');
  const { value: decryptionKey } = document.getElementById('decryptionKey');

  try {
    const decryptedData = decryptData(encryptedData, decryptionKey);
    document.getElementById('result').innerHTML = `<strong>Decrypted Data:</strong><br>${decryptedData}`;
  } catch (error) {
    console.error('Decryption Error:', error.message);
  }
}

function encryptData(data, secretKey) {
  return CryptoJS.AES.encrypt(data, secretKey).toString();
}

function decryptData(encryptedData, secretKey) {
  return CryptoJS.AES.decrypt(encryptedData, secretKey).toString(CryptoJS.enc.Utf8);
}

