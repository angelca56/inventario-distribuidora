document.addEventListener("DOMContentLoaded", function () {
    const botones = document.querySelectorAll(".boton-notificacion");

    botones.forEach(boton => {
        boton.addEventListener("mouseenter", () => {
            boton.classList.add("boton-hover");
        });

        boton.addEventListener("mouseleave", () => {
            boton.classList.remove("boton-hover");
        });

        boton.addEventListener("mousedown", () => {
            boton.classList.add("boton-clic");
        });

        boton.addEventListener("mouseup", () => {
            boton.classList.remove("boton-clic");
        });
    });

    document.getElementById("btnEntrada").addEventListener("click", function () {
        document.body.classList.add("fade-out");
        setTimeout(() => {
            window.location.href = "/notificaciones_entrada";
        }, 300);
    });

    document.getElementById("btnVenta").addEventListener("click", function () {
        document.body.classList.add("fade-out");
        setTimeout(() => {
            window.location.href = "/notificaciones_venta";
        }, 300);
    });
});