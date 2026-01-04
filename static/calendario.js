const calendario = document.getElementById("calendario");
const titulo = document.getElementById("mes-ano");

const hoje = new Date();
let ano = hoje.getFullYear();
let mes = hoje.getMonth();

const meses = [
    "Janeiro", "Fevereiro", "Março", "Abril",
    "Maio", "Junho", "Julho", "Agosto",
    "Setembro", "Outubro", "Novembro", "Dezembro"
];

function criarCalendario(){
    titulo.textContent=`${meses[mes]} ${ano}`;

    const primeiroDia = new Date(ano, mes, 1).getDay();
    const totalDias = new Date(ano, mes + 1, 0).getDate();

    calendario.innerHTML = "";

    // espaços vazios antes do dia 1
    for (let i = 0; i < primeiroDia; i++) {
        calendario.appendChild(document.createElement("div"));
    }

    for (let dia = 1; dia <= totalDias; dia++) {
    const div = document.createElement("div");
    div.className = "dia";
    div.textContent = dia;

    const data = new Date(ano, mes, dia);
    const diaSemana = data.getDay(); // 0 = domingo, 6 = sábado

    // fim de semana
    if (diaSemana === 0 || diaSemana === 7) {
        div.classList.add("fim-semana");
    }

    // hoje
    if (
        dia === hoje.getDate() &&
        mes === hoje.getMonth() &&
        ano === hoje.getFullYear()
    ) {
        div.classList.add("hoje");
    }

    calendario.appendChild(div);
}

}

criarCalendario();

function mesAnterior() {
    mes--;
    if (mes < 0) {
        mes = 11;
        ano--;
    }
    criarCalendario();
}

function proximoMes() {
    mes++;
    if (mes > 11) {
        mes = 0;
        ano++;
    }
    criarCalendario();
}

document.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
        mesAnterior();
    }

    if (event.key === "ArrowRight") {
        proximoMes();
    }
});



