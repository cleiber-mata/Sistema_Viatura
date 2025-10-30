# ------------------------------
# MÓDULO: armazenamento.py
# Finalidade: Gerenciar leitura, gravação e carregamento global dos dados do sistema
# ------------------------------

import os
import json
import datetime

# ------------------------------
# CONFIGURAÇÃO DE DIRETÓRIOS E ARQUIVOS
# ------------------------------
DATA_DIR = "data"
ARQUIVO_USUARIOS = f"{DATA_DIR}/usuarios.json"
ARQUIVO_ESTOQUE = f"{DATA_DIR}/estoque.json"
ARQUIVO_COLABORADORES = f"{DATA_DIR}/colaboradores.json"
ARQUIVO_LIXEIRA = f"{DATA_DIR}/lixeira.json"
ARQUIVO_VIATURAS = f"{DATA_DIR}/viaturas.json"

# Garante que o diretório de dados exista
os.makedirs(DATA_DIR, exist_ok=True)


# ------------------------------
# FUNÇÕES BÁSICAS DE JSON
# ------------------------------
def salvar_json(arquivo, dados):
    """Salva dados em formato JSON, com indentação e suporte a acentuação."""
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERRO] Falha ao salvar {arquivo}: {e}")


def carregar_json(arquivo):
    """Carrega dados JSON. Retorna lista vazia se o arquivo não existir ou estiver corrompido."""
    if os.path.exists(arquivo):
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"[AVISO] O arquivo '{arquivo}' está corrompido. Foi restaurado como lista vazia.")
            return []
        except Exception as e:
            print(f"[ERRO] Falha ao ler {arquivo}: {e}")
            return []
    return []


# ------------------------------
# FUNÇÕES DE SALVAMENTO E CARREGAMENTO GLOBAL
# ------------------------------
def carregar_dados():
    """Carrega todos os conjuntos de dados do sistema e retorna em um dicionário."""
    dados = {
        "usuarios": carregar_json(ARQUIVO_USUARIOS),
        "estoque": carregar_json(ARQUIVO_ESTOQUE),
        "colaboradores": carregar_json(ARQUIVO_COLABORADORES),
        "lixeira": carregar_json(ARQUIVO_LIXEIRA),
        "viaturas": carregar_json(ARQUIVO_VIATURAS),
    }

    # Identificadores automáticos
    dados["proximo_id_item"] = max([i["id"] for i in dados["estoque"]], default=0) + 1
    dados["proximo_id_colaborador"] = max([c["id"] for c in dados["colaboradores"]], default=0) + 1
    dados["proximo_id_viatura"] = max([v["id"] for v in dados["viaturas"]], default=0) + 1

    return dados


def salvar_dados(dados):
    """Salva todos os conjuntos de dados do sistema."""
    salvar_json(ARQUIVO_USUARIOS, dados.get("usuarios", []))
    salvar_json(ARQUIVO_ESTOQUE, dados.get("estoque", []))
    salvar_json(ARQUIVO_COLABORADORES, dados.get("colaboradores", []))
    salvar_json(ARQUIVO_LIXEIRA, dados.get("lixeira", []))
    salvar_json(ARQUIVO_VIATURAS, dados.get("viaturas", []))


# ------------------------------
# (Opcional) UTILITÁRIO DE BACKUP
# ------------------------------
def criar_backup():
    """Cria uma cópia completa da pasta 'data' com data e hora no nome."""
    try:
        import shutil
        data_agora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        destino = f"backup_{data_agora}"
        shutil.copytree(DATA_DIR, destino)
        print(f"[OK] Backup criado em '{destino}'")
    except Exception as e:
        print(f"[ERRO] Falha ao criar backup: {e}")
