# ==================== sistema_viatura.py ====================
import os
import zipfile
import datetime
import re
from uteis import limpar_tela, pausa, aguardar_enter
from armazenamento import salvar_json, carregar_json

# ---------------- ARQUIVOS DE DADOS ----------------
USUARIOS_FILE = "data/usuarios.json"
POLICIAIS_FILE = "data/policiais.json"
VIATURAS_FILE = "data/viaturas.json"
BACKUP_DIR = "backup"
BACKUP_FILE = os.path.join(BACKUP_DIR, "backup_rotam.zip")

# ---------------- LISTAS EM MEMÓRIA ----------------
usuarios = []
policiais = []
viaturas = []

# ---------------- CARREGAR E SALVAR ----------------
def carregar_usuarios():
    global usuarios
    usuarios = carregar_json(USUARIOS_FILE)

def salvar_usuarios():
    salvar_json(USUARIOS_FILE, usuarios)

def carregar_policiais():
    global policiais
    policiais = carregar_json(POLICIAIS_FILE)

def salvar_policiais():
    salvar_json(POLICIAIS_FILE, policiais)

def carregar_viaturas():
    global viaturas
    viaturas = carregar_json(VIATURAS_FILE)

def salvar_viaturas():
    salvar_json(VIATURAS_FILE, viaturas)

# ---------------- BACKUP ----------------
def criar_backup():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    with zipfile.ZipFile(BACKUP_FILE, 'w') as zipf:
        print("Selecione o que deseja incluir no backup:")
        print("1. Policiais")
        print("2. Viaturas")
        print("3. Ambos")
        opc = input("Opção: ").strip()
        if opc in ['1','3'] and os.path.exists(POLICIAIS_FILE):
            zipf.write(POLICIAIS_FILE, arcname="policiais.json")
        if opc in ['2','3'] and os.path.exists(VIATURAS_FILE):
            zipf.write(VIATURAS_FILE, arcname="viaturas.json")
    print(f"Backup criado com sucesso: {BACKUP_FILE}")
    pausa(2)

def restaurar_backup():
    if not os.path.exists(BACKUP_FILE):
        print("Nenhum backup encontrado.")
        pausa(2)
        return
    with zipfile.ZipFile(BACKUP_FILE, 'r') as zipf:
        arquivos = zipf.namelist()
        print("Selecione o que deseja restaurar:")
        print("1. Policiais")
        print("2. Viaturas")
        print("3. Ambos")
        opc = input("Opção: ").strip()
        if opc in ['1','3'] and "policiais.json" in arquivos:
            zipf.extract("policiais.json", "data")
        if opc in ['2','3'] and "viaturas.json" in arquivos:
            zipf.extract("viaturas.json", "data")
    carregar_policiais()
    carregar_viaturas()
    print("Restauração concluída!")
    pausa(2)

# ---------------- RESET DO SISTEMA ----------------
def reset_sistema():
    limpar_tela()
    print("=== RESET DO SISTEMA ===")
    login_user = input("Login de administrador: ").strip().lower()
    senha = input("Senha: ").strip()
    for u in usuarios:
        if u['login'].lower() == login_user and u['senha'] == senha:
            print("Realizando backup automático antes do reset...")
            criar_backup()
            for file in [USUARIOS_FILE, POLICIAIS_FILE, VIATURAS_FILE]:
                if os.path.exists(file):
                    os.remove(file)
            usuarios.clear()
            policiais.clear()
            viaturas.clear()
            print("Sistema resetado com sucesso!")
            pausa(2)
            return
    print("Login ou senha incorretos!")
    pausa(2)

# ---------------- VALIDADORES ----------------
def nome_valido(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]{2,}$", nome.strip()))

def validar_prefixo(prefixo):
    return bool(prefixo.strip()) and all(c.isdigit() or c=='.' for c in prefixo)

def validar_placa(placa):
    return bool(placa.strip()) and all(c.isalnum() or c=='-' for c in placa)

def validar_tipo(tipo):
    return tipo.lower() in ['moto', '4 rodas']

def validar_os_prime(os_prime):
    return not os_prime or (os_prime.isdigit() and len(os_prime)==5)

def validar_nome_guerra(nome):
    return bool(nome.strip()) and all(c.isalnum() or c.isspace() for c in nome)

def validar_telefone(telefone):
    return telefone.isdigit() and len(telefone) == 11

def validar_matricula(matricula):
    return bool(matricula.strip())

def validar_senha_formato(senha):
    return bool(re.match(r"^[0-9]{6}$", senha))

# ---------------- LOGIN ----------------
def login():
    limpar_tela()
    print("=== LOGIN DE ADMINISTRADOR ===")
    login_user = input("Login: ").strip().lower()
    senha = input("Senha: ").strip()
    for u in usuarios:
        if u['login'].lower() == login_user and u['senha'] == senha:
            print(f"Bem-vindo, {u['nome']}!")
            pausa(1)
            return True
    print("Login ou senha incorretos!")
    pausa(2)
    return False

