import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()  # carrega .env se existir

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL ou SUPABASE_KEY não configuradas")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "tarefas"


def listar_tarefas():
    return supabase.table(TABLE).select("*").order("ID").execute().data or []


def inserir_tarefa(dados):
    supabase.table(TABLE).insert(dados).execute()


def atualizar_tarefa(id, dados):
    supabase.table(TABLE).update(dados).eq("ID", id).execute()


def remover_tarefas(ids):
    supabase.table(TABLE).delete().in_("ID", ids).execute()
