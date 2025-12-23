import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# carrega o .env (LOCAL) ou ignora se estiver no Railway
load_dotenv()


def get_connection():
    url = os.getenv("DATABASE_URL")

    if not url:
        raise ValueError(
            "ERRO: A variável DATABASE_URL não foi configurada no ambiente!"
        )

    return psycopg2.connect(
        url,
        cursor_factory=RealDictCursor,
        sslmode="require"
    )


def criar_tabela():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            status TEXT NOT NULL,
            usuario TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()


def adicionar_tarefa(usuario, titulo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tarefas (usuario, titulo, status) VALUES (%s, %s, %s)",
        (usuario, titulo, "A fazer")
    )

    conn.commit()
    conn.close()


def listar_todas_tarefas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, titulo, status, usuario FROM tarefas ORDER BY id DESC"
    )

    tarefas = cursor.fetchall()
    conn.close()
    return tarefas


def atualizar_tarefas(tarefa_id, novo_status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tarefas SET status = %s WHERE id = %s",
        (novo_status, tarefa_id)
    )

    conn.commit()
    conn.close()


def listar_tarefas_por_status(status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, titulo, status, usuario FROM tarefas WHERE status = %s",
        (status,)
    )

    tarefas = cursor.fetchall()
    conn.close()
    return tarefas
