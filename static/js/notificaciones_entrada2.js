document.addEventListener("DOMContentLoaded", function () {
    const tablaEntradas = document.getElementById("tablaEntradas");
    const filtroTiempo = document.getElementById("filtroTiempo");
    const btnEliminar = document.getElementById("btnEliminar");
    const totalGeneralElement = document.getElementById("totalGeneral");

    // Función para regresar al panel según el rol
    document.getElementById("btnRegresarPanel").addEventListener("click", function () {
        window.location.href = "/regresar_panel"; // Ahora Flask se encarga de la redirección
        });

    let inventarioMayor = {};

    // Función para cargar el inventario mayor y obtener códigos, categorías y precios actualizados.
    function cargarInventarioMayor() {
        return fetch("/api/inventario_mayor")
            .then(response => response.json())
            .then(data => {
                inventarioMayor = {};
                data.forEach(producto => {
                    // Usamos el nombre del producto como clave (ajusta si usas otro identificador)
                    inventarioMayor[producto.nombre] = {
                        codigo: producto.codigo,
                        categoria: producto.categoria,
                        precio: producto.costo  // Suponiendo que "costo" es el precio unitario
                    };
                });
            })
            .catch(error => console.error("Error cargando inventario mayor:", error));
    }

    // Función para cargar las entradas desde la API del Vendedor 2
    function cargarEntradas(filtroDias = "todas") {
        fetch("/api/notificaciones_entrada2")  // API para las notificaciones del Vendedor 2
            .then(response => response.json())
            .then(data => {
                tablaEntradas.innerHTML = ""; // Limpiar la tabla
                let totalGeneral = 0; // Acumular el total de las entradas

                // Definir la fecha límite para el filtro
                const fechaLimite = filtroDias !== "todas" 
                    ? new Date(Date.now() - filtroDias * 24 * 60 * 60 * 1000)
                    : null;

                data.forEach(entrada => {
                    // Convertir la fecha (suponiendo formato "dd/mm/yyyy")
                    let fechaConvertida;
                    if (entrada.fecha) {
                        const [dia, mes, anio] = entrada.fecha.split("/");
                        fechaConvertida = new Date(`${anio}-${mes}-${dia}`);
                    } else {
                        fechaConvertida = "Fecha inválida";
                    }

                    // Filtrar según la fecha si es necesario
                    if (!fechaLimite || (fechaConvertida !== "Fecha inválida" && fechaConvertida >= fechaLimite)) {
                        // Obtener precio: usamos entrada.precio convertido a número, o si falta, el del inventario mayor
                        const precioEntrada = parseFloat(entrada.precio);
                        const productoInfo = inventarioMayor[entrada.producto] || {};
                        const precio = !isNaN(precioEntrada) && precioEntrada > 0 
                                        ? precioEntrada 
                                        : (parseFloat(productoInfo.precio) || 0);
                        const valorFinal = entrada.cantidad * precio;
                        totalGeneral += valorFinal;

                        // Obtener código y categoría actualizados
                        const codigoActualizado = productoInfo.codigo || entrada.codigo || "Sin código";
                        const categoriaActualizada = productoInfo.categoria || entrada.categoria || "Sin categoría";

                        const fila = document.createElement("tr");
                        fila.innerHTML = ` 
                            <td>${entrada.dia || "Sin día"}</td>
                            <td>${entrada.fecha || "Sin fecha"}</td>
                            <td>${entrada.hora || "Sin hora"}</td>
                            <td>${codigoActualizado}</td>
                            <td>${entrada.producto || "Sin nombre"}</td>
                            <td>${categoriaActualizada}</td>
                            <td>${entrada.cantidad || 0}</td>
                            <td>Q${precio.toFixed(2)}</td>
                            <td>Q${valorFinal.toFixed(2)}</td>
                        `;
                        tablaEntradas.appendChild(fila);
                    }
                });

                // Actualizar el total general en el pie de la tabla
                totalGeneralElement.textContent = `Q${totalGeneral.toFixed(2)}`;
            })
            .catch(error => console.error("Error cargando entradas:", error));
    }

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

    // Cargar primero el inventario mayor y luego las entradas
    cargarInventarioMayor().then(() => cargarEntradas());

    // Evento para filtrar entradas por tiempo
    filtroTiempo.addEventListener("change", function () {
        cargarEntradas(this.value);
    });

    // Evento para eliminar las entradas filtradas
    btnEliminar.addEventListener("click", function () {
        const filtroSeleccionado = filtroTiempo.value;
        fetch("/api/notificaciones/eliminar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tipo: "entrada", dias: filtroSeleccionado })
        })
        .then(response => response.json())
        .then(resultado => {
            alert(resultado.mensaje);
            cargarEntradas(filtroSeleccionado);
        })
        .catch(error => console.error("Error eliminando entradas:", error));
    });
});