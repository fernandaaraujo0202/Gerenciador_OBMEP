# database.py
import os
from datetime import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()  # Para carregar variáveis do .env local

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def criar_tabela():
    """
    Via API, criar tabela não é possível.
    Execute este SQL no Supabase:

    create table if not exists tarefas (
        id serial primary key,
        descricao text not null,
        status text not null,
        data timestamp default now(),
        responsavel text not null,
        observacoes text,
        pdf text
    );
    """
    pass


def adicionar_tarefa(responsavel, descricao, observacoes="", pdf=""):
    supabase.table("tarefas").insert({
        "responsavel": responsavel,
        "descricao": descricao,
        "status": "A fazer",
        "data": datetime.now(),
        "observacoes": observacoes,
        "pdf": pdf
    }).execute()


def listar_todas_tarefas():
    res = supabase.table("tarefas").select(
        "*").order("id", desc=True).execute()
    return res.data


def atualizar_tarefas(tarefa_id, novo_status):
    supabase.table("tarefas").update(
        {"status": novo_status}).eq("id", tarefa_id).execute()


def listar_tarefas_por_status(status):
    res = supabase.table("tarefas").select("*").eq("status", status).execute()
    return res.data
