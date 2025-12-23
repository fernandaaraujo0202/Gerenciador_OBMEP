# main.py
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from database import (
    listar_todas_tarefas,
    adicionar_tarefa,
    atualizar_tarefas,
    listar_tarefas_por_status
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

usuarios_autorizados = ["Seme", "Amanda", "Fernanda", "Aline"]


@app.get("/")
def home(request: Request):
    usuario = request.cookies.get("usuario")
    if not usuario:
        return templates.TemplateResponse("login.html", {"request": request})
    return RedirectResponse("/tarefas", status_code=302)


@app.post("/login")
def login(request: Request, usuario: str = Form(...)):
    if usuario not in usuarios_autorizados:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Usuário não autorizado"}
        )
    response = RedirectResponse("/tarefas", status_code=302)
    response.set_cookie("usuario", usuario, httponly=True)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("usuario")
    return response


@app.get("/tarefas")
def tarefas(request: Request):
    usuario = request.cookies.get("usuario")
    if not usuario:
        return RedirectResponse("/", status_code=302)

    tarefas_db = listar_todas_tarefas()
    return templates.TemplateResponse(
        "tarefas.html",
        {"request": request, "usuario": usuario, "tarefas": tarefas_db}
    )


@app.post("/tarefas")
def criar_tarefa(
    request: Request,
    descricao: str = Form(...),
    observacoes: str = Form(""),
    pdf: str = Form("")
):
    responsavel = request.cookies.get("usuario")
    if not responsavel:
        return RedirectResponse("/", status_code=302)

    adicionar_tarefa(responsavel, descricao, observacoes, pdf)
    return RedirectResponse("/tarefas", status_code=302)


@app.post("/tarefas/{tarefa_id}/status")
def mudar_status(tarefa_id: int, status: str = Form(...)):
    atualizar_tarefas(tarefa_id, status)
    return RedirectResponse("/tarefas", status_code=302)


@app.get("/tarefas/status/{status}")
def filtrar_status(request: Request, status: str):
    mapa = {
        "afazer": "A fazer",
        "andamento": "Em andamento",
        "concluida": "Concluída"
    }

    status_real = mapa.get(status)
    if not status_real:
        return RedirectResponse("/tarefas", status_code=302)

    tarefas_db = listar_tarefas_por_status(status_real)
    return templates.TemplateResponse(
        "tarefas.html",
        {"request": request, "tarefas": tarefas_db, "filtro": status_real}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
