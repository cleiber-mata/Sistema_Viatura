import sqlite3
import shutil
import json
import os
from datetime import datetime
from uteis import limpar_tela, pausa

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
                (tabela, json.dumps(dados), datetime.now().isoformat()))
    con.commit()
    con.close()

def restaurar_item_lixeira():
    con = conectar()
    cur = con.cursor()

    # Seleciona tudo da lixeira
    cur.execute("SELECT id, tabela, dados FROM lixeira")
    itens = cur.fetchall()

    if not itens:
        print("Lixeira vazia. Nada para restaurar.")
        pausa(2)
        return

    for item in itens:
        lixo_id, tabela, dados_json = item

        # Converte o JSON para dict
        dados = json.loads(dados_json)

        # Monta SQL dinamicamente
        colunas = ", ".join(dados.keys())
        placeholders = ", ".join(["?"] * len(dados))
        valores = tuple(dados.values())

        sql_insert = f"INSERT INTO {tabela} ({colunas}) VALUES ({placeholders})"

        try:
            cur.execute(sql_insert, valores)
            # Remove o item restaurado da lixeira
            cur.execute("DELETE FROM lixeira WHERE id = ?", (lixo_id,))
        except Exception as e:
            print(f"Erro ao restaurar item {lixo_id}: {e}")

    con.commit()
    con.close()
    print("Itens restaurados com sucesso!")
    pausa(2)



def apagar_lixeira():
    con = conectar()
    cur = con.cursor()
    cur.execute("DELETE FROM lixeira")
    con.commit()
    con.close()
    
def ver_lixeira():
    con = conectar()
    try:
        cur = con.cursor()
        cur.execute("SELECT * FROM lixeira")
        itens = cur.fetchall()
        return itens
    finally:
        con.close()


def restaurar_sistema():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    inicializar_db()


def criar_backup_automatico():
    if os.path.exists(DB_PATH):
        backup_path = os.path.join(BACKUP_DIR, "backup_rotam.db")
        shutil.copy(DB_PATH, backup_path)
        
def menu_lixeira():
    while True:
        limpar_tela()
        print("=== MENU LIXEIRA ===")
        print("1. Ver lixeira.")
        print("2. Restaurar itens da lixeira.")
        print("3. Apagar itens da lixeira permanentemente.")
        print("0. Sair")

        opc = input("Opção: ").strip()

        if opc == "1":
            itens = ver_lixeira()
            if not itens:
                print("Lixeira vazia.")
            else:
                print("\n=== ITENS NA LIXEIRA ===")
                for item in itens:
                    print(item)
            input("\nPressione Enter para continuar...")
        elif opc == "2":
            restaurar_item_lixeira()
        elif opc == "3":
            apagar_lixeira()
            print("Itens apagados permanentemente.")
            pausa(2)
        elif opc == "0":
            pausa(1)
            break
        else:
            print("Opção inválida!")
            pausa(2)
