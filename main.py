# subir o servidor

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# importa a classe FastAPI e requisição HTTP
from fastapi import FastAPI, Request
# permite misturar html e pythom, envia dados do backend para o HTML
from fastapi.templating import Jinja2Templates
from fastapi import Form  # receber dados enviados pelo form do HTML
# importa resposta que redireciona o navegador para outra pagina
from fastapi.responses import RedirectResponse
from database import criar_tabela, listar_tarefas_por_status
from database import listar_todas_tarefas, adicionar_tarefa, atualizar_tarefas


usuario_autorizado = ["Seme", "Amanda", "Fernanda", "Aline"]

criar_tabela()

# app é o servidor. Nele definimos rotas e métodos (GET, POST, PUT...)
app = FastAPI()


# diz ao FastAPI onde então os arquivos  HTML e "templates" é o nome da pasta
templates = Jinja2Templates(directory="templates")

# define uma rota "/" é a página inicial


@app.get("/")  # rota do tipo get
# função da rota, recebe requisição do navegador
def home(request: Request):
    usuario = request.cookies.get("usuario")

    if not usuario:
        # retorna resposta em HTML (.TemplatesResponse),envia o dicionario para o HTML
        return templates.TemplateResponse("login.html", {"request": request})

    return RedirectResponse(url="/tarefas", status_code=302)


@app.post("/login")  # cria rota que recebe dados enviados pelo formulário HTML
# campo usuario, valor string, vem de um formulário HTML, com campo obrigatório (corresponde ao input usuario do HTML)
def login_post(request: Request, usuario: str = Form(...)):
    if usuario not in usuario_autorizado:
        return templates.TemplateResponse("login.html", {"request": request, "erro": "Login incorreto"})

    # 302 é redirecionamento temporario
    response = RedirectResponse(url="/", status_code=302)
    # cria o cookie usuario enquanto o navegador estiver aberto
    response.set_cookie(key="usuario", value=usuario, httponly=True)
    return response  # o navegador salva o cookie e redireciona


@app.get("/logout")
def logout(request: Request):
    # remove usuário da sessão (se existir)
    request.session.pop("usuario", None)

    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("usuario")
    return response


@app.get("/tarefas")
def listar_tarefas_view(request: Request):
    usuario = request.cookies.get("usuario")
    if not usuario:
        return RedirectResponse(url="/login", status_code=302)

    tarefas_db = listar_todas_tarefas()

    return templates.TemplateResponse("tarefas.html", {"request": request, "usuario": usuario, "tarefas": tarefas_db})


@app.post("/tarefas")
def criar_tarefa(request: Request, titulo: str = Form(...)):
    usuario = request.cookies.get("usuario")
    if not usuario:
        return RedirectResponse(url="/login", status_code=302)

    adicionar_tarefa(usuario, titulo)

    return RedirectResponse(url="/tarefas", status_code=302)


@app.post("/tarefas/{tarefa_id}/status")
def mudar_status(tarefa_id: int, status: str = Form(...)):
    atualizar_tarefas(tarefa_id, status)
    return RedirectResponse(url="/tarefas", status_code=302)


@app.get("/tarefas/status/{status}")
def tarefas_filtradas(request: Request, status: str):
    mapa_status = {
        "afazer": "A fazer",
        "andamento": "Em andamento",
        "concluida": "Concluída"
    }

    status_real = mapa_status.get(status)

    if not status_real:
        return RedirectResponse(url="/tarefas", status_code=302)

    tarefas_db = listar_tarefas_por_status(status_real)

    return templates.TemplateResponse(
        "tarefas.html",
        {
            "request": request,
            "tarefas": tarefas_db,
            "filtro": status_real
        }
    )
