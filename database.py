import sqlite3

#Gestisce la memorizzazione sicura dei contenitori e segreti.
#SQLite è leggero e sicuro
#Crittografia integrata nei dati sensibili.

def init_db():
    """Inizializza il database e crea le tabelle necessarie."""
    conn = sqlite3.connect("securebox.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS containers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        encryption_key BLOB
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS secrets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        container_id INTEGER,
        name TEXT,
        content BLOB,
        FOREIGN KEY (container_id) REFERENCES containers(id)
    )
    """)
    conn.commit()
    conn.close()
