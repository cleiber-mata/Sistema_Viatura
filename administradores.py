import datetime
import re
from uteis import limpar_tela, pausa, aguardar_enter
from armazenamento import salvar_json, carregar_json
from policiais import cadastrar_policial

# ---------------- ARQUIVO DE DADOS ----------------
USUARIOS_FILE = "data/usuarios.json"
usuarios = []

# ---------------- CARREGAR E SALVAR ----------------
def carregar_usuarios():
    global usuarios
    usuarios = carregar_json(USUARIOS_FILE)

def salvar_usuarios():
    salvar_json(USUARIOS_FILE, usuarios)

# ---------------- VALIDAÇÕES AUXILIARES ----------------
def nome_valido(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]{2,}$", nome.strip()))

def login_disponivel(login_user):
    return login_user and all(u['login'] != login_user for u in usuarios)

def senha_valida(senha):
    return len(senha) >= 4

# ---------------- CADASTRO DE ADMINISTRADOR ----------------
def cadastrar_usuario(realizar_cadastro=False):
    global usuarios
    limpar_tela()
    print("=== CADASTRO DE ADMINISTRADOR ===" if not realizar_cadastro else "=== REALIZAR CADASTRO ===")
    
    # Nome
    while True:
        nome = input("Nome completo: ").strip()
        if nome_valido(nome):
            break
        print("Nome inválido! Use apenas letras e espaços, mínimo 2 caracteres.")

    # Login
    while True:
        login_user = input("Login: ").strip()
        if login_disponivel(login_user):
            break
        print("Login inválido ou já existe! Tente outro.")

    # Senha
    while True:
        senha = input("Senha (mínimo 4 caracteres): ").strip()
        if senha_valida(senha):
            break
        print("Senha inválida! Digite ao menos 4 caracteres.")

    # Dados adicionais
    telefone = input("Telefone (DDD + número): ").strip()
    matricula = input("Matrícula: ").strip()
    patente = input("Patente: ").strip()
    companhia = input("Companhia: ").strip()
    batalhao = input("Batalhão: ").strip()

    # Gerar ID
    novo_id = max([u['id'] for u in usuarios], default=0) + 1
    novo = {
        "id": novo_id,
        "nome": nome,
        "login": login_user,
        "senha": senha,
        "telefone": telefone,
        "matricula": matricula,
        "patente": patente,
        "companhia": companhia,
        "batalhao": batalhao,
        "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    usuarios.append(novo)
    salvar_usuarios()
    print(f"Administrador '{nome}' cadastrado com sucesso!")

    # Cadastro automático como policial, se for o cadastro inicial
    if realizar_cadastro:
        cadastrar_policial(
            nome=nome,
            matricula=matricula,
            telefone=telefone,
            companhia=companhia,
            batalhao=batalhao,
            patente=patente
        )
    
    aguardar_enter()

# ---------------- LISTAGEM DE ADMINISTRADORES ----------------
def listar_usuarios():
    limpar_tela()
    if not usuarios:
        print("Nenhum administrador cadastrado.")
        aguardar_enter()
        return
    
    print(f"{'ID':<3} {'Nome':<25} {'Login':<15} {'Telefone':<12} {'Matrícula':<10} {'Patente':<10} {'Companhia':<10} {'Batalhão'}")
    print("-"*100)
    for u in usuarios:
        print(f"{u['id']:<3} {u['nome']:<25} {u['login']:<15} {u['telefone']:<12} {u['matricula']:<10} {u['patente']:<10} {u['companhia']:<10} {u['batalhao']}")
    aguardar_enter()

# ---------------- LOGIN ----------------
def login():
    limpar_tela()
    print("=== LOGIN DE ADMINISTRADOR ===")
    login_user = input("Login: ").strip()
    senha = input("Senha: ").strip()
    
    for u in usuarios:
        if u['login'] == login_user and u['senha'] == senha:
            print(f"Bem-vindo, {u['nome']}!")
            pausa(1)
            return True
    print("Login ou senha incorretos!")
    pausa(2)
    return False
