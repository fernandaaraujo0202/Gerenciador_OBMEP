const calendario = document.getElementById("calendario");
const titulo = document.getElementById("mes-ano");

const hoje = new Date();
const ano = hoje.getFullYear();
const mes = hoje.getMonth();

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

    // dias do mês
    for (let dia = 1; dia <= totalDias; dia++) {
        const div = document.createElement("div");
        div.className = "dia";
        div.textContent = dia;
        calendario.appendChild(div);
    }
}

criarCalendario();

