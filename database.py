import os
from supabase import create_client, Client

# Pega as chaves das variáveis de ambiente do Render/Railway
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# Inicializa o cliente apenas se as chaves existirem
if not url or not key:
    print("AVISO: SUPABASE_URL ou SUPABASE_KEY não configuradas!")
    supabase = None
else:
    supabase: Client = create_client(url, key)


def listar_todas_tarefas():
    if not supabase:
        return []
    try:
        response = supabase.table("tarefas").select(
            "*").order("id", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao listar: {e}")
        return []


def criar_tarefa(descricao, status="", responsavel="", observacoes="", pdf=""):
    if not supabase:
        return None
    try:
        data_to_insert = {
            "descricao": descricao,
            "status": status,
            "responsavel": responsavel,
            "observacoes": observacoes,
            "pdf": pdf
        }
        response = supabase.table("tarefas").insert(data_to_insert).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao criar: {e}")
        return None
