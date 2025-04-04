document.addEventListener("DOMContentLoaded", function () {
    const contenedorVentas = document.getElementById("contenedorVentas");
    const filtroTiempo = document.getElementById("filtroTiempo");
    const btnEliminar = document.getElementById("btnEliminar");
    
    let inventarioMayor = {};

    // Cargar inventario mayor antes de mostrar ventas
    function cargarInventarioMayor() {
        return fetch("/api/inventario_mayor")
            .then(response => response.json())
            .then(data => {
                inventarioMayor = {};
                data.forEach(producto => {
                    inventarioMayor[producto.id] = {
                        codigo: producto.codigo,
                        categoria: producto.categoria
                    };
                });
            })
            .catch(error => console.error("Error cargando inventario mayor:", error));
    }

    function cargarVentas(filtroDias = "todas") {
        fetch("/api/notificaciones_venta")
            .then(response => response.json())
            .then(ventas => {
                contenedorVentas.innerHTML = ""; // Limpiar antes de insertar datos
                let ventasPorDia = {};

                const fechaLimite = filtroDias !== "todas" ? new Date(Date.now() - filtroDias * 24 * 60 * 60 * 1000) : null;

                ventas.forEach(venta => {
                    const fechaVenta = new Date(venta.fecha.split("/").reverse().join("-"));

                    if (!fechaLimite || fechaVenta >= fechaLimite) {
                        let fecha = venta.fecha;
                        if (!ventasPorDia[fecha]) {
                            ventasPorDia[fecha] = {
                                dia: venta.dia,
                                ventas: [],
                                totalGeneral: 0
                            };
                        }
                        const valorFinal = venta.cantidad * (venta.precio || 0);
                        ventasPorDia[fecha].ventas.push({
                            ...venta,
                            valorFinal
                        });
                        ventasPorDia[fecha].totalGeneral += valorFinal;
                    }
                });

                Object.keys(ventasPorDia).forEach(fecha => {
                    let data = ventasPorDia[fecha];

                    let tablaHTML = `
                        <h2>${data.dia} - ${fecha}</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Hora</th>
                                    <th>Código</th>
                                    <th>Nombre del Producto</th>
                                    <th>Categoría</th>
                                    <th>Cantidad (Unidades)</th>
                                    <th>Precio</th>
                                    <th>Valor Final (Q)</th>
                                </tr>
                            </thead>
                            <tbody>`;

                    data.ventas.forEach(venta => {
                        const productoInfo = inventarioMayor[venta.id_producto] || {};
                        const codigoActualizado = productoInfo.codigo || venta.codigo || "Sin código";
                        const categoriaActualizada = productoInfo.categoria || venta.categoria || "Sin categoría";

                        tablaHTML += `
                            <tr>
                                <td>${venta.hora || "Sin hora"}</td>
                                <td>${codigoActualizado}</td>
                                <td>${venta.producto || "Sin nombre"}</td>
                                <td>${categoriaActualizada}</td>
                                <td>${venta.cantidad}</td>
                                <td>Q${(venta.precio || 0).toFixed(2)}</td>
                                <td>Q${venta.valorFinal.toFixed(2)}</td>
                            </tr>`;
                    });

                    tablaHTML += `
                            </tbody>
                            <tfoot>
                                <tr>
                                    <td colspan="6" style="text-align: right;"><strong>Total General:</strong></td>
                                    <td><strong>Q${data.totalGeneral.toFixed(2)}</strong></td>
                                </tr>
                            </tfoot>
                        </table>
                        <hr>`;

                    contenedorVentas.innerHTML += tablaHTML;
                });
            })
            .catch(error => console.error("Error cargando ventas:", error));
    }

    document.getElementById("btnRegresarPanel").addEventListener("click", function () {
        window.location.href = "/regresar_panel";
    });

    document.getElementById("btnCerrarSesion").addEventListener("click", function () {
        fetch("/logout", { method: "GET" })
            .then(response => {
                if (response.redirected) {
                    window.location.href = response.url;
                }
            })
            .catch(error => console.error("Error al cerrar sesión:", error));
    });

    filtroTiempo.addEventListener("change", function () {
        cargarVentas(this.value);
    });

    btnEliminar.addEventListener("click", function () {
        const filtroSeleccionado = filtroTiempo.value;
        fetch("/api/notificaciones/eliminar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ tipo: "venta", dias: filtroSeleccionado })
        })
            .then(response => response.json())
            .then(resultado => {
                alert(resultado.mensaje);
                cargarVentas(filtroSeleccionado);
            })
            .catch(error => console.error("Error eliminando ventas:", error));
    });

    // Cargar todo al inicio
    cargarInventarioMayor().then(() => cargarVentas());
});