from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

#Gestisce la crittografia con chiavi uniche per ogni contenitore.

def generate_key():
    """Genera una chiave AES casuale a 256 bit."""
    return os.urandom(32)

def encrypt(data: bytes, key: bytes):
    """Cifra i dati usando AES-GCM."""
    iv = os.urandom(12)
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(data) + encryptor.finalize()
    return iv + encryptor.tag + ciphertext

def decrypt(encrypted_data: bytes, key: bytes):
    """Decifra i dati cifrati con AES-GCM."""
    iv, tag, ciphertext = encrypted_data[:12], encrypted_data[12:28], encrypted_data[28:]
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()
