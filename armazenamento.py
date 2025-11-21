# ------------------------------
# MÓDULO: armazenamento.py (versão SQL)
# Finalidade: Gerenciar leitura, gravação e CRUD global dos dados via SQLite
# ------------------------------

import sqlite3
import os
import datetime

# ------------------------------
# CONFIGURAÇÃO DO BANCO
# ------------------------------
DATA_DIR = "data"
DB_NAME = f"{DATA_DIR}/sistema.db"

os.makedirs(DATA_DIR, exist_ok=True)


def conectar():
    """Abre conexão com o banco SQLite."""
    return sqlite3.connect(DB_NAME)


# ------------------------------
# CRIAÇÃO DAS TABELAS
# ------------------------------
def inicializar_banco():
    conn = conectar()
    cursor = conn.cursor()

    # Usuários / Administradores / Policiais (tudo cabe aqui)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            login TEXT UNIQUE,
            senha TEXT,
            telefone TEXT,
            matricula TEXT,
            patente TEXT,
            companhia TEXT,
            batalhao TEXT,
            data_cadastro TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            quantidade INTEGER,
            descricao TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS colaboradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            funcao TEXT,
            matricula TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lixeira (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origem TEXT,
            dado TEXT,
            data_exclusao TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS viaturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prefixo TEXT,
            placa TEXT,
            modelo TEXT,
            tipo TEXT,
            km_atual INTEGER,
            os_prime TEXT,
            data_cadastro TEXT
        );
    """)

    conn.commit()
    conn.close()


# ------------------------------
# CRUD GENÉRICO
# ------------------------------
def inserir(tabela, dados: dict):
    """Insere um registro em qualquer tabela."""
    conn = conectar()
    cursor = conn.cursor()

    colunas = ", ".join(dados.keys())
    valores = ", ".join(["?" for _ in dados])

    cursor.execute(
        f"INSERT INTO {tabela} ({colunas}) VALUES ({valores})",
        list(dados.values())
    )

    conn.commit()
    ultimo_id = cursor.lastrowid
    conn.close()
    return ultimo_id


def listar(tabela):
    """Retorna todos os registros de uma tabela."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {tabela}")
    registros = cursor.fetchall()

    conn.close()
    return registros


def buscar_por_id(tabela, id_registro):
    """Busca um único registro pelo ID."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {tabela} WHERE id=?", (id_registro,))
    registro = cursor.fetchone()

    conn.close()
    return registro


def atualizar(tabela, id_registro, dados: dict):
    """Atualiza um registro com base no ID."""
    conn = conectar()
    cursor = conn.cursor()

    set_clause = ", ".join([f"{k}=?" for k in dados])
    valores = list(dados.values()) + [id_registro]

    cursor.execute(
        f"UPDATE {tabela} SET {set_clause} WHERE id=?",
        valores
    )

    conn.commit()
    conn.close()


def deletar(tabela, id_registro):
    """Remove registro da tabela."""
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(f"DELETE FROM {tabela} WHERE id=?", (id_registro,))
    conn.commit()
    conn.close()


# ------------------------------
# BACKUP DO BANCO
# ------------------------------
def criar_backup():
    """Cria backup completo do arquivo do banco."""
    try:
        data_agora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = f"backup_{data_agora}.db"

        if os.path.exists(DB_NAME):
            with open(DB_NAME, "rb") as fsrc:
                with open(destino, "wb") as fdst:
                    fdst.write(fsrc.read())

        print(f"[OK] Backup criado: {destino}")

    except Exception as e:
        print(f"[ERRO] Falha no backup: {e}")
