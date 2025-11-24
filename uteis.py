import os
import time

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def pausa(seg=1):
    time.sleep(seg)
    
def enter_continue():
    input("Pressione Enter para continuar...")
