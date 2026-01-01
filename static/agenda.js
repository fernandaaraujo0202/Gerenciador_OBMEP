document.addEventListener("DOMContentLoaded", function () {
    const calendarEl = document.getElementById("calendar");

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        locale: "pt-br",

        dateClick(info) {
            alert("Você clicou em: " + info.dateStr);
        }
    });

    calendar.render();
});
