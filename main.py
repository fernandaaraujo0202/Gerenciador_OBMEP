from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from database import criar_tabela, listar_todas_tarefas, criar_tarefa

app = FastAPI()

# Cria a tabela ao iniciar o app


@app.on_event("startup")
def startup_event():
    criar_tabela()

# Página inicial


@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Bem-vindo ao Gerenciador OBMEP!</h1>"

# Rota para listar tarefas


@app.get("/tarefas", response_class=HTMLResponse)
def tarefas():
    tarefas_db = listar_todas_tarefas()
    html = "<h2>Tarefas</h2><ul>"
    for t in tarefas_db:
        html += f"<li>{t['id']} - {t['descricao']} - {t['status']} - {t['responsavel']}</li>"
    html += "</ul>"
    return html

# Rota para criar tarefas via formulário


@app.post("/tarefas", response_class=HTMLResponse)
def criar(request: Request, descricao: str = Form(...), status: str = Form(""), responsavel: str = Form(""), observacoes: str = Form(""), pdf: str = Form("")):
    criar_tarefa(descricao, status, responsavel, observacoes, pdf)
    return RedirectResponse(url="/tarefas", status_code=302)
