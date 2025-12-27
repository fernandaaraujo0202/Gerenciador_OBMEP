from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import atualizar_celula
from pydantic import BaseModel
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
    # Remover
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

    return RedirectResponse("/", status_code=303)


class Atualizacao(BaseModel):
    id: int
    coluna: str
    valor: str


@app.post("/atualizar-celula")
async def atualizar(dados: Atualizacao):
    atualizar_celula(dados.id, dados.coluna, dados.valor)
    return {"ok": True}


@app.post("/upload-pdf")
async def upload_pdf(
    id: int = Form(...),
    file: UploadFile = File(...)
):
    try:
        database.salvar_pdf(id, file)
        return {"ok": True}
    except Exception as e:
        print("ERRO UPLOAD PDF:", e)
        return {"ok": False, "erro": str(e)}
