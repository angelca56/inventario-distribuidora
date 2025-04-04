document.addEventListener("DOMContentLoaded", function() {
    const botones = document.querySelectorAll(".btn");

    // Función para regresar al panel según el rol
    document.getElementById("btnRegresarPanel").addEventListener("click", function () {
        window.location.href = "/regresar_panel"; // Ahora Flask se encarga de la redirección
        });

    botones.forEach(boton => {
        boton.addEventListener("mouseenter", () => {
            boton.classList.add("boton-hover");
        });

        boton.addEventListener("mouseleave", () => {
            boton.classList.remove("boton-hover");
        });

        boton.addEventListener("click", function() {
            boton.classList.add("boton-clic");
            document.body.classList.add("fade-out");

            setTimeout(() => {
                if (boton.id === "btnVendedor1") {
                    window.location.href = "/notificaciones";
                } else if (boton.id === "btnVendedor2") {
                    window.location.href = "/notificaciones2"; // 🔹 Redirige a notificaciones2.html
                }
            }, 500);
        });
    });
});