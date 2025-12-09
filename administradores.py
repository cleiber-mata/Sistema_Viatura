from database import conectar, menu_lixeira, restaurar_sistema
from uteis import pausa, limpar_tela
from requisitos_funcionalidades import mostrar_requisitos

def cadastrar_administrador():
    limpar_tela()
    print("=== CADASTRAR ADMINISTRADOR ===")

    nome_completo = input("Nome Completo: ").strip().lower()
    nome = input("Primeiro Nome: ").strip().lower()
    sobrenome = input("Sobrenome: ").strip().lower()
    login = f"{nome}.{sobrenome}"

    while True:
        senha = input("Senha (6 dígitos numéricos): ").strip()
        if senha.isdigit() and len(senha) == 6:
            confirmar = input("Confirmar senha: ").strip()
            if confirmar == senha:
                break
            else:
                print("Senhas não conferem!")
        else:
            print("Senha inválida!")

    con = conectar()
    cur = con.cursor()

    try:
        cur.execute("INSERT INTO administradores (nome_completo, nome, sobrenome, login, senha) VALUES (?, ?, ?, ?, ?)",
                    (nome_completo, nome, sobrenome, login, senha))
        con.commit()
        print(f"Administrador criado com login: {login}")
    except:
        print("Erro: login já existente!")
    finally:
        con.close()

    pausa(2)


def login():
    limpar_tela()
    print("=== LOGIN ===")

    login_dig = input("Login: ").strip().lower()
    senha_dig = input("Senha: ").strip()

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id FROM administradores WHERE login=? AND senha=?", (login_dig, senha_dig))
    r = cur.fetchone()
    con.close()

    if r:
        print("Login bem-sucedido!")
        pausa(1)
        return True
    else:
        print("Login inválido!")
        pausa(1)
        return False


def menu_admins():
    while True:
        limpar_tela()
        print("=== MENU ADMINISTRADOR ===")
        print("1. Relatorios.")
        print("2. Restaurar Sistema")
        print("3. Restart Sistema.")
        print("4. Lixeira")
        print("9. Requisitos e Funcionalidades.")
        print("0. Voltar")

        opc = input("Opção: ").strip()

        if opc == "1":
            print("Em desenvolvimento!")
            pausa(1)
        elif opc == "2":
            restaurar_sistema()
            pausa(1)
        elif opc == "3":
            print("Em desenvolvimento!")
            pausa(1)
        elif opc == "4":
            menu_lixeira()
        elif opc == "9":
            mostrar_requisitos()
        elif opc == "0":
            break
        else:
            pausa(1)
