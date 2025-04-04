document.addEventListener("DOMContentLoaded", function () {
    const formRegistrarVenta = document.getElementById("formRegistrarVenta");

    formRegistrarVenta.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevenir el comportamiento por defecto del formulario

        const codigo = document.getElementById("codigo").value;
        const cantidad = document.getElementById("cantidad").value;

        // Validar que los campos no estén vacíos
        if (!codigo || !cantidad) {
            alert("Por favor, complete todos los campos.");
            return;
        }

        // Crear el objeto con los datos a enviar
        const datosVenta = {
            codigo: codigo,
            cantidad: parseInt(cantidad, 10) // Asegurarse de que la cantidad sea un número entero
        };

        // Enviar la solicitud POST al servidor
        fetch("/api/registrar_venta_carro", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(datosVenta)
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                // Si la venta fue registrada correctamente
                alert(data.mensaje);
                // Limpiar el formulario después de registrar la venta
                formRegistrarVenta.reset();
            } else if (data.error) {
                // Si hubo un error
                alert(`Error: ${data.error}`);
            }
        })
        .catch(error => {
            // Manejar errores de red
            alert("Hubo un problema con la solicitud: " + error);
        });
    });
});