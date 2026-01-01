
/* ================== CRIAÇÃO AUTOMÁTICA ================== */
document.addEventListener("change", function (e) {
    const el = e.target;
    if (!["INPUT", "SELECT"].includes(el.tagName)) return;

    const tr = el.closest("tr");
    if (!tr || !tr.classList.contains("linha-nova")) return;

    if (el.value && !tr.dataset.criada) {
        tr.dataset.criada = "true";

        fetch("/criar-tarefa", { method: "POST" })
            .then(r => r.json())
            .then(data => {
                const id = data.id;

                tr.querySelectorAll("input, select")
                  .forEach(c => c.dataset.id = id);

                tr.classList.remove("linha-nova");

                salvarCampo(el);
                criarNovaLinha();
            });
    }
});

/* ================== SALVAR INPUT E SELECT ================== */
document.addEventListener("blur", e => {
    if (["INPUT", "SELECT"].includes(e.target.tagName)) {
        salvarCampo(e.target);
    }
}, true);

document.addEventListener("change", e => {
    if (e.target.tagName === "SELECT") {
        salvarCampo(e.target);
    }
});

function salvarCampo(el) {
    if (!el.dataset.id || !el.dataset.coluna) return;

    fetch("/atualizar-celula", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            id: Number(el.dataset.id),
            coluna: el.dataset.coluna,
            valor: el.value
        })
    }).then(() => {
        el.style.background = "#d4f8d4";
        setTimeout(() => el.style.background = "", 600);
    });
}

/* ================== UPLOAD PDF ================== */
function uploadPDF(input) {
    const id = input.dataset.id;
    if (!id || !input.files[0]) return;

    const fd = new FormData();
    fd.append("id", id);
    fd.append("file", input.files[0]);

    fetch("/upload-pdf", { method:"POST", body:fd })
        .then(() => location.reload());
}

/* ================== REMOVER ================== */
function removerSelecionados() {
    const ids = [...document.querySelectorAll(".chk-remover:checked")]
        .map(c => Number(c.dataset.id));

    if (!ids.length) return alert("Selecione uma linha");

    fetch("/remover-tarefas", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify(ids)
    }).then(() => location.reload());
}

/* ================== NOVA LINHA ================== */
function criarNovaLinha() {
    const tr = document.createElement("tr");
    tr.className = "linha-nova";
    tr.innerHTML = `
        <td><input type="checkbox"></td>
        <td><input type="text" data-coluna="Descrição"></td>
        <td>
            <select data-coluna="Status">
                <option value="">-- selecione --</option>
                <option>A fazer</option>
                <option>Em andamento</option>
                <option>Concluído</option>
            </select>
        </td>
        <td><input type="date" data-coluna="Data"></td>
        <td><input type="text" data-coluna="Responsável"></td>
        <td><input type="text" data-coluna="Observações"></td>
        <td><input type="file" onchange="uploadPDF(this)"></td>
    `;
    document.querySelector("tbody").appendChild(tr);
}


function filtrarStatus() {
    const filtro = document.getElementById("filtro-status").value;
    const linhas = document.querySelectorAll("tbody tr");

    linhas.forEach(tr => {
        // não filtra a linha nova
        if (tr.classList.contains("linha-nova")) return;

        const selectStatus = tr.querySelector('select[data-coluna="Status"]');
        if (!selectStatus) return;

        const statusLinha = selectStatus.value;

        if (!filtro || statusLinha === filtro) {
            tr.style.display = "";
        } else {
            tr.style.display = "none";
        }
    });
}

function toggleFiltroStatus() {
    const select = document.getElementById("filtro-status");
    select.style.display = select.style.display === "none" ? "block" : "none";
}

function fecharFiltroStatus() {
    document.getElementById("filtro-status").style.display = "none";
}
