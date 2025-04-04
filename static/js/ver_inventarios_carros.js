    // Función para regresar al panel según el rol
    document.getElementById("btnRegresarPanel").addEventListener("click", function () {
        window.location.href = "/regresar_panel"; // Ahora Flask se encarga de la redirección
    });

// Función para redirigir a la página seleccionada
function irA(url) {
    window.location.href = url;
}