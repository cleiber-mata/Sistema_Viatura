import tkinter as tk
from tkinter import scrolledtext

def mostrar_requisitos():
    texto = """
    ============================================================
    SISTEMA DE GERENCIAMENTO DE VIATURAS, POLICIAIS E ADMINISTRADORES
    ============================================================

    DOCUMENTAÇÃO DE REQUISITOS E FUNCIONALIDADES DO SISTEMA

    O sistema gerencia administradores, policiais e viaturas, mantendo tudo registrado em banco de dados e acessado por menus no terminal.

1. Acesso ao sistema
O uso completo exige login de administrador. Cada administrador tem nome, login, senha e dados funcionais. O ID é criado automaticamente.

2. Policiais
Permite cadastrar policiais com nome de guerra, matrícula, telefone, patente, companhia e batalhão.
Todos os dados ficam listáveis em tela.

3. Viaturas
Cadastro de viaturas com prefixo, placa, tipo (Moto ou 4 Rodas), KM, OS Prime, última revisão, contato da oficina, observações e responsável.
O sistema identifica automaticamente viaturas disponíveis (sem OS) e baixadas (com OS).
Também permite listar, buscar por prefixo, buscar por OS e gerar relatório.

4. Lixeira (Recuperação de dados)
Itens excluídos podem ir para a lixeira e ser restaurados depois.
A lixeira também pode ser esvaziada.

5. Backup
É possível criar backup da pasta de dados a qualquer momento.

6. Estrutura do menu
O menu principal reúne:
– cadastro e listagem de viaturas
– pesquisa por prefixo ou OS
– relatório geral
– cadastro e listagem de policiais
– listagem de administradores
– criação de backup
– acesso à lixeira
– retorno ao menu inicial ou saída

7. Regras e validações
Prefixo, placa e login não podem repetir.
Telefones precisam ter 11 dígitos.
Datas de criação são automáticas.
Tipos de viatura só podem ser Moto ou 4 Rodas.)
    """

    # Cria a janela
    janela = tk.Tk()
    janela.title("Requisitos do Sistema")
    janela.geometry("950x700")

    # Área de texto com barra de rolagem
    caixa = scrolledtext.ScrolledText(janela, wrap=tk.WORD, font=("Consolas", 11))
    caixa.pack(expand=True, fill="both")

    caixa.insert(tk.END, texto)
    caixa.config(state="disabled")  # impede edição

    janela.mainloop()


