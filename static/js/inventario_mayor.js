document.addEventListener("DOMContentLoaded", function () {
    console.log("📦 Inventario Mayor cargado");

    const tablaInventario = document.getElementById("tablaInventario");
    const filtroBusqueda = document.getElementById("filtroBusqueda");
    const filtroCategoria = document.getElementById("filtroCategoria");
    const ordenarCantidad = document.getElementById("ordenarCantidad");
    const ordenarCosto = document.getElementById("ordenarCosto");

    // Función para regresar al panel según el rol
    document.getElementById("btnRegresarPanel").addEventListener("click", function () {
        window.location.href = "/regresar_panel"; // Ahora Flask se encarga de la redirección
    });

    // 🔹 Función para cargar productos con filtros y ordenamientos
    function cargarProductos() {
        let url = "/api/inventario?";

        // Obtener valores de los filtros
        const buscar = filtroBusqueda.value.trim();
        const categoria = filtroCategoria.value;
        const ordenar = ordenarCantidad.dataset.ordenar || ordenarCosto.dataset.ordenar || "";

        // Agregar filtros a la URL
        if (buscar) url += `buscar=${encodeURIComponent(buscar)}&`;
        if (categoria) url += `categoria=${encodeURIComponent(categoria)}&`;
        if (ordenar) url += `ordenar=${encodeURIComponent(ordenar)}&`;

        // Función para cargar el inventario mayor y agregar el cálculo del valor final
        fetch(url)
        .then(response => {
            if (!response.ok) throw new Error("❌ No se pudo cargar el inventario.");
            return response.json();
        })
        .then(productos => {
            tablaInventario.innerHTML = ""; // Limpiar tabla
            let totalGeneral = 0; // Acumulador para el total general
             
            productos.forEach((producto) => {
                // Cálculo del valor final
                const valorFinal = Number(producto.cantidad) * Number(producto.costo);
                totalGeneral += valorFinal; // Acumular el valor final al total general
                // Crear fila en la tabla para cada producto
                const row = document.createElement("tr");
                row.innerHTML = `
                <td>${producto.codigo}</td>
                <td>${producto.nombre}</td>
                <td>${producto.categoria}</td>
                <td>${producto.cantidad.toLocaleString("en-US")}</td>
                <td>Q${Number(producto.costo).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td>Q${valorFinal.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td> <!-- Valor Final -->
                <td>
                <button class="btn btn-warning btn-sm editar-btn" data-codigo="${producto.codigo}">✏️ Editar</button>
                <button class="btn btn-danger btn-sm eliminar-btn" data-codigo="${producto.codigo}">❌ Eliminar</button>
                </td>
                `;
                tablaInventario.appendChild(row);
            });
            
            // Actualizar el Total General en el pie de la tabla (esto es similar a lo que tienes para las entradas)
            const totalGeneralElement = document.getElementById('totalGeneralInventario'); // Asegúrate de tener este elemento en tu HTML
            totalGeneralElement.textContent = `Q${totalGeneral.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        })
        
        .catch(error => console.error("❌ Error al cargar productos:", error));
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

    // 🔹 Eventos para activar los filtros y ordenaciones
    filtroBusqueda.addEventListener("input", cargarProductos);
    filtroCategoria.addEventListener("change", cargarProductos);
    
    ordenarCantidad.addEventListener("click", function () {
        ordenarCantidad.dataset.ordenar = "cantidad";
        ordenarCosto.dataset.ordenar = "";
        cargarProductos();
    });
    
        ordenarCosto.addEventListener("click", function () {
        ordenarCosto.dataset.ordenar = "costo";
        ordenarCantidad.dataset.ordenar = "";
        cargarProductos();
    });

    // 🔹 Función para editar un producto
    window.editarProducto = function (codigo) {
        fetch("/api/inventario")
            .then(response => response.json())
            .then(productos => {
                const producto = productos.find(p => p.codigo === codigo);
                if (!producto) {
                    alert("⚠️ Producto no encontrado.");
                    return;
                }

                // Capturar nuevos valores
                const nuevoNombre = prompt("📝 Editar Nombre:", producto.nombre);
                const nuevaCategoria = prompt("📂 Editar Categoría:", producto.categoria);
                const nuevaCantidad = prompt("📦 Editar Cantidad (Unidades):", producto.cantidad);
                const nuevoCosto = prompt("💰 Editar Costo:", producto.costo);

                // Verificar si el usuario canceló el prompt
                if (nuevoNombre === null || nuevaCategoria === null || nuevaCantidad === null || nuevoCosto === null) {
                    alert("⚠️ Edición cancelada.");
                    return;
                }

                // Enviar los cambios al servidor
                fetch("/api/editar_producto", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        codigo: codigo,
                        nombre: nuevoNombre,
                        categoria: nuevaCategoria,
                        cantidad: Number(nuevaCantidad),
                        costo: Number(nuevoCosto)
                    })
                })
                .then(response => response.json())
                .then(data => {
                    alert("✅ " + data.mensaje);
                    cargarProductos(); // Recargar la tabla con los cambios
                })
                .catch(error => console.error("❌ Error al editar producto:", error));
            });
    };

    // 🔹 Función para eliminar un producto
    window.eliminarProducto = function (codigo) {
        if (!confirm("⚠️ ¿Estás seguro de que deseas eliminar este producto?")) {
            return;
        }

        fetch("/api/eliminar_producto", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ codigo: codigo })
        })
        .then(response => response.json())
        .then(data => {
            alert("✅ " + data.mensaje);
            cargarProductos(); // Recargar la tabla después de eliminar
        })
        .catch(error => console.error("❌ Error al eliminar producto:", error));
    };

    // 🔹 Evento para capturar clicks en la tabla (Delegación de eventos)
    tablaInventario.addEventListener("click", function (event) {
        const codigo = event.target.getAttribute("data-codigo");

        if (event.target.classList.contains("editar-btn")) {
            editarProducto(codigo);
        }

        if (event.target.classList.contains("eliminar-btn")) {
            eliminarProducto(codigo);
        }
    });

    // 🔹 Función para agregar un producto (llamada desde agregar_producto.js)
    window.agregarProducto = function (codigo, nombre, categoria, cantidad, costo) {
        fetch("/api/agregar_producto", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                codigo: codigo,
                nombre: nombre,
                categoria: categoria,
                cantidad: Number(cantidad),
                costo: Number(costo)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("⚠️ " + data.error);
            } else {
                alert("✅" + data.mensaje);
                window.location.href = "/inventario_mayor"; // Volver al inventario
            }
        })
        .catch(error => console.error("❌ Error al agregar producto:", error));
    };

    // 🔹 Redirigir a la página de agregar producto
    btnAgregar.addEventListener("click", function () {
        console.log("✅ Botón 'Agregar Producto' clickeado");
        window.location.href = "/agregar_producto";
    });

    // Registrar una entrada en el inventario mayor (solo admin/supervisor)
if (btnRegistrarEntrada) {
    btnRegistrarEntrada.addEventListener("click", function () {
        const codigo = prompt("Ingrese el código del producto para registrar entrada:");
        const cantidadEntrada = prompt("Ingrese la cantidad a registrar:");

        if (!codigo || !cantidadEntrada) {
            alert("⚠️ Información incompleta.");
            return;
        }

        fetch("/api/registrar_entrada", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                codigo: codigo,
                cantidad: Number(cantidadEntrada)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert("⚠️ " + data.error);
            } else {
                alert("✅ " + data.mensaje);
                cargarProductos(); // Actualiza la tabla del Inventario Mayor
            }
        })
        .catch(error => console.error("❌ Error al registrar entrada:", error));
    });
}

    // 🔹 Cargar productos al inicio
    cargarProductos();
});