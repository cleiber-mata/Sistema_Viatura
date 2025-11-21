from database import conectar, mover_para_lixeira
from uteis import limpar_tela, pausa

def menu_policiais():
    while True:
        limpar_tela()
        print("=== POLICIAIS ===")
        print("1. Cadastrar")
        print("2. Listar")
        print("3. Apagar")
        print("0. Voltar")

        opc = input("Opção: ")

        if opc == "1":
            cadastrar()
        elif opc == "2":
            listar()
        elif opc == "3":
            apagar()
        elif opc == "0":
            break
        else:
            pausa(1)


def cadastrar():
    limpar_tela()
    nome = input("Nome: ").strip()
    matricula = input("Matrícula: ").strip()

    con = conectar()
    cur = con.cursor()

    try:
        cur.execute("INSERT INTO policiais (nome, matricula) VALUES (?, ?)", (nome, matricula))
        con.commit()
        print("Policial cadastrado!")
    except:
        print("Erro: matrícula já cadastrada!")
    finally:
        con.close()

    pausa(2)


def listar():
    limpar_tela()
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, nome, matricula FROM policiais")

    for row in cur.fetchall():
        print(row)

    con.close()
    pausa(3)


def apagar():
    listar()
    pid = input("ID para apagar: ").strip()

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM policiais WHERE id=?", (pid,))
    dados = cur.fetchone()

    if not dados:
        print("ID não encontrado!")
        pausa(2)
        return

    mover_para_lixeira("policiais", dados)

    cur.execute("DELETE FROM policiais WHERE id=?", (pid,))
    con.commit()
    con.close()

    print("Movido para a lixeira.")
    pausa(2)
