document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("form-agregar-carro").addEventListener("submit", function (event) {
        event.preventDefault(); // Evita que la página se recargue

        let codigo = document.getElementById("codigo").value.trim();
        let nombre = document.getElementById("nombre").value.trim();
        let categoria = document.getElementById("categoria").value.trim();
        let cantidad = Number(document.getElementById("cantidad").value) || 0;
        let precio = Number(document.getElementById("precio").value) || 0.0;

        if (codigo === "" || nombre === "" || categoria === "" ) {
            alert("⚠️ Todos los campos son obligatorios");
            return;
        }

        // 🔹 Enviar datos al servidor
        fetch("/api/agregar_producto_carro2", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ codigo, nombre, categoria, cantidad, precio }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("❌ " + data.error);
            } else {
                alert("✅ " + data.mensaje);
                window.location.href = "/inventario_carro2"; // Redirigir al inventario del carro
            }
        })
        .catch(error => {
            console.error("❌ Error al agregar el producto:", error);
            alert("❌ Hubo un error al agregar el producto.");
        });
    });
});