# ---------------- GERAÇÃO DE LOGIN ----------------
def gerar_login(nome_completo):
    partes = nome_completo.strip().split()
    if len(partes) < 2:
        partes.append("user")
    primeiro = re.sub(r'[^a-zA-Z0-9]', '', partes[0].lower())
    ultimo = re.sub(r'[^a-zA-Z0-9]', '', partes[-1].lower())
    if not primeiro:
        primeiro = "user"
    if not ultimo:
        ultimo = "user"
    base = f"{primeiro}.{ultimo}"
    login_final = base
    contador = 1
    logins_existentes = [u['login'].lower() for u in usuarios]
    while login_final.lower() in logins_existentes:
        login_final = f"{base}{contador}"
        contador += 1
    return login_final

# ---------------- CADASTROS ----------------
def cadastrar_usuario(realizar_cadastro=False):
    global usuarios
    limpar_tela()
    print("=== CADASTRO DE ADMINISTRADOR ===" if not realizar_cadastro else "=== REALIZAR CADASTRO ===")
    
    while True:
        nome = input("Nome completo: ").strip()
        if nome_valido(nome):
            break
        print("Nome inválido! Use pelo menos 2 letras.")
    
    login_user = gerar_login(nome)
    print(f"Login sugerido: {login_user}")

    while True:
        senha = input("Senha (6 dígitos numéricos): ").strip()
        if not validar_senha_formato(senha):
            print("Senha inválida! Deve ter 6 dígitos.")
            continue
        senha_conf = input("Confirme a senha: ").strip()
        if senha != senha_conf:
            print("Senhas não conferem! Tente novamente.")
            continue
        break

    telefone = input("Telefone (DDD+Número, 11 dígitos): ").strip()
    matricula = input("Matrícula: ").strip()
    patente = input("Patente: ").strip()
    companhia = input("Companhia: ").strip()
    batalhao = input("Batalhão: ").strip()

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

    # Admin automaticamente como policial
    cadastrar_policial(nome=nome, matricula=matricula, telefone=telefone, companhia=companhia, batalhao=batalhao, patente=patente)
    pausa(2)

def listar_administradores():
    limpar_tela()
    if not usuarios:
        print("Nenhum administrador cadastrado.")
        aguardar_enter()
        return
    print(f"{'ID':<3} {'Nome':<25} {'Login':<20} {'Telefone':<12} {'Matrícula':<10} {'Patente':<15} {'Companhia':<10} {'Batalhão'}")
    print("-"*100)
    for u in usuarios:
        print(f"{u['id']:<3} {u['nome']:<25} {u['login']:<20} {u['telefone']:<12} {u['matricula']:<10} {u['patente']:<15} {u['companhia']:<10} {u['batalhao']}")
    aguardar_enter()

