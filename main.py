from auth import login
from vault import create_container, list_containers
from ui import text_editor
from backup import send_backup
import curses
# main Gestisce il flusso principale dell'applicazione.
#Gestisce il menu principale
#Integra autenticazione, gestione contenitori e backup
def main():
    key = login()
    if not key:
        print("Autenticazione fallita!")
        return
    
    while True:
        print("\n1. Crea Contenitore")
        print("2. Mostra Contenitori")
        print("3. Modifica Segreti")
        print("4. Backup via Gmail")
        print("5. Esci")
        choice = input("Scelta: ")

        if choice == "1":
            name = input("Nome del contenitore: ")
            create_container(name, key)

        elif choice == "2":
            print(list_containers())

        elif choice == "3":
            curses.wrapper(text_editor)

        elif choice == "4":
            send_backup()

        elif choice == "5":
            break

if __name__ == "__main__":
    main()
