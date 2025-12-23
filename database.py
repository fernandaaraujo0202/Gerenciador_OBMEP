import os
from supabase import create_client, Client
from datetime import datetime


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
