import os
from supabase import create_client, Client
from datetime import datetime

# Pega as variáveis de ambiente definidas no Railway
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception(
        "As variáveis SUPABASE_URL e SUPABASE_KEY precisam estar definidas!")

# Cria o client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Função para criar a tabela caso ainda não exista


def criar_tabela():
    # Supabase normalmente já cria tabelas via dashboard ou migrations,
    # mas se quiser criar via Python, use a API SQL:
    supabase.rpc(
        "sql",
        {"query": """
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            descricao TEXT NOT NULL,
            status TEXT,
            data TIMESTAMP DEFAULT NOW(),
            responsavel TEXT,
            observacoes TEXT,
            pdf TEXT
        );
        """}
    ).execute()

# Funções de manipulação de tarefas


def listar_todas_tarefas():
    response = supabase.table("tarefas").select(
        "*").order("id", desc=True).execute()
    return response.data


def criar_tarefa(descricao, status="", responsavel="", observacoes="", pdf=""):
    response = supabase.table("tarefas").insert({
        "descricao": descricao,
        "status": status,
        "responsavel": responsavel,
        "observacoes": observacoes,
        "pdf": pdf
    }).execute()
    return response.data
