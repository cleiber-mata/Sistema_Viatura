# uteis.py
"""
Funções utilitárias usadas pelo sistema ROTAM:
- limpar_tela(): limpa o terminal (compatível com Windows/Linux e ambientes interativos)
- pausa(segundos=2, msg=None): pausa a execução por segundos, opcional com mensagem
- aguardar_enter(prompt="Pressione Enter para continuar..."): aguarda o usuário pressionar Enter
"""

import os
import time

def limpar_tela():
    """Limpa a tela do terminal. Funciona em Windows, Unix e tenta forçar limpeza em ambientes interativos."""
    try:
        # comando padrão do sistema
        os.system('cls' if os.name == 'nt' else 'clear')
        # tentativa extra para alguns terminais/IDEs
        print("\033c", end="")
    except Exception:
        # se algo der errado, apenas não quebra o programa
        pass

def pausa(segundos=2, msg=None):
    """
    Pausa a execução por 'segundos'.
    Se 'msg' for fornecida, imprime a mensagem antes de pausar.
    """
    try:
        if msg:
            print(msg)
        time.sleep(segundos)
    except Exception:
        # em casos extremos ignore a pausa para não travar o sistema
        pass

def aguardar_enter(prompt="Pressione Enter para continuar..."):
    """
    Exibe um prompt e aguarda o usuário pressionar Enter.
    Trata KeyboardInterrupt de forma amigável.
    """
    try:
        input(f"\n{prompt}")
    except KeyboardInterrupt:
        # se o usuário der Ctrl+C, apenas continua
        print("")  # quebra de linha para manter o layout
        return
