from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import database


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request):
    tarefas = database.listar_tarefas()
    return templates.TemplateResponse(
        "tarefas.html",
        {"request": request, "tarefas": tarefas}
    )


@app.post("/tarefas")
def salvar_tarefa(
    id: str = Form(None),
    descricao: str = Form(""),
    status: str = Form(""),
    data: str = Form(""),
    responsavel: str = Form(""),
    observacoes: str = Form(""),
    PDF: str = Form(""),
    remover: str = Form(None)
):
    # 🗑️ Remover
    if remover:
        database.remover_tarefas([int(remover)])
        return RedirectResponse("/", status_code=303)

    dados = {
        "Descrição": descricao,
        "Status": status,
        "Data": data or None,
        "Responsável": responsavel,
        "Observações": observacoes,
        "PDF": PDF
    }

    # ✏️ Atualizar
    if id:
        database.atualizar_tarefa(int(id), dados)

    # ➕ Criar nova tarefa
    elif any(dados.values()):
        database.inserir_tarefa(dados)

    return RedirectResponse("/tarefas", status_code=303)
