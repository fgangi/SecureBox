import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from io import BytesIO

VAULT_FILE = "vault.sec"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"

def get_drive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next time
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return build("drive", "v3", credentials=creds)

def upload_vault():
    """
    Upload the local vault.sec to Google Drive.
    """
    if not os.path.exists(VAULT_FILE):
        print("Vault file not found. Nothing to upload.")
        return
    service = get_drive_service()

    file_metadata = {
        "name": VAULT_FILE
    }
    media = MediaFileUpload(VAULT_FILE, resumable=True)
    # You can search if the file already exists and update it, but let's just create a new one for simplicity
    created_file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    print(f"Uploaded vault to Drive with file ID: {created_file.get('id')}")

def download_vault():
    """
    Download the vault.sec file from Google Drive to local storage.
    Overwrites the local vault.sec if found.
    """
    service = get_drive_service()
    # For simplicity, let's search by name. You can also search by file ID.
    query = f"name='{VAULT_FILE}' and trashed=false"
    response = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    files = response.get("files", [])
    if not files:
        print("No vault.sec found in Drive.")
        return
    file_id = files[0]["id"]
    request = service.files().get_media(fileId=file_id)
    fh = BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Download progress: {int(status.progress() * 100)}%")
    with open(VAULT_FILE, "wb") as f:
        f.write(fh.getvalue())
    print("Vault downloaded successfully.")
