from menu import menu_inicial
from database import inicializar_db, criar_backup_automatico
import os

if __name__ == "__main__":
    os.makedirs("data/backups", exist_ok=True)

    inicializar_db()
    try:
        menu_inicial()
    finally:
        criar_backup_automatico()
        print("Backup automático realizado. Sistema encerrado.")
