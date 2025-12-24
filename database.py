import os
from supabase import create_client, Client


url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key) if url and key else None


def listar_todas_tarefas():
    # Faz a consulta na tabela "tarefas"
    response = supabase.table("tarefas") \
        .select("*") \
        .order("ID", desc=True) \
        .execute()
    return response.data


def criar_tarefa(descricao, status="", data="", responsavel="", observacoes="", PDF=""):
    if not supabase:
        return None
    # Ajustado para bater com as colunas do seu print
    dados = {
        "Descrição": descricao,
        "Status": status,
        "Data": data,
        "Responsável": responsavel,
        "Observações": observacoes,
        "PDF": PDF
    }
    response = supabase.table("tarefas").insert(dados).execute()
    return response.data
