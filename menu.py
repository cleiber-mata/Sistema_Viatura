from uteis import limpar_tela, pausa
from administradores import cadastrar_administrador, login
from viaturas import menu_viaturas
from policiais import menu_policiais
from administradores import menu_admins
from database import criar_backup_automatico

def menu_inicial():
    while True:
        limpar_tela()
        print("=== SISTEMA ROTAM ===")
        print("1. Cadastrar Administrador")
        print("2. Login")
        print("0. Sair")

        opc = input("\nOpção: ").strip()

        if opc == "1":
            cadastrar_administrador()
        elif opc == "2":
            if login():
                menu_principal()
        elif opc == "0":
            break
        else:
            print("Opção inválida!")
            pausa(1)

def menu_principal():
    while True:
        limpar_tela()
        print("=== MENU PRINCIPAL ===")
        print("1. Viaturas")
        print("2. Policiais")
        print("3. Administradores")
        print("0. Voltar menu anterior.")

        opc = input("Opção: ").strip()

        if opc == "1":
            menu_viaturas()
        elif opc == "2":
            menu_policiais()
        elif opc == "3":
            menu_admins()
        elif opc == "0":
            criar_backup_automatico()
            print("Saindo...")
            pausa(1)
            break
        else:
            print("Opção inválida!")
            pausa(1)