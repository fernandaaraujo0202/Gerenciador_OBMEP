import os
import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from database import listar_todas_tarefas, criar_tarefa

app = FastAPI(title="Gerenciador OBMEP")

# Rota de sobrevivência (Health Check) para o UptimeRobot bater aqui


@app.get("/health")
def health_check():
    return {"status": "online", "message": "Estou acordado!"}

# Rota principal (Lista tarefas)


@app.get("/", response_class=HTMLResponse)
def home():
    tarefas = listar_todas_tarefas()

    html = """
    <html>
        <head><title>OBMEP - Gerenciador</title></head>
        <body>
            <h1>Lista de Tarefas</h1>
            <a href="/nova">Adicionar Nova Tarefa</a>
            <ul>
    """

    if not tarefas:
        html += "<li>Nenhuma tarefa encontrada ou erro na conexão.</li>"
    else:
        for t in tarefas:
            # Garante que chaves que podem ser None não quebrem o HTML
            desc = t.get('descricao', 'Sem descrição')
            status = t.get('status', 'Pendente')
            html += f"<li><strong>{desc}</strong> - Status: {status}</li>"

    html += "</ul></body></html>"
    return html

# Rota para processar a criação de tarefa


@app.post("/tarefas", response_class=HTMLResponse)
def nova_tarefa(
    descricao: str = Form(...),
    status: str = Form("Pendente"),
    responsavel: str = Form(""),
    observacoes: str = Form(""),
    pdf: str = Form("")
):
    resultado = criar_tarefa(descricao, status, responsavel, observacoes, pdf)
    if resultado:
        return f"<h2>Sucesso!</h2><p>Tarefa '{descricao}' criada.</p><a href='/'>Voltar</a>"
    else:
        return "<h2>Erro!</h2><p>Não foi possível salvar no banco.</p><a href='/'>Voltar</a>"


if __name__ == "__main__":
    # O Render usa a variável PORT, localmente usa 8000
    port = int(os.environ.get("PORT", 8000))
    # Usamos uvicorn.run(app, ...) para facilitar o deploy direto
    uvicorn.run(app, host="0.0.0.0", port=port)
