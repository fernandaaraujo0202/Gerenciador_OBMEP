from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "eventos"


def listar_eventos_por_data(data):
    return supabase.table(TABLE) \
        .select("*") \
        .eq("data", data) \
        .order("id") \
        .execute().data or []


def inserir_evento(titulo, descricao, data):
    res = supabase.table(TABLE).insert({
        "titulo": titulo,
        "descricao": descricao,
        "data": data
    }).execute()
    return res.data[0]
