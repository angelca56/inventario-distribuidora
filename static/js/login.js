document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const correoInput = document.getElementById("correo");
    const passwordInput = document.getElementById("password");
    const mensajeError = document.getElementById("error-msg");
    const loginBtn = document.getElementById("login-btn");
    const loader = document.getElementById("loader");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Evita el envío normal del formulario

        const correo = correoInput.value.trim();
        const password = passwordInput.value.trim();

        // Limpiar errores anteriores
        mensajeError.textContent = "";
        mensajeError.style.opacity = "0";
        mensajeError.style.color = "red";
        correoInput.classList.remove("error");
        passwordInput.classList.remove("error");

        // Validar que los campos no estén vacíos
        if (!correo || !password) {
            mensajeError.textContent = "⚠️ Todos los campos son obligatorios.";
            mensajeError.style.opacity = "1";
            if (!correo) correoInput.classList.add("error");
            if (!password) passwordInput.classList.add("error");
            return;
        }

        // Deshabilitar el botón y mostrar el loader
        loginBtn.disabled = true;
        loader.style.display = "inline-block";
        loginBtn.querySelector("span").textContent = "Ingresando...";

        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ correo, password })  // Enviamos JSON
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                mensajeError.textContent = data.error;
                mensajeError.style.opacity = "1";
                correoInput.classList.add("error");
                passwordInput.classList.add("error");

                // Reactivar el botón y ocultar el loader
                loginBtn.disabled = false;
                loader.style.display = "none";
                loginBtn.querySelector("span").textContent = "Ingresar";
            } else {
                mensajeError.textContent = "✅ Ingresando...";
                mensajeError.style.color = "green";
                setTimeout(() => {
                    window.location.href = data.redirect; // Redirigir según el rol
                }, 1000);
            }
        })
        .catch(error => {
            console.error("❌ Error en fetch:", error);
            mensajeError.textContent = "❌ Error de conexión con el servidor";
            mensajeError.style.opacity = "1";

            // Reactivar el botón y ocultar el loader
            loginBtn.disabled = false;
            loader.style.display = "none";
            loginBtn.querySelector("span").textContent = "Ingresar";
        });
    });
});