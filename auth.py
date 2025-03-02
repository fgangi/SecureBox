import os
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

USERS_FILE = "users.json"
SALT_SIZE = 16           # 16 bytes salt
KEY_LEN = 32             # 256-bit key
ITERATIONS = 100_000     # Number of iterations for PBKDF2

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    else:
        return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def register_user(username: str, master_password: str):
    users = load_users()
    if username in users:
        print("User already registered!")
        return
    salt = os.urandom(SALT_SIZE)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    hashed_password = kdf.derive(master_password.encode("utf-8"))
    users[username] = {"salt": salt.hex(), "hashed_password": hashed_password.hex()}
    save_users(users)
    print("User registered successfully.")

def authenticate_user(username: str, master_password: str) -> bool:
    users = load_users()
    if username not in users:
        print("User not found. Please register first.")
        return False
    user_data = users[username]
    salt = bytes.fromhex(user_data["salt"])
    stored_hash = bytes.fromhex(user_data["hashed_password"])
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    try:
        kdf.verify(master_password.encode("utf-8"), stored_hash)
        return True
    except Exception:
        return False
