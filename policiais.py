import datetime
from uteis import limpar_tela, pausa, aguardar_enter
from armazenamento import salvar_json, carregar_json

# ---------------- ARQUIVO DE DADOS ----------------
POLICIAIS_FILE = "data/policiais.json"
policiais = []

# ---------------- CARREGAR E SALVAR ----------------
def carregar_policiais():
    global policiais
    policiais = carregar_json(POLICIAIS_FILE)

def salvar_policiais():
    salvar_json(POLICIAIS_FILE, policiais)

# ---------------- VALIDAÇÕES ----------------
def validar_nome_guerra(nome):
    return bool(nome.strip()) and all(c.isalnum() or c.isspace() for c in nome)

def validar_telefone(telefone):
    return telefone.isdigit() and len(telefone) == 11  # DDD + 9 dígitos

def validar_matricula(matricula):
    return bool(matricula.strip())

# ---------------- CADASTRO DE POLICIAL ----------------
def cadastrar_policial(nome=None, matricula=None, telefone=None, companhia=None, batalhao=None, patente=None):
    global policiais
    limpar_tela()
    print("=== CADASTRO DE POLICIAL (PM) ===")

    # Patentes
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

    # Nome de guerra
    if not nome:
        while True:
            nome = input("Nome de guerra: ").strip()
            if validar_nome_guerra(nome):
                break
            print("Nome inválido! Não pode estar vazio ou conter símbolos especiais.")

    # Matrícula
    if not matricula:
        while True:
            matricula = input("Matrícula: ").strip()
            if validar_matricula(matricula):
                break
            print("Matrícula inválida!")

    # Telefone
    if not telefone:
        while True:
            telefone = input("Telefone (DDD + número, 11 dígitos): ").strip()
            if validar_telefone(telefone):
                break
            print("Telefone inválido! Digite 11 números sem espaços ou símbolos.")

    # Companhia e batalhão
    if not companhia:
        companhia = input("Companhia: ").strip()
    if not batalhao:
        batalhao = input("Batalhão: ").strip()

    # ID automático
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
    aguardar_enter()

# ---------------- LISTAGEM DE POLICIAIS ----------------
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
