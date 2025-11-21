import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = "data/rotam.db"
BACKUP_DIR = "data/backups"

def conectar():
    return sqlite3.connect(DB_PATH)

def inicializar_db():
    con = conectar()
    cur = con.cursor()

    # Tabela de admins
    cur.execute("""
        CREATE TABLE IF NOT EXISTS administradores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    # Policiais
    cur.execute("""
        CREATE TABLE IF NOT EXISTS policiais(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            matricula TEXT NOT NULL UNIQUE
        )
    """)

    # Viaturas
    cur.execute("""
        CREATE TABLE IF NOT EXISTS viaturas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefixo TEXT NOT NULL UNIQUE,
            placa TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL
        )
    """)

    # Lixeira
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lixeira(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tabela TEXT NOT NULL,
            dados TEXT NOT NULL,
            data TEXT NOT NULL
        )
    """)

    con.commit()
    con.close()


def mover_para_lixeira(tabela, dados):
    con = conectar()
    cur = con.cursor()
    cur.execute("INSERT INTO lixeira (tabela, dados, data) VALUES (?, ?, ?)",
                (tabela, str(dados), datetime.now().isoformat()))
    con.commit()
    con.close()


def restaurar_lixeira():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM lixeira")
    con.commit()
    con.close()


def apagar_lixeira():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM lixeira")
    con.commit()
    con.close()


def restaurar_sistema():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    inicializar_db()


def criar_backup_automatico():
    if os.path.exists(DB_PATH):
        backup_path = os.path.join(BACKUP_DIR, "backup_rotam.db")
        shutil.copy(DB_PATH, backup_path)
