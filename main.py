import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import listar_todas_tarefas, criar_tarefa

app = FastAPI()

# Configura a pasta de templates
templates = Jinja2Templates(directory="templates")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    tarefas = listar_todas_tarefas()
    return templates.TemplateResponse("tarefas.html", {
        "request": request,
        "tarefas": tarefas,
        "usuario": "Usuário"
    })


@app.post("/tarefas", response_class=HTMLResponse)
def nova_tarefa(
    request: Request,
    descricao: str = Form(...),
    status: str = Form("Pendente"),
    responsavel: str = Form(""),
    observacoes: str = Form(""),
    PDF: str = Form("")
):
    criar_tarefa(descricao, status, responsavel, observacoes, PDF)
    tarefas = listar_todas_tarefas()
    return templates.TemplateResponse("tarefas.html", {
        "request": request,
        "tarefas": tarefas,
        "usuario": "Usuário"
    })


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
