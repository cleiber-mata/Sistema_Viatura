import datetime
from uteis import limpar_tela, pausa, aguardar_enter
import armazenamento_sql as db

# ---------------- CADASTRO DE VIATURA ----------------
def cadastrar_viatura():
    limpar_tela()
    print("=== CADASTRO DE VIATURA ===")

    # Prefixo
    while True:
        prefixo = input("Prefixo (Ex: 44.0001 moto / 55.0001 4 rodas) [Obrigatório]: ").strip()

        existe = db.listar("viaturas")
        if prefixo and not any(v[1] == prefixo for v in existe):
            break

        print("Campo obrigatório ou prefixo já cadastrado!")

    # Placa
    while True:
        placa = input("Placa [Obrigatório]: ").strip()

        existe = db.listar("viaturas")
        if placa and not any(v[2] == placa for v in existe):
            break

        print("Campo obrigatório ou placa já cadastrada!")

    # Tipo
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

    data_cadastro = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Inserir no banco
    db.inserir("viaturas", {
        "prefixo": prefixo,
        "placa": placa,
        "modelo": tipo,
        "km_atual": km_atual,
        "os_prime": os_prime,
        "data_ultima_revisao": data_ultima_revisao,
        "telefone_oficina": telefone_oficina,
        "observacao": observacao,
        "responsavel": responsavel,
        "data_cadastro": data_cadastro
    })

    print(f"Viatura '{prefixo}' cadastrada com sucesso!")
    aguardar_enter()


# ---------------- LISTAGEM DE VIATURAS ----------------
def listar_viaturas():
    limpar_tela()
    registros = db.listar("viaturas")

    if not registros:
        print("Nenhuma viatura cadastrada.")
        aguardar_enter()
        return

    print(f"{'ID':<3} {'Prefixo':<10} {'Placa':<8} {'Tipo':<10} {'KM':<6} {'OS Prime':<8} {'Últ. Revisão':<12} {'Responsável'}")
    print("-" * 100)

    for v in registros:
        # Índices conforme ordem das colunas
        print(f"{v[0]:<3} {v[1]:<10} {v[2]:<8} {v[3]:<10} {v[4] or '-':<6} {v[5] or '-':<8} {v[6] or '-':<12} {v[9] or '-'}")

    aguardar_enter()


# ---------------- PESQUISA POR PREFIXO ----------------
def pesquisar_viatura_prefixo():
    limpar_tela()
    prefixo = input("Digite o prefixo da viatura: ").strip()

    registros = db.listar("viaturas")
    encontrados = [v for v in registros if v[1] == prefixo]

    if encontrados:
        print("Viaturas encontradas:")
        for v in encontrados:
            print(f"{v[1]} - {v[2]} - {v[3]} - OS Prime: {v[5] or '-'} - KM: {v[4] or '-'}")
    else:
        print("Nenhuma viatura encontrada com esse prefixo.")

    aguardar_enter()


# ---------------- PESQUISA POR OS PRIME ----------------
def pesquisar_os_prime():
    limpar_tela()
    os_prime = input("Digite a OS Prime (5 dígitos): ").strip()

    registros = db.listar("viaturas")
    encontrados = [v for v in registros if v[5] == os_prime]

    if encontrados:
        print("Viaturas encontradas:")
        for v in encontrados:
            print(f"{v[1]} - {v[2]} - {v[3]} - KM: {v[4] or '-'} - Responsável: {v[9] or '-'}")
    else:
        print("Nenhuma viatura encontrada com essa OS Prime.")

    aguardar_enter()


# ---------------- RELATÓRIO ----------------
def relatorio_viaturas():
    limpar_tela()

    registros = db.listar("viaturas")

    total = len(registros)
    baixadas = [v for v in registros if v[5]]        # OS Prime preenchida
    disponiveis = [v for v in registros if not v[5]]

    print("=== RELATÓRIO DE VIATURAS ===")
    print(f"Total de viaturas cadastradas: {total}")
    print(f"Viaturas baixadas (com OS Prime): {len(baixadas)}")
    print(f"Viaturas disponíveis: {len(disponiveis)}\n")

    if baixadas:
        print("Detalhes das viaturas baixadas:")
        for v in baixadas:
            print(f"{v[1]} - {v[2]} - KM: {v[4] or '-'} - Próx. Revisão: {v[6] or '-'} - OS Prime: {v[5]}")

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
