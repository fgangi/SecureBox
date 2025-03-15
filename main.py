import argparse
from getpass import getpass

import db
import cloud

def main():
    parser = argparse.ArgumentParser(description="SecureBox CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Vault initialization and listing
    subparsers.add_parser("init", help="Initialize a new vault")
    subparsers.add_parser("list", help="List all containers")

    # Container commands
    create_parser = subparsers.add_parser("create-container", help="Create a new container")
    create_parser.add_argument("name", help="Name of the container")

    delete_parser = subparsers.add_parser("delete-container", help="Delete a container")
    delete_parser.add_argument("container_id", type=int)

    # Secret commands
    add_secret_parser = subparsers.add_parser("add-secret", help="Add a secret to a container")
    add_secret_parser.add_argument("container_id", type=int)
    add_secret_parser.add_argument("secret_text", help="The secret text")

    show_parser = subparsers.add_parser("show", help="Show a container's secrets")
    show_parser.add_argument("container_id", type=int)

    edit_secret_parser = subparsers.add_parser("edit-secret", help="Edit a secret")
    edit_secret_parser.add_argument("container_id", type=int)
    edit_secret_parser.add_argument("secret_id", type=int)
    edit_secret_parser.add_argument("new_text", help="New text for the secret")

    # Cloud backup commands
    subparsers.add_parser("backup-upload", help="Upload the vault to Google Drive")
    subparsers.add_parser("backup-download", help="Download the vault from Google Drive")

    args = parser.parse_args()

    if args.command == "init":
        master_password = getpass("Set a master password for your vault: ")
        db.init_vault(master_password)
    elif args.command == "list":
        master_password = getpass("Enter your master password: ")
        db.list_containers(master_password)
    elif args.command == "create-container <name>":
        master_password = getpass("Enter your master password: ")
        db.create_container(master_password, args.name)
    elif args.command == "delete-container <container_id>":
        master_password = getpass("Enter your master password: ")
        db.delete_container(master_password, args.container_id)
    elif args.command == "add-secret <container_id> <secret_text>":
        master_password = getpass("Enter your master password: ")
        db.add_secret(master_password, args.container_id, args.secret_text)
    elif args.command == "show <container_id>":
        master_password = getpass("Enter your master password: ")
        db.show_container(master_password, args.container_id)
    elif args.command == "edit-secret <container_id> <secret_id> <new_text>":
        master_password = getpass("Enter your master password: ")
        db.edit_secret(master_password, args.container_id, args.secret_id, args.new_text)
    elif args.command == "backup-upload":
        cloud.upload_vault()
    elif args.command == "backup-download":
        cloud.download_vault()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
