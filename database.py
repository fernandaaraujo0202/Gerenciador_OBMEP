import os
from supabase import create_client, Client
from dotenv import load_dotenv
import tempfile
import unicodedata
import re

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


def atualizar_celula(tarefa_id, coluna, valor):
    if not supabase:
        return
    supabase.table(TABLE) \
        .update({coluna: valor}) \
        .eq("ID", tarefa_id) \
        .execute()


def limpar_nome_arquivo(nome):
    nome = unicodedata.normalize("NFKD", nome).encode(
        "ascii", "ignore").decode("ascii")
    nome = re.sub(r"[^a-zA-Z0-9._-]", "_", nome)
    return nome


def salvar_pdf(tarefa_id, upload_file):
    import tempfile
    import os

    nome_limpo = limpar_nome_arquivo(upload_file.filename)
    caminho = f"{tarefa_id}_{nome_limpo}"

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(upload_file.file.read())
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        supabase.storage.from_("pdfs").upload(
            caminho,
            f,
            file_options={
                "content-type": upload_file.content_type
            }
        )

    os.remove(tmp_path)

    url = supabase.storage.from_("pdfs").get_public_url(caminho)

    supabase.table("tarefas") \
        .update({"PDF": url}) \
        .eq("ID", tarefa_id) \
        .execute()
