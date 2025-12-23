from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from database import listar_todas_tarefas, criar_tarefa

app = FastAPI(title="Gerenciador OBMEP")

# Rota home


@app.get("/", response_class=HTMLResponse)
def home():
    tarefas = listar_todas_tarefas()
    html = "<h1>Lista de Tarefas</h1><ul>"
    for t in tarefas:
        html += f"<li>{t['id']}: {t['descricao']} - {t['status']}</li>"
    html += "</ul>"
    return html

# Criar tarefa via formulário


@app.post("/tarefas", response_class=HTMLResponse)
def nova_tarefa(
    descricao: str = Form(...),
    status: str = Form(...),
    data: str = Form(...),
    responsavel: str = Form(...),
    observacoes: str = Form(...),
    pdf: str = Form("")
):
    criar_tarefa(descricao, status, data, responsavel, observacoes, pdf)
    return f"Tarefa '{descricao}' criada com sucesso!"

# Atualizar ou deletar podem ser adicionados da mesma forma
