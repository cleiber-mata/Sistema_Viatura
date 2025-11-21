# ============================================================
# SISTEMA COMPLETO DE GERENCIAMENTO DE VIATURAS, POLICIAIS E ADMINISTRADORES
# ============================================================
import os
import sqlite3
import datetime
import re
import shutil
from getpass import getpass

DB_FILE = "data/sistema_rotam.db"
BACKUP_DIR = "backup"
LIXEIRA_TABLES = ["usuarios_lixeira", "policiais_lixeira", "viaturas_lixeira"]

# ======================== UTILITÁRIOS ========================
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa(segundos=2):
    import time
    time.sleep(segundos)

def aguardar_enter():
    input("\nPressione Enter para continuar...")

def criar_backup_automatico():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    backup_file = os.path.join(BACKUP_DIR, "backup_rotam.db")
    if os.path.exists(DB_FILE):
        shutil.copy2(DB_FILE, backup_file)

# ======================== BANCO DE DADOS ========================
def conectar():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    return conn

def inicializar_db():
    conn = conectar()
    c = conn.cursor()
    
    # Usuários
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios(
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
    
    # Policiais
    c.execute('''CREATE TABLE IF NOT EXISTS policiais(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patente TEXT,
        nome_guerra TEXT,
        matricula TEXT,
        telefone TEXT,
        companhia TEXT,
        batalhao TEXT,
        data_cadastro TEXT
    )''')
    
    # Viaturas
    c.execute('''CREATE TABLE IF NOT EXISTS viaturas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        prefixo TEXT UNIQUE,
        placa TEXT UNIQUE,
        tipo TEXT,
        km_atual TEXT,
        os_prime TEXT,
        data_ultima_revisao TEXT,
        telefone_oficina TEXT,
        observacao TEXT,
        responsavel TEXT,
        data_cadastro TEXT
    )''')

    # Lixeiras
    for table in ["usuarios","policiais","viaturas"]:
        lixeira = f"{table}_lixeira"
        c.execute(f'''CREATE TABLE IF NOT EXISTS {lixeira} AS SELECT * FROM {table} WHERE 0''')
    
    conn.commit()
    conn.close()

# ======================== VALIDAÇÕES ========================
def nome_valido(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]{2,}$", nome.strip()))

def senha_valida(senha):
    return bool(re.match(r"^\d{6}$", senha.strip()))

def validar_telefone(telefone):
    return not telefone or (telefone.isdigit() and len(telefone)==11)

def validar_tipo_viatura(tipo):
    return tipo.lower() in ['moto','4 rodas']

def gerar_login(nome_completo, conn):
    partes = nome_completo.strip().split()
    if len(partes) < 2:
        partes.append("user")
    primeiro = re.sub(r'[^a-zA-Z0-9]', '', partes[0].lower())
    ultimo = re.sub(r'[^a-zA-Z0-9]', '', partes[-1].lower())
    base = f"{primeiro}.{ultimo}"
    login_final = base
    contador = 1
    c = conn.cursor()
    while c.execute("SELECT 1 FROM usuarios WHERE login=?", (login_final,)).fetchone():
        login_final = f"{base}{contador}"
        contador += 1
    return login_final

# ======================== ADMINISTRADORES ========================
def cadastrar_usuario():
    conn = conectar()
    c = conn.cursor()
    limpar_tela()
    print("=== CADASTRO DE ADMINISTRADOR ===")
    while True:
        nome = input("Nome completo: ").strip()
        if nome_valido(nome):
            break
        print("Nome inválido! Use pelo menos 2 letras.")
    login_user = gerar_login(nome, conn)
    print(f"Login sugerido: {login_user}")
    
    while True:
        senha = getpass("Senha (6 dígitos numéricos): ").strip()
        if not senha_valida(senha):
            print("Senha inválida! Deve ter 6 dígitos numéricos.")
            continue
        senha_conf = getpass("Confirme a senha: ").strip()
        if senha != senha_conf:
            print("Senhas não conferem!")
            continue
        break
    
    telefone = input("Telefone (opcional, 11 dígitos): ").strip() or None
    while telefone and not validar_telefone(telefone):
        print("Telefone inválido!")
        telefone = input("Telefone (opcional, 11 dígitos): ").strip() or None

    matricula = input("Matrícula (opcional): ").strip() or None
    patente = input("Patente (opcional): ").strip() or None
    companhia = input("Companhia (opcional): ").strip() or None
    batalhao = input("Batalhão (opcional): ").strip() or None
    data_cadastro = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    c.execute('''INSERT INTO usuarios(nome, login, senha, telefone, matricula, patente, companhia, batalhao, data_cadastro)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                 (nome, login_user, senha, telefone, matricula, patente, companhia, batalhao, data_cadastro))
    conn.commit()
    
    # Cadastrar automaticamente como policial
    c.execute('''INSERT INTO policiais(patente, nome_guerra, matricula, telefone, companhia, batalhao, data_cadastro)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (patente, nome, matricula, telefone, companhia, batalhao, data_cadastro))
    conn.commit()
    conn.close()
    print(f"Administrador '{nome}' cadastrado com sucesso!")
    pausa(2)

def listar_administradores():
    conn = conectar()
    c = conn.cursor()
    limpar_tela()
    print("=== LISTA DE ADMINISTRADORES ===")
    rows = c.execute("SELECT id,nome,login,telefone,matricula,patente,companhia,batalhao FROM usuarios").fetchall()
    if not rows:
        print("Nenhum administrador cadastrado.")
        aguardar_enter()
        return
    print(f"{'ID':<3} {'Nome':<25} {'Login':<20} {'Telefone':<12} {'Matrícula':<10} {'Patente':<15} {'Companhia':<10} {'Batalhão'}")
    print("-"*100)
    for u in rows:
        print(f"{u[0]:<3} {u[1]:<25} {u[2]:<20} {u[3] or '-':<12} {u[4] or '-':<10} {u[5] or '-':<15} {u[6] or '-':<10} {u[7] or '-'}")
    aguardar_enter()
    conn.close()

def login():
    conn = conectar()
    c = conn.cursor()
    limpar_tela()
    print("=== LOGIN ADMINISTRADOR ===")
    login_user = input("Login: ").strip().lower()
    senha = getpass("Senha: ").strip()
    c.execute("SELECT * FROM usuarios WHERE LOWER(login)=? AND senha=?", (login_user, senha))
    if c.fetchone():
        print("Login realizado com sucesso!")
        pausa(1)
        conn.close()
        return True
    print("Login ou senha incorretos!")
    pausa(2)
    conn.close()
    return False

# ======================== POLICIAIS ========================
def cadastrar_policial():
    conn = conectar()
    c = conn.cursor()
    limpar_tela()
    print("=== CADASTRO DE POLICIAL ===")
    patentes = ["Soldado", "Cabo", "Terceiro-Sargento", "Segundo-Sargento",
                "Primeiro-Sargento", "Subtenente", "Aspirante", "Tenente",
                "Capitão", "Major", "Tenente-Coronel", "Coronel"]
    for i, p in enumerate(patentes,1):
        print(f"{i}. {p}")
    while True:
        try:
            opc = int(input("Escolha a patente (número): ").strip())
            if 1 <= opc <= len(patentes):
                patente = patentes[opc-1]
                break
        except:
            pass
        print("Opção inválida!")
    
    while True:
        nome_guerra = input("Nome de guerra: ").strip()
        if nome_valido(nome_guerra):
            break
        print("Nome inválido!")
    
    matricula = input("Matrícula: ").strip()
    telefone = input("Telefone (DDD+Número, 11 dígitos): ").strip()
    while not validar_telefone(telefone):
        print("Telefone inválido!")
        telefone = input("Telefone (DDD+Número, 11 dígitos): ").strip()
    companhia = input("Companhia: ").strip()
    batalhao = input("Batalhão: ").strip()
    data_cadastro = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    c.execute('''INSERT INTO policiais(patente,nome_guerra,matricula,telefone,companhia,batalhao,data_cadastro)
                 VALUES(?,?,?,?,?,?,?)''',
                 (patente,nome_guerra,matricula,telefone,companhia,batalhao,data_cadastro))
    conn.commit()
    conn.close()
    print(f"Policial '{nome_guerra}' cadastrado com sucesso!")
    pausa(2)

def listar_policiais():
    conn = conectar()
    c = conn.cursor()
    limpar_tela()
    print("=== LISTA DE POLICIAIS ===")
    rows = c.execute("SELECT id,patente,nome_guerra,matricula,telefone,companhia,batalhao FROM policiais").fetchall()
    if not rows:
        print("Nenhum policial cadastrado.")
        aguardar_enter()
        return
    print(f"{'ID':<3} {'Patente':<15} {'Nome Guerra':<20} {'Matrícula':<10} {'Telefone':<12} {'Companhia':<10} {'Batalhão'}")
    print("-"*90)
    for p in rows:
        print(f"{p[0]:<3} {p[1]:<15} {p[2]:<20} {p[3] or '-':<10} {p[4] or '-':<12} {p[5] or '-':<10} {p[6] or '-'}")
    aguardar_enter()
    conn.close()

# ======================== VIATURAS ========================
def cadastrar_viatura():
    conn = conectar()
    c = conn.cursor()
    limpar_tela()
    print("=== CADASTRO DE VIATURA ===")
    while True:
        prefixo = input("Prefixo: ").strip()
        if prefixo and not c.execute("SELECT 1 FROM viaturas WHERE prefixo=?", (prefixo,)).fetchone():
            break
        print("Prefixo inválido ou já cadastrado!")
    
    while True:
        placa = input("Placa: ").strip()
        if placa and not c.execute("SELECT 1 FROM viaturas WHERE placa=?", (placa,)).fetchone():
            break
        print("Placa inválida ou já cadastrada!")
    
    while True:
        tipo = input("Tipo (Moto/4 Rodas): ").strip()
        if validar_tipo_viatura(tipo):
            tipo = tipo.title()
            break
        print("Tipo inválido!")
    
    km_atual = input("KM atual (opcional): ").strip() or None
    os_prime = input("OS Prime (opcional, 5 dígitos): ").strip() or None
    data_ultima_revisao = input("Data última revisão (opcional): ").strip() or None
    telefone_oficina = input("Telefone oficina (opcional): ").strip() or None
    observacao = input("Observação (opcional): ").strip() or None
    responsavel = input("Responsável (opcional): ").strip() or None
    data_cadastro = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    c.execute('''INSERT INTO viaturas(prefixo,placa,tipo,km_atual,os_prime,data_ultima_revisao,
                 telefone_oficina,observacao,responsavel,data_cadastro)
                 VALUES(?,?,?,?,?,?,?,?,?,?)''',
                 (prefixo,placa,tipo,km_atual,os_prime,data_ultima_revisao,
                  telefone_oficina,observacao,responsavel,data_cadastro))
    conn.commit()
    conn.close()
    print(f"Viatura '{prefixo}' cadastrada com sucesso!")
    pausa(2)

def listar_viaturas():
    conn = conectar()
    c = conn.cursor()
    limpar_tela()
    print("=== LISTA DE VIATURAS ===")
    rows = c.execute("SELECT id,prefixo,placa,tipo,km_atual,os_prime,data_ultima_revisao,responsavel FROM viaturas").fetchall()
    if not rows:
        print("Nenhuma viatura cadastrada.")
        aguardar_enter()
        return
    print(f"{'ID':<3} {'Prefixo':<10} {'Placa':<8} {'Tipo':<8} {'KM':<6} {'OS Prime':<8} {'Últ. Revisão':<12} {'Responsável'}")
    print("-"*90)
    for v in rows:
        print(f"{v[0]:<3} {v[1]:<10} {v[2]:<8} {v[3]:<8} {v[4] or '-':<6} {v[5] or '-':<8} {v[6] or '-':<12} {v[7] or '-'}")
    aguardar_enter()
    conn.close()

# ======================== LIXEIRA ========================
def mover_para_lixeira(tabela, id_item):
    conn = conectar()
    c = conn.cursor()
    lixeira = f"{tabela}_lixeira"
    c.execute(f"INSERT INTO {lixeira} SELECT * FROM {tabela} WHERE id=?", (id_item,))
    c.execute(f"DELETE FROM {tabela} WHERE id=?", (id_item,))
    conn.commit()
    conn.close()
    print("Item movido para lixeira!")
    pausa(1)

def restaurar_lixeira():
    conn = conectar()
    c = conn.cursor()
    for table in ["usuarios", "policiais", "viaturas"]:
        lixeira = f"{table}_lixeira"
        c.execute(f"INSERT INTO {table} SELECT * FROM {lixeira}")
        c.execute(f"DELETE FROM {lixeira}")
    conn.commit()
    conn.close()
    print("Todos os itens restaurados da lixeira!")
    pausa(2)

def apagar_lixeira():
    conn = conectar()
    c = conn.cursor()
    for lixeira in LIXEIRA_TABLES:
        c.execute(f"DELETE FROM {lixeira}")
    conn.commit()
    conn.close()
    print("Lixeira esvaziada permanentemente!")
    pausa(2)

# ======================== RESTAURAR SISTEMA ========================
def restaurar_sistema():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    inicializar_db()
    print("Sistema restaurado com sucesso!")
    pausa(2)

# ======================== MENUS ========================
def menu_viaturas():
    while True:
        limpar_tela()
        print("=== MENU VIATURAS ===")
        print("1. Cadastrar Viatura")
        print("2. Listar Viaturas")
        print("3. Mover Viatura para Lixeira")
        print("0. Voltar")
        opc = input("Opção: ").strip()
        if opc=="1":
            cadastrar_viatura()
        elif opc=="2":
            listar_viaturas()
        elif opc=="3":
            id_item = input("ID da viatura a mover para lixeira: ").strip()
            if id_item.isdigit():
                mover_para_lixeira("viaturas", int(id_item))
        elif opc=="0":
            break
        else:
            print("Opção inválida!")
            pausa(2)

def menu_policiais():
    while True:
        limpar_tela()
        print("=== MENU POLICIAIS ===")
        print("1. Cadastrar Policial")
        print("2. Listar Policiais")
        print("3. Mover Policial para Lixeira")
        print("0. Voltar")
        opc = input("Opção: ").strip()
        if opc=="1":
            cadastrar_policial()
        elif opc=="2":
            listar_policiais()
        elif opc=="3":
            id_item = input("ID do policial a mover para lixeira: ").strip()
            if id_item.isdigit():
                mover_para_lixeira("policiais", int(id_item))
        elif opc=="0":
            break
        else:
            print("Opção inválida!")
            pausa(2)

def menu_administradores():
    while True:
        limpar_tela()
        print("=== MENU ADMINISTRADORES ===")
        print("1. Cadastrar Administrador")
        print("2. Listar Administradores")
        print("3. Mover Administrador para Lixeira")
        print("4. Restaurar Lixeira")
        print("5. Apagar Lixeira")
        print("6. Restaurar Sistema")
        print("0. Voltar")
        opc = input("Opção: ").strip()
        if opc=="1":
            cadastrar_usuario()
        elif opc=="2":
            listar_administradores()
        elif opc=="3":
            id_item = input("ID do administrador a mover para lixeira: ").strip()
            if id_item.isdigit():
                mover_para_lixeira("usuarios", int(id_item))
        elif opc=="4":
            restaurar_lixeira()
        elif opc=="5":
            apagar_lixeira()
        elif opc=="6":
            restaurar_sistema()
        elif opc=="0":
            break
        else:
            print("Opção inválida!")
            pausa(2)

def menu_principal():
    while True:
        limpar_tela()
        print("=== MENU PRINCIPAL ===")
        print("1. Viaturas")
        print("2. Policiais")
        print("3. Administradores")
        print("0. Sair")
        opc = input("Opção: ").strip()
        if opc=="1":
            menu_viaturas()
        elif opc=="2":
            menu_policiais()
        elif opc=="3":
            menu_administradores()
        elif opc=="0":
            criar_backup_automatico()
            print("Saindo do sistema... Backup realizado.")
            break
        else:
            print("Opção inválida!")
            pausa(2)

# ======================== EXECUÇÃO ========================
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    inicializar_db()
    while True:
        limpar_tela()
        print("=== SISTEMA ROTAM ===")
        print("1. Cadastrar Administrador")
        print("2. Login")
        print("0. Sair")
        opc = input("Opção: ").strip()
        if opc=="1":
            cadastrar_usuario()
        elif opc=="2":
            if login():
                menu_principal()
        elif opc=="0":
            criar_backup_automatico()
            print("Saindo do sistema... Backup realizado.")
            break
        else:
            print("Opção inválida!")
            pausa(2)