"""
============================================================
SISTEMA DE GERENCIAMENTO DE VIATURAS, POLICIAIS E ADMINISTRADORES
============================================================

DOCUMENTAÇÃO DE REQUISITOS E FUNCIONALIDADES DO SISTEMA
Arquivo: requisitosfuncionais.py

============================================================
1. REQUISITOS DO SISTEMA
============================================================

- Permitir cadastro de administradores com login e senha.
- Permitir cadastro de policiais contendo:
    nome de guerra, matrícula, patente, companhia, batalhão e telefone.
- Permitir cadastro de viaturas contendo:
    prefixo (único), placa (única), tipo (Moto ou 4 Rodas), KM atual,
    OS Prime, data da última revisão, telefone da oficina, observações
    e responsável.
- Identificação automática de viaturas baixadas (com OS Prime) e
  viaturas disponíveis (sem OS Prime).
- Pesquisa de viaturas por prefixo ou OS Prime.
- Registro automático da data e hora de criação de administradores,
  policiais e viaturas.
- Exigir login do administrador para acessar o menu principal.
- Permitir criação de backup opcional da pasta de dados.
- Interface baseada em terminal (linha de comando).
- Persistência de dados em JSON ou banco de dados SQL.
- IDs gerados automaticamente.
- Validação de campos obrigatórios e impedimento de duplicidades:
    login, prefixo e placa.

============================================================
2. FUNCIONALIDADES GERAIS
============================================================

1. Limpeza da tela:
    - Limpa o terminal (Windows ou Linux).

2. Pausa:
    - Aguarda alguns segundos antes de avançar.

3. Aguardo de Enter:
    - Espera o usuário pressionar Enter.

4. Backup de dados:
    - Copia toda a pasta "data" com data/hora no nome.
    - Utiliza a biblioteca shutil.

============================================================
3. FUNCIONALIDADES DE ADMINISTRADOR
============================================================

5. Cadastrar administrador:
    - Solicita nome completo, login, senha, telefone,
      matrícula, patente, companhia e batalhão.
    - Valida nome, senha mínima e login único.
    - Gera ID automático.
    - Registra data e hora.
    - Pode criar automaticamente o policial correspondente.

6. Listar administradores:
    - Exibe todos os administradores cadastrados com
      ID, Nome, Login, Telefone, Matrícula, Patente,
      Companhia e Batalhão.

7. Login do administrador:
    - Solicita login e senha.
    - Permite acesso ao menu principal ao validar.
    - Em caso de erro, retorna ao menu inicial.

============================================================
4. FUNCIONALIDADES DE POLICIAL
============================================================

8. Cadastrar policial:
    - Solicita nome de guerra, matrícula, telefone,
      companhia, batalhão e patente (selecionada em lista).
    - Valida campos obrigatórios.
    - Gera ID automático.
    - Registra data e hora.

9. Listar policiais:
    - Exibe ID, Patente, Nome de Guerra, Matrícula,
      Telefone, Companhia e Batalhão.

============================================================
5. FUNCIONALIDADES DE VIATURAS
============================================================

10. Cadastrar viatura:
    - Solicita prefixo, placa, tipo (Moto ou 4 Rodas),
      KM, OS Prime, última revisão, telefone da oficina,
      observações e responsável.
    - Valida prefixo e placa únicos.
    - Gera ID automático.
    - Registra data e hora.

11. Listar viaturas:
    - Exibe ID, Prefixo, Placa, Tipo, KM, OS Prime,
      Última Revisão e Responsável.

12. Pesquisar viatura por prefixo:
    - Retorna todas as viaturas com o prefixo informado.

13. Pesquisar viatura por OS Prime:
    - Retorna viaturas com a OS Prime informada.

14. Relatório de situação:
    - Total de viaturas cadastradas.
    - Viaturas baixadas (com OS Prime).
    - Viaturas disponíveis.
    - Informações detalhadas das viaturas baixadas.

============================================================
6. FUNCIONALIDADES DE MENUS
============================================================

15. Menu inicial:
    - Cadastrar administrador.
    - Login.
    - Sair.

16. Menu principal (após login):
    - Cadastrar viatura.
    - Listar viaturas.
    - Pesquisar por prefixo.
    - Pesquisar por OS Prime.
    - Gerar relatório de viaturas.
    - Cadastrar policial.
    - Listar policiais.
    - Listar administradores.
    - Criar backup.
    - Voltar ao menu inicial.
    - Sair.

============================================================
7. VALIDAÇÕES E REGRAS DO SISTEMA
============================================================

- IDs gerados automaticamente.
- Prefixo e placa das viaturas são únicos.
- Login do administrador é único.
- Telefone deve ter 11 dígitos.
- Tipo da viatura deve ser apenas "Moto" ou "4 Rodas".
- Campos opcionais podem permanecer em branco.
- Datas de criação registradas automaticamente.
- Cadastro de administrador pode criar policial correspondente.

============================================================
8. REQUISITOS PARA EXECUÇÃO
============================================================

- Python instalado.
- Sistema executado pelo terminal.
- Persistência em JSON ou SQL.
- Biblioteca shutil para backup.
- Estrutura modular recomendada:
      - armazenamento.py
      - viaturas.py
      - policiais.py
      - administradores.py
      - uteis.py

============================================================
FIM DO DOCUMENTO
============================================================
"""
