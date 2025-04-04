document.addEventListener("DOMContentLoaded", function () {
    console.log("🚚 Inventario Carro cargado");

    // Rol del usuario inyectado en el template, con valor por defecto "vendedor"
    const usuarioRol = window.usuarioRol || "vendedor";

    // Función para regresar al panel según el rol
    document.getElementById("btnRegresarPanel").addEventListener("click", function () {
    window.location.href = "/regresar_panel"; // Ahora Flask se encarga de la redirección
    });

    // Elementos de la interfaz
    const tablaInventario = document.getElementById("tablaInventarioCarro");
    const filtroBusqueda = document.getElementById("filtroBusqueda");
    const filtroCategoria = document.getElementById("filtroCategoria");
    const ordenarCantidad = document.getElementById("ordenarCantidad");
    const ordenarCosto = document.getElementById("ordenarCosto");

    // Botones para operaciones
    const btnRegistrarVenta = document.getElementById("btnRegistrarVenta");
    const btnRegistrarEntrada = document.getElementById("btnRegistrarEntrada"); // Debe existir en el HTML
    const btnAgregarProducto = document.getElementById("btnAgregarProducto"); // Solo para admin y supervisor

    // Configurar la interfaz según el rol del usuario
    function configurarInterfaz() {
        if (usuarioRol === "vendedor") {
            if (btnAgregarProducto) btnAgregarProducto.style.display = "none";
        } else if (usuarioRol === "admin" || usuarioRol === "supervisor") {
            if (btnAgregarProducto) btnAgregarProducto.style.display = "block";
        }
    }
    configurarInterfaz();
    
    // Función para cargar productos desde la API del inventario del carro
    function cargarProductos() {
        let url = "/api/inventario_carro?";
        const buscar = filtroBusqueda.value.trim();
        const categoria = filtroCategoria.value;
        const ordenar = ordenarCantidad.dataset.ordenar || ordenarCosto.dataset.ordenar || "";
        
        if (buscar) url += `buscar=${encodeURIComponent(buscar)}&`;
        if (categoria) url += `categoria=${encodeURIComponent(categoria)}&`;
        if (ordenar) url += `ordenar=${encodeURIComponent(ordenar)}&`;
        
        fetch(url)
        .then(response => {
            if (!response.ok) throw new Error("❌ No se pudo cargar el inventario.");
            return response.json();
        })
        .then(productos => {
            tablaInventario.innerHTML = ""; // Limpiar tabla
            let totalGeneral = 0; // Acumulador para el total general
             
            productos.forEach((producto) => {
                // Asegurarse de que la cantidad y el precio sean números válidos
                const cantidad = Number(producto.cantidad);
                const precio = Number(producto.precio);

                // Si la cantidad o el precio no son números válidos, continuar con el siguiente producto
                if (isNaN(cantidad) || isNaN(precio)) {
                    console.error("❌ Datos inválidos en el producto: ", producto);
                    return; // Salir de esta iteración si los datos no son válidos
                }

                // Cálculo del valor final
                const valorFinal = cantidad * precio;
                totalGeneral += valorFinal; // Acumular el valor final al total general

                // Para admin y supervisor se muestran botones de editar y eliminar
                let acciones = "";
                if (usuarioRol === "admin" || usuarioRol === "supervisor") {
                    acciones = `
                    <button class="btn btn-warning btn-sm editar-btn" data-codigo="${producto.codigo}">✏️ Editar</button>
                    <button class="btn btn-danger btn-sm eliminar-btn" data-codigo="${producto.codigo}">❌ Eliminar</button>
                    `;
                }

                // Crear fila en la tabla para cada producto
                const row = document.createElement("tr");
                row.innerHTML = `
                <td>${producto.codigo}</td>
                <td>${producto.nombre}</td>
                <td>${producto.categoria}</td>
                <td>${cantidad.toLocaleString("en-US")}</td>
                <td>Q${precio.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
                <td>Q${valorFinal.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td> <!-- Valor Final -->
                ${ (usuarioRol === "admin" || usuarioRol === "supervisor") ? `<td>${acciones}</td>` : "" }
                `;
                tablaInventario.appendChild(row);
            });

            // Actualizar el Total General en el pie de la tabla
            const totalGeneralElement = document.getElementById('totalGeneralCarro');
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

    // Eventos para filtros y ordenación
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

    // Función para editar un producto (solo para admin/supervisor)
    function editarProducto(codigo) {
        // Obtener los productos desde la API
        fetch("/api/inventario_carro")
            .then(response => response.json())
            .then(productos => {
                const producto = productos.find(p => p.codigo === codigo);
                if (!producto) {
                    alert("⚠️ Producto no encontrado.");
                    return;
                }
    
                // Mostrar los valores actuales en los campos del prompt
                const nuevoNombre = prompt("📝 Editar Nombre:", producto.nombre);
                const nuevaCategoria = prompt("📂 Editar Categoría:", producto.categoria);
                const nuevaCantidad = prompt("📦 Editar Cantidad (Unidades):", producto.cantidad);
                const nuevoPrecio = prompt("💰 Editar Precio:", producto.precio);
    
                // Si el usuario cancela alguna de las ediciones, no hacer nada
                if (nuevoNombre === null || nuevaCategoria === null || nuevaCantidad === null || nuevoPrecio === null) {
                    alert("⚠️ Edición cancelada.");
                    return;
                }
    
                // Enviar los datos actualizados a la API
                const data = {
                    codigo: codigo,
                    nombre: nuevoNombre,
                    categoria: nuevaCategoria,
                    cantidad: Number(nuevaCantidad),
                    precio: Number(nuevoPrecio)
                };
    
                fetch("/api/editar_producto_carro", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(data)
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.mensaje) {
                            alert("✅ " + data.mensaje); // Muestra el mensaje de éxito
                        } else if (data.error) {
                            alert("❌ " + data.error); // Muestra el error
                        }
                        cargarProductos(); // Recarga los productos después de la edición
                    })
                    .catch(error => {
                        console.error("❌ Error al editar producto:", error);
                        alert("⚠️ Algo salió mal al editar el producto.");
                    });
            })
            .catch(error => {
                console.error("❌ Error al obtener productos:", error);
                alert("⚠️ No se pudo obtener el producto para editar.");
            });
    }    

    // Función para eliminar un producto (solo para admin/supervisor)
    function eliminarProducto(codigo) {
        // Confirmación antes de proceder con la eliminación
        if (!confirm("⚠️ ¿Estás seguro de que deseas eliminar este producto?")) return;
    
        const data = { codigo: codigo };
    
        fetch("/api/eliminar_producto_carro", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        })
        .then(response => response.json()) // Convierte la respuesta a JSON
        .then(data => {
            if (data.mensaje) {  // Asegúrate de que el mensaje esté presente en la respuesta
                alert("✅ " + data.mensaje); // Muestra el mensaje de éxito
            } else if (data.error) {
                alert("❌ " + data.error); // Muestra el error
            } else {
                alert("⚠️ Respuesta inesperada: " + JSON.stringify(data)); // Si no hay mensaje ni error
            }
            cargarProductos(); // Recarga los productos después de la eliminación
        })
        .catch(error => {
            console.error("❌ Error al eliminar producto:", error);
            alert("⚠️ Algo salió mal al eliminar el producto.");
        });        
    }    

    // Evento para redirigir a la página de agregar producto (solo admin/supervisor)
    if (btnAgregarProducto) {
        btnAgregarProducto.addEventListener("click", function () {
            window.location.href = "/agregar_producto_carro";
        });
    }

    // Lógica para registrar una venta (para todos los roles: admin, supervisor, vendedor)
    if (btnRegistrarVenta) {
        btnRegistrarVenta.addEventListener("click", function () {
            const codigo = prompt("Ingrese el código del producto vendido:");
            const cantidadVendida = prompt("Ingrese la cantidad vendida:");
            if (!codigo || !cantidadVendida) {
                alert("⚠️ Información incompleta.");
                return;
            }
            fetch("/api/registrar_venta_carro", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    codigo: codigo,
                    cantidad: Number(cantidadVendida)
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert("⚠️ " + data.error);
                } else {
                    alert("✅ " + data.mensaje);
                    cargarProductos();
                }
            })
            .catch(error => console.error("❌ Error al registrar venta:", error));
        });
    }

    // Lógica para registrar una entrada (permitido para admin/supervisor y vendedor)
    if (btnRegistrarEntrada) {
        btnRegistrarEntrada.addEventListener("click", function () {
            const codigo = prompt("Ingrese el código del producto para registrar entrada:");
            const cantidadEntrada = prompt("Ingrese la cantidad a registrar:");
            if (!codigo || !cantidadEntrada) {
                alert("⚠️ Información incompleta.");
                return;
            }
            fetch("/api/registrar_entrada_carro", {
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
                    cargarProductos();
                }
            })
            .catch(error => console.error("❌ Error al registrar entrada:", error));
        });
    }

    // Delegación de eventos para los botones de editar y eliminar en la tabla
    tablaInventario.addEventListener("click", function (event) {
        const codigo = event.target.getAttribute("data-codigo");
        if (event.target.classList.contains("editar-btn")) {
            editarProducto(codigo);
        }
        if (event.target.classList.contains("eliminar-btn")) {
            eliminarProducto(codigo);
        }
    });

    // Cargar productos al inicio
    cargarProductos();
});