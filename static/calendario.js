const calendario = document.getElementById("calendario");
const titulo = document.getElementById("mes-ano");
const painel = document.getElementById("painel");

const hoje = new Date();

let anoAtual = hoje.getFullYear();
let mesAtual = hoje.getMonth();

const meses = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
];

function criarCalendario() {
    titulo.textContent = `${meses[mesAtual]} ${anoAtual}`;
    calendario.innerHTML = "";

    const primeiroDia = new Date(anoAtual, mesAtual, 1).getDay();
    const totalDias = new Date(anoAtual, mesAtual + 1, 0).getDate();

    // espaços vazios antes do dia 1
    for (let i = 0; i < primeiroDia; i++) {
        calendario.appendChild(document.createElement("div"));
    }

    for (let dia = 1; dia <= totalDias; dia++) {
        const div = document.createElement("div");
        div.className = "dia";
        div.textContent = dia;

        const data = new Date(anoAtual, mesAtual, dia);
        const diaSemana = data.getDay(); // 0 = domingo, 6 = sábado

        // fim de semana
        if (diaSemana === 0 || diaSemana === 6) {
            div.classList.add("fim-semana");
        }

        // hoje
        if (
            dia === hoje.getDate() &&
            mesAtual === hoje.getMonth() &&
            anoAtual === hoje.getFullYear()
        ) {
            div.classList.add("hoje");
        }

        // clique no dia
        div.addEventListener("click", () => {
            document
                .querySelectorAll(".dia")
                .forEach(d => d.classList.remove("selecionado"));

            div.classList.add("selecionado");

            const diaFormatado = String(dia).padStart(2, "0");
            const mesFormatado = String(mesAtual + 1).padStart(2, "0");
            const dataFormatada = `${diaFormatado}/${mesFormatado}/${anoAtual}`;

            painel.innerHTML = `
                <div class="notas-header">
                    <strong>${dataFormatada}</strong>
                    <button class="botao-nota">+ Nota</button>
                </div>

                <div id="lista-notas"></div>
            `;

            const botao = painel.querySelector(".botao-nota");
            const listaNotas = painel.querySelector("#lista-notas");

            botao.addEventListener("click", () => {
                const nota = document.createElement("div");
                nota.className = "nota";
                nota.innerHTML = `
    <input 
        type="text" 
        class="nota-titulo" 
        placeholder="Título"
    >
    <textarea 
        rows="3" 
        placeholder="Escreva sua nota..."
    ></textarea>
`;

                listaNotas.appendChild(nota);
            });
        });

        calendario.appendChild(div);
    }
}

// teclado: ← mês anterior | → próximo mês
document.addEventListener("keydown", (e) => {
    if (e.key === "ArrowLeft") {
        mesAtual--;
        if (mesAtual < 0) {
            mesAtual = 11;
            anoAtual--;
        }
        criarCalendario();
    }

    if (e.key === "ArrowRight") {
        mesAtual++;
        if (mesAtual > 11) {
            mesAtual = 0;
            anoAtual++;
        }
        criarCalendario();
    }
});

criarCalendario();
