# ============================================================
# administradores.py (versão orientada a objetos com SQL)
# ============================================================

import sqlite3
import datetime
from uteis import limpar_tela, pausa, aguardar_enter
from policiais import cadastrar_policial

DB_FILE = "data/sistema.db"

# ---------------------------- CLASSE ADMINISTRADOR ----------------------------
class Administrador:
    def __init__(self, id=None, nome=None, login=None, senha=None, telefone=None,
                 matricula=None, patente=None, companhia=None, batalhao=None,
                 data_cadastro=None):
        self.id = id
        self.nome = nome
        self.login = login
        self.senha = senha
        self.telefone = telefone
        self.matricula = matricula
        self.patente = patente
        self.companhia = companhia
        self.batalhao = batalhao
        self.data_cadastro = data_cadastro or datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # ---------------------------- MÉTODOS ESTÁTICOS ----------------------------
    @staticmethod
    def criar_tabela():
        """Cria a tabela de administradores no banco, se não existir."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS administradores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            login TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            telefone TEXT,
            matricula TEXT,
            patente TEXT,
            companhia TEXT,
            batalhao TEXT,
            data_cadastro TEXT
        )
        """)
        conn.commit()
        conn.close()
    
    @staticmethod
    def login(login_user, senha):
        """Verifica login e senha no banco."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM administradores WHERE login=? AND senha=?", (login_user, senha))
        row = cursor.fetchone()
        conn.close()
        if row:
            print(f"Bem-vindo, {row[1]}!")
            pausa(1)
            return Administrador(*row)
        else:
            print("Login ou senha incorretos!")
            pausa(2)
            return None

    @staticmethod
    def listar():
        """Lista todos os administradores cadastrados."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM administradores")
        rows = cursor.fetchall()
        conn.close()

        limpar_tela()
        if not rows:
            print("Nenhum administrador cadastrado.")
            aguardar_enter()
            return

        print(f"{'ID':<3} {'Nome':<25} {'Login':<15} {'Telefone':<12} {'Matrícula':<10} {'Patente':<10} {'Companhia':<10} {'Batalhão'}")
        print("-"*100)
        for row in rows:
            print(f"{row[0]:<3} {row[1]:<25} {row[2]:<15} {row[4] or '-':<12} {row[5] or '-':<10} {row[6] or '-':<10} {row[7] or '-':<10} {row[8] or '-'}")
        aguardar_enter()

    # ---------------------------- MÉTODOS DE INSTÂNCIA ----------------------------
    def salvar(self, cadastro_policial=False):
        """Insere ou atualiza o administrador no banco."""
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        if not self.id:
            # Inserir novo administrador
            cursor.execute("""
            INSERT INTO administradores (nome, login, senha, telefone, matricula, patente, companhia, batalhao, data_cadastro)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (self.nome, self.login, self.senha, self.telefone, self.matricula,
                  self.patente, self.companhia, self.batalhao, self.data_cadastro))
            self.id = cursor.lastrowid
        else:
            # Atualizar administrador existente (opcional)
            cursor.execute("""
            UPDATE administradores
            SET nome=?, login=?, senha=?, telefone=?, matricula=?, patente=?, companhia=?, batalhao=?, data_cadastro=?
            WHERE id=?
            """, (self.nome, self.login, self.senha, self.telefone, self.matricula,
                  self.patente, self.companhia, self.batalhao, self.data_cadastro, self.id))

        conn.commit()
        conn.close()
        print(f"Administrador '{self.nome}' cadastrado/atualizado com sucesso!")

        # Se for cadastro inicial, cria policial automaticamente
        if cadastro_policial:
            cadastrar_policial(
                nome=self.nome,
                matricula=self.matricula,
                telefone=self.telefone,
                companhia=self.companhia,
                batalhao=self.batalhao,
                patente=self.patente
            )
        aguardar_enter()

# ---------------------------- FUNÇÕES AUXILIARES ----------------------------
def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]{2,}$", nome.strip()))

def login_disponivel(login_user):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM administradores WHERE login=?", (login_user,))
    exists = cursor.fetchone()
    conn.close()
    return not exists

def senha_valida(senha):
    return len(senha) >= 4

# ---------------------------- INTERFACE DE CADASTRO ----------------------------
def cadastrar_administrador_interface(realizar_cadastro=False):
    limpar_tela()
    print("=== CADASTRO DE ADMINISTRADOR ===" if not realizar_cadastro else "=== REALIZAR CADASTRO ===")

    while True:
        nome = input("Nome completo: ").strip()
        if validar_nome(nome):
            break
        print("Nome inválido! Use apenas letras e espaços, mínimo 2 caracteres.")

    while True:
        login_user = input("Login: ").strip()
        if login_disponivel(login_user):
            break
        print("Login inválido ou já existe!")

    while True:
        senha = input("Senha (mínimo 4 caracteres): ").strip()
        if senha_valida(senha):
            break
        print("Senha inválida! Digite ao menos 4 caracteres.")

    telefone = input("Telefone (opcional): ").strip()
    matricula = input("Matrícula (opcional): ").strip()
    patente = input("Patente (opcional): ").strip()
    companhia = input("Companhia (opcional): ").strip()
    batalhao = input("Batalhão (opcional): ").strip()

    admin = Administrador(
        nome=nome,
        login=login_user,
        senha=senha,
        telefone=telefone,
        matricula=matricula,
        patente=patente,
        companhia=companhia,
        batalhao=batalhao
    )
    admin.salvar(cadastro_policial=realizar_cadastro)
