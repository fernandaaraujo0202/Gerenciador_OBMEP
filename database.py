import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key) if url and key else None


def listar_todas_tarefas():
    if not supabase:
        return []
    # Usando os nomes exatos das colunas da sua imagem
    response = supabase.table("tarefas").select(
        "*").order("ID", desc=True).execute()
    return response.data


def criar_tarefa(descricao, status="", responsavel="", observacoes="", pdf=""):
    if not supabase:
        return None
    # Ajustado para bater com as colunas do seu print
    dados = {
        "Descrição": descricao,
        "Status": status,
        "Responsável": responsavel,
        "Observações": observacoes,
        "PDF": PDF  # Adicione esta coluna no Supabase!
    }
    response = supabase.table("tarefas").insert(dados).execute()
    return response.data
