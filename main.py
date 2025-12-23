import os
import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from database import listar_todas_tarefas, criar_tarefa

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home():
    tarefas = listar_todas_tarefas()
    html = "<h1>Gerenciador OBMEP</h1><hr><ul>"
    for t in tarefas:
        # Usando os nomes das colunas com a primeira letra maiúscula conforme seu print
        desc = t.get('Descrição', 'Sem título')
        status = t.get('Status', 'Pendente')
        html += f"<li>{desc} - <b>{status}</b></li>"
    html += "</ul>"
    return html


@app.post("/tarefas", response_class=HTMLResponse)
def nova_tarefa(descricao: str = Form(...), status: str = Form("Pendente"),
                responsavel: str = Form(""), observacoes: str = Form(""), pdf: str = Form("")):
    criar_tarefa(descricao, status, responsavel, observacoes, pdf)
    return "Tarefa criada! <a href='/'>Voltar</a>"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
