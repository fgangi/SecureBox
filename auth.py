import hashlib
import os
import base64
from getpass import getpass

#Gestisce il login degli utenti con password sicura usando PBKDF2:
#PBKDF2 evita attacchi di forza bruta generando una chiave sicura.
#getpass() nasconde la password durante l'inserimento.

SALT = b'secure_salt'

def derive_key(password: str):
    """Genera una chiave sicura a partire dalla password dell'utente."""
    return base64.urlsafe_b64encode(hashlib.pbkdf2_hmac('sha256', password.encode(), SALT, 100000))

def login():
    """Richiede la password all'utente e restituisce la chiave derivata."""
    password = getpass("Inserisci la password del vault: ")
    return derive_key(password)
