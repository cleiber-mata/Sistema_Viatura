# ============================================================
# SISTEMA DE GERENCIAMENTO DE VIATURAS, POLICIAIS E ADMINISTRADORES
# ============================================================

# ============================================================
# REQUISITOS DO SISTEMA
# ============================================================
# - Permitir cadastro de administradores com login e senha.
# - Permitir cadastro de policiais com dados completos:
#   nome de guerra, matrícula, patente, companhia, batalhão, telefone.
# - Permitir cadastro de viaturas com os seguintes dados:
#   prefixo (único), placa (única), tipo (Moto ou 4 Rodas), KM atual,
#   OS Prime, data da última revisão, telefone da oficina, observações e responsável.
# - Identificar automaticamente viaturas com OS Prime (viaturas baixadas)
#   e viaturas disponíveis.
# - Pesquisar viaturas por prefixo ou por OS Prime.
# - Registrar data e hora de cadastro de usuários, policiais e viaturas.
# - Exigir login do administrador antes de acessar o menu principal.
# - Permitir backup opcional da pasta de dados.
# - Manter interface em linha de comando (terminal).
# - Persistência de dados em JSON ou banco de dados SQL.
# - IDs para administradores, policiais e viaturas são gerados automaticamente.
# - Validar campos obrigatórios e impedir duplicidades (login, prefixo, placa).

# ============================================================
# FUNCIONALIDADES GERAIS
# ============================================================

# 1. Limpeza de Tela
#    - Limpa o terminal (Windows e Linux).

# 2. Pausa no Sistema
#    - Aguarda alguns segundos antes de continuar.

# 3. Aguardo de Enter
#    - Espera o usuário pressionar Enter para avançar.

# 4. Backup de Dados
#    - Cria uma cópia completa da pasta 'data' com data e hora no nome.
#    - Utiliza biblioteca 'shutil' para copiar diretórios.

# ============================================================
# FUNCIONALIDADES DE ADMINISTRADOR
# ============================================================

# 5. Cadastrar Administrador
#    - Solicita:
#       - Nome completo
#       - Login
#       - Senha (mínimo 4 caracteres)
#       - Telefone (opcional)
#       - Matrícula (opcional)
#       - Patente (opcional)
#       - Companhia (opcional)
#       - Batalhão (opcional)
#    - Valida:
#       - Nome não vazio e apenas letras e espaços
#       - Login único
#       - Senha mínima
#    - Gera ID automático
#    - Registra data e hora do cadastro
#    - Pode criar automaticamente o policial correspondente

# 6. Listar Administradores
#    - Exibe todos os administradores cadastrados
#    - Formato: ID, Nome, Login, Telefone, Matrícula, Patente, Companhia, Batalhão

# 7. Login do Administrador
#    - Solicita login e senha
#    - Compara com os administradores cadastrados
#    - Permite acesso ao menu principal se estiver correto
#    - Em caso de erro, exibe mensagem e retorna ao menu inicial

# ============================================================
# FUNCIONALIDADES DE POLICIAL
# ============================================================

# 8. Cadastrar Policial
#    - Solicita:
#       - Nome de guerra
#       - Matrícula
#       - Telefone (DDD + número, 11 dígitos)
#       - Companhia
#       - Batalhão
#       - Patente (selecionada a partir de lista pré-definida)
#    - Valida campos obrigatórios
#    - Gera ID automático
#    - Registra data e hora do cadastro

# 9. Listar Policiais
#    - Exibe todos os policiais cadastrados
#    - Formato: ID, Patente, Nome de Guerra, Matrícula, Telefone, Companhia, Batalhão

# ============================================================
# FUNCIONALIDADES DE VIATURAS
# ============================================================

# 10. Cadastrar Viatura
#     - Solicita:
#        - Prefixo (único)
#        - Placa (única)
#        - Tipo (Moto ou 4 Rodas)
#        - KM atual (opcional)
#        - OS Prime (opcional)
#        - Data da última revisão (opcional)
#        - Telefone da oficina (opcional)
#        - Observações (opcional)
#        - Responsável (opcional)
#     - Valida campos obrigatórios
#     - Gera ID automático
#     - Registra data e hora do cadastro

# 11. Listar Viaturas
#     - Exibe todas as viaturas cadastradas
#     - Formato: ID, Prefixo, Placa, Tipo, KM, OS Prime, Última Revisão, Responsável

# 12. Pesquisar Viatura por Prefixo
#     - Solicita prefixo
#     - Retorna todas as viaturas com esse prefixo

# 13. Pesquisar Viatura por OS Prime
#     - Solicita OS Prime
#     - Retorna todas as viaturas com essa OS Prime

# 14. Relatório de Situação das Viaturas
#     - Mostra:
#        - Total de viaturas cadastradas
#        - Viaturas baixadas (com OS Prime)
#        - Viaturas disponíveis (sem OS Prime)
#     - Exibe detalhes das viaturas baixadas:
#        - Prefixo, Placa, KM, Próxima Revisão, OS Prime

# ============================================================
# FUNCIONALIDADES DE MENUS
# ============================================================

# 15. Menu Inicial
#     - Cadastrar administrador
#     - Login
#     - Sair do programa

# 16. Menu Principal (Após Login)
#     - Cadastrar viatura
#     - Listar viaturas
#     - Pesquisar viatura por prefixo
#     - Pesquisar viatura por OS Prime
#     - Gerar relatório de viaturas
#     - Cadastrar policial
#     - Listar policiais
#     - Listar administradores
#     - Criar backup
#     - Voltar ao menu inicial
#     - Sair do programa

# ============================================================
# VALIDAÇÕES E REGRAS
# ============================================================

# - Todos os IDs são gerados automaticamente incrementando o último cadastrado
# - Prefixo e Placa das viaturas devem ser únicos
# - Login dos administradores deve ser único
# - Nome de guerra e matrícula do policial devem ser válidos
# - Telefone deve ter 11 dígitos
# - Tipo de viatura só pode ser 'Moto' ou '4 Rodas'
# - Campos opcionais podem ficar em branco
# - Data de cadastro registrada automaticamente
# - Cadastro inicial de administrador cria automaticamente um policial correspondente

# ============================================================
# REQUISITOS DE EXECUÇÃO
# ============================================================

# - Python instalado
# - Execução via terminal (cmd, PowerShell ou Linux)
# - Persistência de dados em JSON ou banco SQL
# - Biblioteca 'shutil' para backup (opcional)
# - Interface em linha de comando
# - Todos os dados são salvos automaticamente nos arquivos correspondentes
# - Sistema modular, permitindo separação de módulos:
#       - armazenamento.py
#       - viaturas.py
#       - policiais.py
#       - administradores.py
#       - uteis.py

# ============================================================
# FIM DOS COMENTÁRIOS / DOCUMENTAÇÃO COMPLETA
# ============================================================
