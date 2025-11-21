from database import conectar, mover_para_lixeira
from uteis import limpar_tela, pausa

def menu_viaturas():
    while True:
        limpar_tela()
        print("=== VIATURAS ===")
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
    prefixo = input("Prefixo: ")
    placa = input("Placa: ")
    tipo = input("Tipo: ")

    con = conectar()
    cur = con.cursor()

    try:
        cur.execute("INSERT INTO viaturas (prefixo, placa, tipo) VALUES (?, ?, ?)",
                    (prefixo, placa, tipo))
        con.commit()
        print("Viatura cadastrada!")
    except:
        print("Erro: prefixo ou placa já existem!")
    finally:
        con.close()

    pausa(2)


def listar():
    limpar_tela()
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT id, prefixo, placa, tipo FROM viaturas")

    for row in cur.fetchall():
        print(row)

    con.close()
    pausa(3)


def apagar():
    listar()
    vid = input("ID para apagar: ").strip()

    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT * FROM viaturas WHERE id=?", (vid,))
    dados = cur.fetchone()

    if not dados:
        print("ID não encontrado!")
        pausa(2)
        return

    mover_para_lixeira("viaturas", dados)

    cur.execute("DELETE FROM viaturas WHERE id=?", (vid,))
    con.commit()
    con.close()

    print("Movido para a lixeira.")
    pausa(2)
