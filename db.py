import os
import json
import encryption

VAULT_FILE = "vault.sec"  # Name of the local encrypted vault file

def init_vault(master_password: str):
    """
    Creates a new vault file (empty JSON), encrypts it, and writes to disk.
    """
    if os.path.exists(VAULT_FILE):
        print("Vault file already exists. Overwrite? (y/N)")
        if input().lower() != "y":
            return
    
    # Basic structure for the vault
    data = {
        "containers": []
    }
    plaintext = json.dumps(data).encode("utf-8")
    ciphertext = encryption.encrypt_data(master_password, plaintext)
    
    with open(VAULT_FILE, "wb") as f:
        f.write(ciphertext)
    print("Vault initialized successfully.")

def load_vault(master_password: str) -> dict:
    """
    Decrypts and loads the vault from disk, returning the JSON data.
    """
    if not os.path.exists(VAULT_FILE):
        raise FileNotFoundError("Vault file not found.")
    with open(VAULT_FILE, "rb") as f:
        ciphertext = f.read()
    plaintext = encryption.decrypt_data(master_password, ciphertext)
    return json.loads(plaintext.decode("utf-8"))

def save_vault(master_password: str, data: dict):
    """
    Encrypts and saves the vault data to disk.
    """
    plaintext = json.dumps(data).encode("utf-8")
    ciphertext = encryption.encrypt_data(master_password, plaintext)
    with open(VAULT_FILE, "wb") as f:
        f.write(ciphertext)

def list_containers(master_password: str):
    """
    Lists all containers in the vault.
    """
    data = load_vault(master_password)
    containers = data.get("containers", [])
    if not containers:
        print("No containers found.")
        return
    for c in containers:
        print(f"Container ID: {c['id']}, Name: {c['name']}")

def create_container(master_password: str, name: str):
    """
    Creates a new container with a given name.
    """
    data = load_vault(master_password)
    containers = data.get("containers", [])
    new_id = len(containers) + 1  # simplistic ID generation
    containers.append({
        "id": new_id,
        "name": name,
        "secrets": []
    })
    data["containers"] = containers
    save_vault(master_password, data)
    print(f"Created container '{name}' with ID {new_id}.")

def add_secret(master_password: str, container_id: int, secret_text: str):
    """
    Adds a new secret to the specified container.
    """
    data = load_vault(master_password)
    containers = data.get("containers", [])
    container = next((c for c in containers if c["id"] == container_id), None)
    if not container:
        print("Container not found.")
        return
    secrets_list = container.get("secrets", [])
    new_secret_id = len(secrets_list) + 1
    secrets_list.append({
        "id": new_secret_id,
        "cryptedText": secret_text  # In a real system, you might re-encrypt individually, but this is a simpler approach
    })
    container["secrets"] = secrets_list
    save_vault(master_password, data)
    print(f"Added secret to container '{container['name']}' with ID {new_secret_id}.")

def show_container(master_password: str, container_id: int):
    """
    Shows the secrets in the specified container.
    """
    data = load_vault(master_password)
    containers = data.get("containers", [])
    container = next((c for c in containers if c["id"] == container_id), None)
    if not container:
        print("Container not found.")
        return
    print(f"Container: {container['name']}")
    for secret in container.get("secrets", []):
        print(f"  Secret ID: {secret['id']}, Text: {secret['cryptedText']}")
