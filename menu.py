# ============================================================
# SISTEMA ROTAM - VERSÃO FINAL 100% FUNCIONAL E CORRIGIDA
# ============================================================

import sqlite3
import os
import datetime
import re
import hashlib
import shutil
from pathlib import Path

# ---------------- CONFIGURAÇÕES ----------------
DATA_DIR = Path("data")
BACKUP_DIR = Path("backup")
DB_FILE = DATA_DIR / "rotam.db"
DATA_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# ---------------- UTILITÁRIOS ----------------
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa(seg=2):
    import time
    time.sleep(seg)

def aguardar_enter():
    input("\nPressione ENTER para continuar...")

def titulo(texto):
    limpar_tela()
    print("=" * 70)
    print(f"   {texto.upper()}   ".center(70))
    print("=" * 70)

# ---------------- BANCO DE DADOS ----------------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        telefone TEXT,
        matricula TEXT,
        patente TEXT,
        companhia TEXT,
        batalhao TEXT,
        data_cadastro TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS policiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patente TEXT NOT NULL,
        nome_guerra TEXT NOT NULL,
        matricula TEXT UNIQUE NOT NULL,
        telefone TEXT NOT NULL,
        companhia TEXT,
        batalhao TEXT,
        data_cadastro TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS viaturas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prefixo TEXT UNIQUE NOT NULL,
        placa TEXT UNIQUE NOT NULL,
        tipo TEXT NOT NULL,
        km_atual TEXT,
        os_prime TEXT,
        data_ultima_revisao TEXT,
        telefone_oficina TEXT,
        observacao TEXT,
        responsavel TEXT,
        data_cadastro TEXT
    )''')
    conn.commit()
    conn.close()

# ---------------- CLASSES E FUNÇÕES AUXILIARES ----------------
class User:
    @staticmethod
    def hash_senha(s): return hashlib.sha256(s.encode()).hexdigest()

    @staticmethod
    def login_valido(login, senha):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT senha FROM users WHERE login=?", (login.lower(),))
        row = c.fetchone()
        conn.close()
        return row and row[0] == User.hash_senha(senha)

    @staticmethod
    def salvar(**dados):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        dados['senha'] = User.hash_senha(dados['senha'])
        dados.setdefault('data_cadastro', datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
        cols = ', '.join(dados.keys())
        vals = ', '.join(['?'] * len(dados))
        c.execute(f"INSERT INTO users ({cols}) VALUES ({vals})", tuple(dados.values()))
        conn.commit()
        conn.close()

    @staticmethod
    def todos():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        rows = c.fetchall()
        conn.close()
        return rows

class Policial:
    @staticmethod
    def salvar(**dados):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        dados['data_cadastro'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        cols = ', '.join(dados.keys())
        vals = ', '.join(['?'] * len(dados))
        c.execute(f"INSERT INTO policiais ({cols}) VALUES ({vals})", tuple(dados.values()))
        conn.commit()
        conn.close()

    @staticmethod
    def todos():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM policiais")
        rows = c.fetchall()
        conn.close()
        return rows

class Viatura:
    @staticmethod
    def salvar(**dados):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        dados['data_cadastro'] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        cols = ', '.join(dados.keys())
        vals = ', '.join(['?'] * len(dados))
        c.execute(f"INSERT INTO viaturas ({cols}) VALUES ({vals})", tuple(dados.values()))
        conn.commit()
        conn.close()

    @staticmethod
    def todos():
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM viaturas")
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def por_prefixo(p):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM viaturas WHERE prefixo LIKE ?", (f"%{p}%",))
        rows = c.fetchall()
        conn.close()
        return rows

    @staticmethod
    def por_os_prime(os):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM viaturas WHERE os_prime = ?", (os,))
        rows = c.fetchall()
        conn.close()
        return rows

# ---------------- LISTAGENS ----------------
def listar_administradores():
    titulo("LISTA DE ADMINISTRADORES")
    admins = User.todos()
    if not admins:
        print("Nenhum administrador cadastrado.")
    else:
        print(f"{'ID':<4} {'Nome':<25} {'Login':<15} {'Telefone':<13} {'Matrícula':<12} {'Patente':<15}")
        print("-" * 90)
        for a in admins:
            print(f"{a[0]:<4} {a[1]:<25} {a[2]:<15} {a[4] or '-':<13} {a[5] or '-':<12} {a[6] or '-':<15}")
    aguardar_enter()

def listar_policiais():
    titulo("LISTA DE POLICIAIS")
    pols = Policial.todos()
    if not pols:
        print("Nenhum policial cadastrado.")
    else:
        print(f"{'ID':<4} {'Patente':<18} {'Nome Guerra':<20} {'Matrícula':<12} {'Telefone':<13}")
        print("-" * 90)
        for p in pols:
            print(f"{p[0]:<4} {p[1]:<18} {p[2]:<20} {p[3]:<12} {p[4]:<13}")
    aguardar_enter()

def listar_viaturas():
    titulo("LISTA DE VIATURAS")
    viaturas = Viatura.todos()
    if not viaturas:
        print("Nenhuma viatura cadastrada.")
    else:
        print(f"{'ID':<4} {'Prefixo':<10} {'Placa':<10} {'Tipo':<10} {'KM':<8} {'OS Prime':<10} {'Responsável'}")
        print("-" * 90)
        for v in viaturas:
            status = "BAIXADA" if v[5] else "DISPONÍVEL"
            print(f"{v[0]:<4} {v[1]:<10} {v[2]:<10} {v[3]:<10} {v[4] or '-':<8} {v[5] or '-':<10} {v[9] or '-'}  [{status}]")
    aguardar_enter()

# ---------------- PESQUISAS ----------------
def pesquisar_prefixo():
    titulo("PESQUISAR VIATURA POR PREFIXO")
    pref = input("Digite o prefixo (ou parte dele): ").strip()
    resultados = Viatura.por_prefixo(pref)
    if not resultados:
        print("Nenhuma viatura encontrada.")
    else:
        print(f"{'ID':<4} {'Prefixo':<10} {'Placa':<10} {'Tipo':<10} {'OS Prime':<10}")
        for v in resultados:
            print(f"{v[0]:<4} {v[1]:<10} {v[2]:<10} {v[3]:<10} {v[5] or '-':<10}")
    aguardar_enter()

def pesquisar_os_prime():
    titulo("PESQUISAR VIATURA POR OS PRIME")
    os = input("Digite a OS Prime (5 dígitos): ").strip()
    resultados = Viatura.por_os_prime(os)
    if not resultados:
        print("Nenhuma viatura encontrada com essa OS Prime.")
    else:
        print(f"{'Prefixo':<10} {'Placa':<10} {'KM':<8} {'Responsável'}")
        for v in resultados:
            print(f"{v[1]:<10} {v[2]:<10} {v[4] or '-':<8} {v[9] or '-'}")
    aguardar_enter()

# ---------------- RELATÓRIO ----------------
def relatorio_viaturas():
    titulo("RELATÓRIO DE SITUAÇÃO DAS VIATURAS")
    todas = Viatura.todos()
    total = len(todas)
    baixadas = [v for v in todas if v[5]]  # tem OS Prime
    disponiveis = total - len(baixadas)

    print(f"Total de viaturas cadastradas : {total}")
    print(f"Viaturas DISPONÍVEIS          : {disponiveis}")
    print(f"Viaturas BAIXADAS (OS Prime)  : {len(baixadas)}")
    print("=" * 70)

    if baixadas:
        print(f"{'Prefixo':<10} {'Placa':<10} {'Tipo':<10} {'KM':<8} {'OS Prime':<10} {'Responsável'}")
        print("-" * 70)
        for v in baixadas:
            print(f"{v[1]:<10} {v[2]:<10} {v[3]:<10} {v[4] or '-':<8} {v[5]:<10} {v[9] or '-'}")
    else:
        print("Nenhuma viatura baixada no momento.")
    aguardar_enter()

# ---------------- CADASTROS ----------------
def cadastrar_admin():
    titulo("CADASTRO DE ADMINISTRADOR")
    while True:
        nome = input("Nome completo: ").strip()
        if re.match(r"^[A-Za-zÀ-ÿ\s]{4,}$", nome):
            break
        print("Nome inválido!")

    login = input("Login: ").strip().lower()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE login=?", (login,))
    while c.fetchone():
        print("Login já existe!")
        login = input("Login: ").strip().lower()
    conn.close()

    senha = input("Senha (mín. 4 caracteres): ")
    while len(senha) < 4:
        senha = input("Senha muito curta! Digite novamente: ")

    tel = input("Telefone (opcional): ").strip()
    mat = input("Matrícula (opcional): ").strip()
    pat = input("Patente (opcional): ").strip()
    comp = input("Companhia (opcional): ").strip()
    bat = input("Batalhão (opcional): ").strip()

    User.salvar(nome=nome, login=login, senha=senha, telefone=tel, matricula=mat,
                patente=pat, companhia=comp, batalhao=bat)

    # Cria policial automaticamente
    Policial.salvar(patente=pat or "Admin", nome_guerra=nome.split()[0],
                    matricula=mat or "ADMIN", telefone=tel or "00000000000",
                    companhia=comp, batalhao=bat)

    print(f"\nAdministrador {nome} cadastrado com sucesso!")
    pausa()

def cadastrar_policial():
    titulo("CADASTRO DE POLICIAL")
    patentes = ["Soldado", "Cabo", "3º Sargento", "2º Sargento", "1º Sargento",
                "Subtenente", "Aspirante", "Tenente", "Capitão", "Major", "Ten-Coronel", "Coronel"]
    print("Patentes disponíveis:")
    for i, p in enumerate(patentes, 1):
        print(f"{i:2}. {p}")
    while True:
        try:
            escolha = int(input("Escolha a patente: "))
            if 1 <= escolha <= len(patentes):
                patente = patentes[escolha-1]
                break
        except:
            pass
        print("Opção inválida!")

    nome_guerra = input("Nome de guerra: ").strip()
    while not nome_guerra:
        nome_guerra = input("Nome de guerra obrigatório: ").strip()

    matricula = input("Matrícula: ").strip()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM policiais WHERE matricula=?", (matricula,))
    while c.fetchone() or not matricula:
        print("Matrícula já existe ou inválida!")
        matricula = input("Matrícula: ").strip()
    conn.close()

    telefone = input("Telefone (11 dígitos): ").strip()
    while not re.fullmatch(r"\d{11}", telefone):
        telefone = input("Telefone inválido! Digite 11 dígitos: ").strip()

    companhia = input("Companhia: ").strip()
    batalhao = input("Batalhão: ").strip()

    Policial.salvar(patente=patente, nome_guerra=nome_guerra, matricula=matricula,
                    telefone=telefone, companhia=companhia, batalhao=batalhao)
    print(f"Policial {nome_guerra} cadastrado!")
    pausa()

def cadastrar_viatura():
    titulo("CADASTRO DE VIATURA")
    while True:
        prefixo = input("Prefixo (único): ").strip().upper()
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT 1 FROM viaturas WHERE prefixo=?", (prefixo,))
        if c.fetchone():
            print("Prefixo já cadastrado!")
        elif prefixo:
            break
    while True:
        placa = input("Placa (única): ").strip().upper()
        c.execute("SELECT 1 FROM viaturas WHERE placa=?", (placa,))
        if c.fetchone():
            print("Placa já cadastrada!")
        elif placa:
            break
    conn.close()

    tipo = input("Tipo (Moto / 4 Rodas): ").strip().title()
    while tipo not in ["Moto", "4 Rodas"]:
        tipo = input("Tipo inválido! Digite Moto ou 4 Rodas: ").strip().title()

    km = input("KM atual (opcional): ").strip() or None
    os_prime = input("OS Prime Prime (5 dígitos, opcional): ").strip() or None
    if os_prime and not (os_prime.isdigit() and len(os_prime) == 5):
        print("OS Prime deve ter 5 dígitos!")
        os_prime = None
    data_rev = input("Data última revisão (opcional): ").strip() or None
    tel_oficina = input("Telefone oficina (opcional): ").strip() or None
    obs = input("Observação (opcional): ").strip() or None
    resp = input("Responsável (opcional): ").strip() or None

    Viatura.salvar(prefixo=prefixo, placa=placa, tipo=tipo, km_atual=km, os_prime=os_prime,
                   data_ultima_revisao=data_rev, telefone_oficina=tel_oficina,
                   observacao=obs, responsavel=resp)
    print(f"Viatura {prefixo} cadastrada com sucesso!")
    pausa()

# ---------------- BACKUP ----------------
def backup_completo():
    titulo("BACKUP COMPLETO")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_zip = BACKUP_DIR / f"backup_rotam_{timestamp}"
    shutil.make_archive(str(nome_zip), 'zip', DATA_DIR)
    print(f"Backup criado com sucesso!")
    print(f"Arquivo: {nome_zip}.zip")
    pausa()

# ---------------- MENU PRINCIPAL ----------------
def menu_principal():
    while True:
        titulo("MENU PRINCIPAL - SISTEMA ROTAM")
        print("1. Cadastrar Viatura")
        print("2. Listar Viaturas")
        print("3. Pesquisar por Prefixo")
        print("4. Pesquisar por OS Prime")
        print("5. Relatório de Situação das Viaturas")
        print("6. Cadastrar Policial")
        print("7. Listar Policiais")
        print("8. Listar Administradores")
        print("9. Fazer Backup Completo")
        print("0. Sair")
        op = input("\nOpção: ").strip()

        if op == "1": cadastrar_viatura()
        elif op == "2": listar_viaturas()
        elif op == "3": pesquisar_prefixo()
        elif op == "4": pesquisar_os_prime()
        elif op == "5": relatorio_viaturas()
        elif op == "6": cadastrar_policial()
        elif op == "7": listar_policiais()
        elif op == "8": listar_administradores()
        elif op == "9": backup_completo()
        elif op == "0": break
        else:
            print("Opção inválida!")
            pausa()

# ---------------- EXECUÇÃO ----------------
if __name__ == "__main__":
    init_db()

    # Primeiro acesso: força cadastro de admin
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    tem_admin = c.fetchone()[0] > 0
    conn.close()

    if not tem_admin:
        print("Primeiro acesso! Cadastre o administrador inicial.")
        cadastrar_admin()

    while True:
        titulo("SISTEMA ROTAM - CONTROLE DE VIATURAS")
        print("1. Fazer Login")
        print("2. Cadastrar Novo Administrador")
        print("0. Sair")
        op = input("\nOpção: ").strip()

        if op == "1":
            login = input("Login: ").strip().lower()
            senha = input("Senha: ")
            if User.login_valido(login, senha):
                print(f"\nBem-vindo, {login.upper()}!")
                pausa(1)
                menu_principal()
            else:
                print("Login ou senha incorretos!")
                pausa(2)
        elif op == "2":
            cadastrar_admin()
        elif op == "0":
            print("Sistema encerrado. Até logo!")
            break