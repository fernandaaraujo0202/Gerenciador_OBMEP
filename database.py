import sqlite3


def get_connection():
    conn = sqlite3.connect("database.db")  # conn é o banco aberto
    conn.row_factory = sqlite3.Row  # .row_factory permite acessar colunas pelo nome
    return conn


def criar_tabela():
    conn = get_connection()  # cria conexão com o banco de dados
    cursor = conn.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            status TEXT NOT NULL,
            usuario TEXT NOT NULL)""")
    conn.commit()  # salva definitivamente a alteração no banco
    conn.close()  # fecha a conexão com o banco


def adicionar_tarefa(usuario, titulo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tarefas (usuario, titulo,status) VALUES (?, ?,?)",
        (usuario, titulo, "pendente")
    )

    conn.commit()
    conn.close()


def listar_todas_tarefas():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, titulo, status, usuario FROM tarefas")
    tarefas = cursor.fetchall()
    conn.close()

    return tarefas


def atualizar_tarefas(tarefa_id, novo_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(" UPDATE tarefas SET status = ? WHERE id = ?",
                   (novo_status, tarefa_id))

    conn.commit()  # salva definitivamente a alteração no banco
    conn.close()  # fecha a conexão com o banco


def listar_tarefas_por_status(status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        " SELECT id, titulo, status FROM tarefas WHERE status = ?", (status,))

    tarefas = cursor.fetchall()
    conn.close()
    return tarefas
