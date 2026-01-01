from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import atualizar_celula
from pydantic import BaseModel
import database
from typing import List
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    SessionMiddleware,
    secret_key="uma-chave-bem-secreta-aqui"
)


@app.get("/")
def home(request: Request):
    usuario = request.session.get("usuario")

    if not usuario:
        return RedirectResponse("/login", status_code=303)

    tarefas = database.listar_tarefas()

    return templates.TemplateResponse("tarefas.html", {
        "request": request,
        "usuario": usuario,
        "tarefas": tarefas
    })

# ------------- TAREFAS ----------------


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


@app.post("/criar-tarefa")
def criar_tarefa():
    tarefa = database.inserir_tarefa({
        "Descrição": "",
        "Status": "",
        "Data": None,
        "Responsável": "",
        "Observações": "",
        "PDF": ""
    })
    return {"id": tarefa["ID"]}


@app.post("/remover-tarefas")
async def remover_tarefas(ids: list[int]):
    database.remover_tarefas(ids)
    return {"ok": True}


# ---------------- LOGIN ----------------
@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
def login(request: Request, usuario: str = Form(...)):

    USUARIO_VALIDO = "2026"  # <-- troque pelo nome que você quiser

    if usuario != USUARIO_VALIDO:
        return RedirectResponse("/login", status_code=303)

    request.session["usuario"] = usuario
    return RedirectResponse("/", status_code=303)


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


# ----------- AGENDA -----------

@app.get("/agenda")
def agenda_page(request: Request):
    usuario = request.session.get("usuario")
    if not usuario:
        return RedirectResponse("/login", status_code=303)

    return templates.TemplateResponse("agenda.html", {
        "request": request,
        "usuario": usuario
    })


class Evento(BaseModel):
    titulo: str
    data: str


@app.get("/eventos")
def listar_eventos(request: Request):
    usuario = request.session.get("usuario")
    return database.listar_eventos(usuario)


@app.post("/eventos")
def criar_evento(evento: Evento, request: Request):
    usuario = request.session.get("usuario")
    database.criar_evento(evento.titulo, evento.data, usuario)
    return {"ok": True}
