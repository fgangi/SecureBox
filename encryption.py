import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Constants for key derivation and encryption
SALT_SIZE = 16
KEY_LEN = 32
ITERATIONS = 100_000
NONCE_SIZE = 12

def derive_key(master_password: str, salt: bytes) -> bytes:
    """
    Derive a 256-bit key from the master password using PBKDF2-HMAC-SHA256.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(master_password.encode("utf-8"))

def encrypt_data(master_password: str, plaintext: bytes) -> bytes:
    """
    Encrypt data with AES-GCM.
    Returns the concatenation of: salt + nonce + ciphertext.
    """
    salt = os.urandom(SALT_SIZE)
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    # The final data includes salt + nonce + ciphertext (tag is inside ciphertext in AESGCM)
    return salt + nonce + ciphertext

def decrypt_data(master_password: str, encrypted: bytes) -> bytes:
    """
    Decrypt data with AES-GCM.
    Expects: salt + nonce + ciphertext.
    """
    salt = encrypted[:SALT_SIZE]
    nonce = encrypted[SALT_SIZE:SALT_SIZE + NONCE_SIZE]
    ciphertext = encrypted[SALT_SIZE + NONCE_SIZE:]
    key = derive_key(master_password, salt)
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)
