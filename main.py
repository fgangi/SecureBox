import argparse
from getpass import getpass
import sys

import db
import cloud

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # Print the usage, then print the error on a new line
        self.print_usage(sys.stderr)
        self.exit(2, f"\nerror: {message}\n")

def main():
    # Custom usage string for the main parser with single-line entries for each command
    custom_usage = (
        "python main.py [command] [arguments]\n\n"
        "Commands:\n"
        "  init                                         - Initialize a new vault.\n"
        "  list                                         - List all containers in the vault.\n"
        "  create-container <name>                      - Create a new container with the specified name.\n"
        "  delete-container <container_id>              - Delete the container identified by its ID.\n"
        "  show <container_id>                          - Display all secrets in the specified container.\n"
        "  add-secret <container_id> <secret_text>      - Add a secret to the specified container.\n"
        "  edit-secret <container_id> <secret_id>       - Edit an existing secret.\n"
        "  backup-upload                                - Upload the vault file to Google Drive.\n"
        "  backup-download                              - Download the vault file from Google Drive.\n\n"
        "Use \"python main.py <command> -h\" for detailed help on a specific command."
    )

    parser = CustomArgumentParser(
        description="SecureBox CLI",
        usage=custom_usage,
        add_help=False
    )
    
    subparsers = parser.add_subparsers(dest="command")

    # Vault initialization and listing
    subparsers.add_parser("init", help="Initialize a new vault")
    subparsers.add_parser("list", help="List all containers in the vault")

    # Container commands
    create_parser = subparsers.add_parser("create-container", help="Create a new container")
    create_parser.add_argument("name", help="Name of the container")

    delete_parser = subparsers.add_parser("delete-container", help="Delete a container")
    delete_parser.add_argument("container_id", type=int, help="ID of the container to delete")

    # Secret commands
    add_secret_parser = subparsers.add_parser("add-secret", help="Add a secret to a container")
    add_secret_parser.add_argument("container_id", type=int, help="ID of the container")
    add_secret_parser.add_argument("secret_text", help="The secret text")

    show_parser = subparsers.add_parser("show", help="Show a container's secrets")
    show_parser.add_argument("container_id", type=int, help="ID of the container")

    edit_secret_parser = subparsers.add_parser("edit-secret", help="Edit a secret")
    edit_secret_parser.add_argument("container_id", type=int, help="ID of the container")
    edit_secret_parser.add_argument("secret_id", type=int, help="ID of the secret")

    # Cloud backup commands
    subparsers.add_parser("backup-upload", help="Upload the vault to Google Drive")
    subparsers.add_parser("backup-download", help="Download the vault from Google Drive")

    # If no arguments are provided, print custom usage and exit
    if len(sys.argv) == 1:
        parser.print_usage()
        sys.exit(1)

    args = parser.parse_args()

    # Command handling
    if args.command == "init":
        master_password = getpass("Set a master password for your vault: ")
        db.init_vault(master_password)
    elif args.command == "list":
        master_password = getpass("Enter your master password: ")
        db.list_containers(master_password)
    elif args.command == "create-container":
        master_password = getpass("Enter your master password: ")
        db.create_container(master_password, args.name)
    elif args.command == "delete-container":
        master_password = getpass("Enter your master password: ")
        db.delete_container(master_password, args.container_id)
    elif args.command == "add-secret":
        master_password = getpass("Enter your master password: ")
        db.add_secret(master_password, args.container_id, args.secret_text)
    elif args.command == "show":
        master_password = getpass("Enter your master password: ")
        db.show_container(master_password, args.container_id)
    elif args.command == "edit-secret":
        master_password = getpass("Enter your master password: ")
        db.edit_secret(master_password, args.container_id, args.secret_id)
    elif args.command == "backup-upload":
        cloud.upload_vault()
    elif args.command == "backup-download":
        cloud.download_vault()
    else:
        parser.print_usage()

if __name__ == "__main__":
    main()
