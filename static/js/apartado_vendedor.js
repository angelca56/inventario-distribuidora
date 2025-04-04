document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Panel de Vendedor cargado");

    // 🔹 Evento para cerrar sesión
    document.getElementById("btnCerrarSesion").addEventListener("click", function () {
        fetch("/logout", { method: "GET" }) // Hacer la petición al backend
        .then(response => {
            if (response.redirected) {
                window.location.href = response.url; // Redirigir al login
                }
            })
            .catch(error => console.error("❌ Error al cerrar sesión:", error));
        });

    // Animación al pasar el mouse sobre los botones
    document.querySelectorAll(".boton-vendedor").forEach((boton) => {
        boton.addEventListener("mouseenter", function () {
            this.classList.add("boton-hover");
        });

        boton.addEventListener("mouseleave", function () {
            this.classList.remove("boton-hover");
        });

        // Agregar efecto de "clic"
        boton.addEventListener("click", function () {
            this.classList.add("boton-clic");
            setTimeout(() => this.classList.remove("boton-clic"), 200); // Quita el efecto tras 200ms
        });
    });

    // ✅ FORZAR RECARGA AL USAR LA FLECHA "ATRÁS"
    window.addEventListener("pageshow", function (event) {
        if (event.persisted) {
            console.log("♻️ Recargando página por navegación hacia atrás");
            window.location.reload();
        }
    });

    // Función para redirigir al usuario a otra página
    window.irA = function (ruta) {
        console.log("🔀 Redirigiendo a:", ruta);

        // Efecto de desvanecimiento antes de cambiar de página
        document.body.classList.add("fade-out");

        setTimeout(() => {
            window.location.href = ruta;
        }, 500); // Espera 500ms antes de redirigir
    };
});