# ============================================================
# uteis.py - utilitários do sistema ROTAM (versão OOP)
# ============================================================

import os
import time

class Uteis:
    @staticmethod
    def limpar_tela():
        """Limpa a tela do terminal. Funciona em Windows, Unix e tenta forçar limpeza em ambientes interativos."""
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\033c", end="")  # tentativa extra para alguns terminais/IDEs
        except Exception:
            pass

    @staticmethod
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
            pass

    @staticmethod
    def aguardar_enter(prompt="Pressione Enter para continuar..."):
        """
        Exibe um prompt e aguarda o usuário pressionar Enter.
        Trata KeyboardInterrupt de forma amigável.
        """
        try:
            input(f"\n{prompt}")
        except KeyboardInterrupt:
            print("")  # quebra de linha para manter o layout
            return