# ---------------- POLICIAIS ----------------
def cadastrar_policial(nome=None, matricula=None, telefone=None, companhia=None, batalhao=None, patente=None):
    global policiais
    limpar_tela()
    print("=== CADASTRO DE POLICIAL (PM) ===")
    
    patentes = ["Soldado", "Cabo", "Terceiro-Sargento", "Segundo-Sargento",
                "Primeiro-Sargento", "Subtenente", "Aspirante", "Tenente",
                "Capitão", "Major", "Tenente-Coronel", "Coronel"]
    if not patente:
        print("Escolha a patente do policial:")
        for i, p in enumerate(patentes, 1):
            print(f"{i}. {p}")
        while True:
            try:
                opc = int(input("Opção: ").strip())
                if 1 <= opc <= len(patentes):
                    patente = patentes[opc - 1]
                    break
                print("Opção inválida!")
            except ValueError:
                print("Digite apenas números.")
    
    if not nome:
        while True:
            nome = input("Nome de guerra: ").strip()
            if validar_nome_guerra(nome):
                break
            print("Nome inválido!")
    
    if not matricula:
        while True:
            matricula = input("Matrícula: ").strip()
            if validar_matricula(matricula):
                break
            print("Matrícula inválida!")
    
    if not telefone:
        while True:
            telefone = input("Telefone (DDD+Número, 11 dígitos): ").strip()
            if validar_telefone(telefone):
                break
            print("Telefone inválido!")
    
    if not companhia:
        companhia = input("Companhia: ").strip()
    if not batalhao:
        batalhao = input("Batalhão: ").strip()
    
    novo_id = max([p['id'] for p in policiais], default=0) + 1
    novo = {
        "id": novo_id,
        "patente": patente,
        "nome_guerra": nome,
        "matricula": matricula,
        "telefone": telefone,
        "companhia": companhia,
        "batalhao": batalhao,
        "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    policiais.append(novo)
    salvar_policiais()
    print(f"Policial '{nome}' cadastrado com sucesso!")
    pausa(2)

def listar_policiais():
    limpar_tela()
    if not policiais:
        print("Nenhum policial cadastrado.")
        aguardar_enter()
        return
    print(f"{'ID':<3} {'Patente':<15} {'Nome Guerra':<20} {'Matrícula':<10} {'Telefone':<12} {'Companhia':<10} {'Batalhão'}")
    print("-"*90)
    for p in policiais:
        print(f"{p['id']:<3} {p['patente']:<15} {p['nome_guerra']:<20} {p['matricula']:<10} {p['telefone']:<12} {p['companhia']:<10} {p['batalhao']}")
    aguardar_enter()

# ---------------- VIATURAS ----------------
def cadastrar_viatura():
    global viaturas
    limpar_tela()
    print("=== CADASTRO DE VIATURA ===")
    
    while True:
        prefixo = input("Prefixo: ").strip()
        if validar_prefixo(prefixo) and all(v['prefixo'] != prefixo for v in viaturas):
            break
        print("Prefixo inválido ou já cadastrado!")

    while True:
        placa = input("Placa: ").strip()
        if validar_placa(placa) and all(v['placa'] != placa for v in viaturas):
            break
        print("Placa inválida ou já cadastrada!")

    while True:
        tipo = input("Tipo de viatura (Moto/4 Rodas): ").strip()
        if validar_tipo(tipo):
            tipo = tipo.title()
            break
        print("Tipo inválido!")

    km_atual = input("KM atual (opcional): ").strip()
    os_prime = input("OS Prime (5 dígitos, opcional): ").strip()
    while not validar_os_prime(os_prime):
        print("OS Prime inválida!")
        os_prime = input("OS Prime (5 dígitos, opcional): ").strip()
    data_ultima_revisao = input("Data última revisão (opcional): ").strip()
    telefone_oficina = input("Telefone da oficina (opcional): ").strip()
    observacao = input("Observação (opcional): ").strip()
    responsavel = input("Responsável (opcional): ").strip()

    novo_id = max([v['id'] for v in viaturas], default=0) + 1
    novo = {
        "id": novo_id,
        "prefixo": prefixo,
        "placa": placa,
        "tipo": tipo,
        "km_atual": km_atual or None,
        "os_prime": os_prime or None,
        "data_ultima_revisao": data_ultima_revisao or None,
        "telefone_oficina": telefone_oficina or None,
        "observacao": observacao or None,
        "responsavel": responsavel or None,
        "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }
    viaturas.append(novo)
    salvar_viaturas()
    print(f"Viatura '{prefixo}' cadastrada com sucesso!")
    pausa(2)

def listar_viaturas():
    limpar_tela()
    if not viaturas:
        print("Nenhuma viatura cadastrada.")
        aguardar_enter()
        return
    print(f"{'ID':<3} {'Prefixo':<10} {'Placa':<8} {'Tipo':<8} {'KM':<6} {'OS Prime':<8} {'Últ. Revisão':<12} {'Responsável'}")
    print("-"*90)
    for v in viaturas:
        print(f"{v['id']:<3} {v['prefixo']:<10} {v['placa']:<8} {v['tipo']:<8} {v['km_atual'] or '-':<6} {v['os_prime'] or '-':<8} {v['data_ultima_revisao'] or '-':<12} {v['responsavel'] or '-'}")
    aguardar_enter()

# ---------------- MENUS ----------------
def menu_viaturas():
    while True:
        limpar_tela()
        print("=== MENU VIATURAS ===")
        print("1. Cadastrar Viatura")
        print("2. Listar Viaturas")
        print("0. Voltar")
        opc = input("Opção: ").strip()
        if opc == "1":
            cadastrar_viatura()
        elif opc == "2":
            listar_viaturas()
        elif opc == "0":
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
        print("0. Voltar")
        opc = input("Opção: ").strip()
        if opc == "1":
            cadastrar_policial()
        elif opc == "2":
            listar_policiais()
        elif opc == "0":
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
        print("3. Backup")
        print("4. Restaurar Backup")
        print("5. Reset do Sistema")
        print("0. Voltar")
        opc = input("Opção: ").strip()
        if opc == "1":
            cadastrar_usuario(realizar_cadastro=True)
        elif opc == "2":
            listar_administradores()
        elif opc == "3":
            criar_backup()
        elif opc == "4":
            restaurar_backup()
        elif opc == "5":
            reset_sistema()
        elif opc == "0":
            break
        else:
            print("Opção inválida!")
            pausa(2)

# ---------------- MENU PRINCIPAL ----------------
def menu_principal():
    while True:
        limpar_tela()
        print("=== MENU PRINCIPAL ===")
        print("1. Administradores")
        print("2. Policiais")
        print("3. Viaturas")
        print("0. Sair")
        opc = input("Opção: ").strip()
        if opc == "1":
            menu_administradores()
        elif opc == "2":
            menu_policiais()
        elif opc == "3":
            menu_viaturas()
        elif opc == "0":
            break
        else:
            print("Opção inválida!")
            pausa(2)

# ---------------- EXECUÇÃO ----------------
if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    carregar_usuarios()
    carregar_policiais()
    carregar_viaturas()

    while True:
        limpar_tela()
        print("=== SISTEMA ROTAM VIATURAS ===")
        print("1. Cadastrar Administrador")
        print("2. Login")
        print("0. Sair")
        opc = input("Opção: ").strip()
        if opc == "1":
            cadastrar_usuario(realizar_cadastro=True)
        elif opc == "2":
            if login():
                menu_principal()
        elif opc == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida!")
            pausa(2)