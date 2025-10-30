import datetime
from uteis import limpar_tela, pausa, aguardar_enter
from armazenamento import salvar_json, carregar_json

# ---------------- ARQUIVO DE DADOS ----------------
VIATURAS_FILE = "data/viaturas.json"
viaturas = []

# ---------------- CARREGAR E SALVAR ----------------
def carregar_viaturas():
    global viaturas
    viaturas = carregar_json(VIATURAS_FILE)

def salvar_viaturas():
    salvar_json(VIATURAS_FILE, viaturas)

# ---------------- CADASTRO DE VIATURA ----------------
def cadastrar_viatura():
    global viaturas
    limpar_tela()
    print("=== CADASTRO DE VIATURA ===")
    
    # Campos obrigatórios
    while True:
        prefixo = input("Prefixo (Ex: 44.0001 para motos, 55.0001 para 4 rodas) [Obrigatório]: ").strip()
        if prefixo and all(v['prefixo'] != prefixo for v in viaturas):
            break
        print("Campo obrigatório ou prefixo já cadastrado!")

    while True:
        placa = input("Placa [Obrigatório]: ").strip()
        if placa and all(v['placa'] != placa for v in viaturas):
            break
        print("Campo obrigatório ou placa já cadastrada!")

    while True:
        tipo = input("Tipo de viatura (Moto/4 Rodas) [Obrigatório]: ").strip().lower()
        if tipo in ['moto', '4 rodas']:
            tipo = tipo.title()
            break
        print("Tipo inválido! Informe 'Moto' ou '4 Rodas'.")

    # Campos opcionais
    km_atual = input("KM atual (opcional): ").strip() or None
    os_prime = input("OS Prime (5 dígitos) (opcional): ").strip() or None
    data_ultima_revisao = input("Data última revisão (DD/MM/AAAA) (opcional): ").strip() or None
    telefone_oficina = input("Telefone da oficina (opcional): ").strip() or None
    observacao = input("Observação curta de manutenção (opcional): ").strip() or None
    responsavel = input("Responsável pela viatura (opcional): ").strip() or None

    novo_id = max([v['id'] for v in viaturas], default=0) + 1
    viatura = {
        "id": novo_id,
        "prefixo": prefixo,
        "placa": placa,
        "tipo": tipo,
        "km_atual": km_atual,
        "os_prime": os_prime,
        "data_ultima_revisao": data_ultima_revisao,
        "telefone_oficina": telefone_oficina,
        "observacao": observacao,
        "responsavel": responsavel,
        "data_cadastro": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    }

    viaturas.append(viatura)
    salvar_viaturas()
    print(f"Viatura '{prefixo}' cadastrada com sucesso!")
    aguardar_enter()

# ---------------- LISTAGEM DE VIATURAS ----------------
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

# ---------------- PESQUISA POR PREFIXO ----------------
def pesquisar_viatura_prefixo():
    limpar_tela()
    prefixo = input("Digite o prefixo da viatura: ").strip()
    encontrados = [v for v in viaturas if v['prefixo'] == prefixo]
    if encontrados:
        print("Viaturas encontradas:")
        for v in encontrados:
            print(f"{v['prefixo']} - {v['placa']} - {v['tipo']} - OS Prime: {v['os_prime'] or '-'} - KM: {v['km_atual'] or '-'}")
    else:
        print("Nenhuma viatura encontrada com esse prefixo.")
    aguardar_enter()

# ---------------- PESQUISA POR OS PRIME ----------------
def pesquisar_os_prime():
    limpar_tela()
    os_prime = input("Digite a OS Prime (5 dígitos): ").strip()
    encontrados = [v for v in viaturas if v['os_prime'] == os_prime]
    if encontrados:
        print("Viaturas encontradas:")
        for v in encontrados:
            print(f"{v['prefixo']} - {v['placa']} - {v['tipo']} - KM: {v['km_atual'] or '-'} - Responsável: {v['responsavel'] or '-'}")
    else:
        print("Nenhuma viatura encontrada com essa OS Prime.")
    aguardar_enter()

# ---------------- RELATÓRIO ----------------
def relatorio_viaturas():
    limpar_tela()
    total = len(viaturas)
    baixadas = [v for v in viaturas if v['os_prime']]
    disponiveis = [v for v in viaturas if not v['os_prime']]

    print("=== RELATÓRIO DE VIATURAS ===")
    print(f"Total de viaturas cadastradas: {total}")
    print(f"Viaturas baixadas (com OS Prime): {len(baixadas)}")
    print(f"Viaturas disponíveis: {len(disponiveis)}\n")
    
    if baixadas:
        print("Detalhes das viaturas baixadas:")
        for v in baixadas:
            print(f"{v['prefixo']} - {v['placa']} - KM: {v['km_atual'] or '-'} - Próx. Revisão: {v['data_ultima_revisao'] or '-'} - OS Prime: {v['os_prime']}")
    aguardar_enter()

# ---------------- MENU DE VIATURAS ----------------
def menu_viaturas():
    while True:
        limpar_tela()
        print("=== MENU DE VIATURAS ===")
        print("1. Cadastrar Viatura")
        print("2. Listar Viaturas")
        print("3. Pesquisar por Prefixo")
        print("4. Pesquisar por OS Prime")
        print("5. Relatório de Situação")
        print("0. Voltar ao menu principal")
        escolha = input("Opção: ").strip()

        if escolha == '1':
            cadastrar_viatura()
        elif escolha == '2':
            listar_viaturas()
        elif escolha == '3':
            pesquisar_viatura_prefixo()
        elif escolha == '4':
            pesquisar_os_prime()
        elif escolha == '5':
            relatorio_viaturas()
        elif escolha == '0':
            break
        else:
            print("Opção inválida! Tente novamente.")
            pausa(2)
