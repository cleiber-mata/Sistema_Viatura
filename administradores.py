from database import conectar
from uteis import pausa, limpar_tela

def cadastrar_administrador():
    limpar_tela()
    print("=== CADASTRAR ADMINISTRADOR ===")

    nome = input("Nome: ").strip().lower()
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
        cur.execute("INSERT INTO administradores (nome, sobrenome, login, senha) VALUES (?, ?, ?, ?)",
                    (nome, sobrenome, login, senha))
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

    login = input("Login: ").strip().lower()
    senha = input("Senha: ").strip()

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id FROM administradores WHERE login=? AND senha=?", (login, senha))
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
    limpar_tela()
    print("=== ADMINISTRADORES ===")
    print("Funções futuras serão adicionadas aqui.")
    pausa(2)
