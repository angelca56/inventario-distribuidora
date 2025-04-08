from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash  # 🔐 Para encriptar contraseñas
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
import os


# 📌 Ruta del archivo JSON inventario mayor
INVENTARIO_FILE = os.path.join("json", "inventario_mayor.json")

# 📌 Ruta del archivo JSON para el Inventario del Carro
INVENTARIO_CARRO_FILE = os.path.join("json", "inventario_carro1.json")

# 📌 Ruta del archivo JSON para el Inventario del Carro 2
INVENTARIO_CARRO2_FILE = os.path.join("json", "inventario_carro2.json")

# 📌 Ruta del archivo JSON para registrar entradas del vendedor
RETIROS_VENDEDOR_FILE = os.path.join("json", "retiros_vendedor.json")

# 📌 Ruta del archivo JSON para registrar ventas del vendedor
VENTAS_VENDEDOR_FILE = os.path.join("json", "ventas_vendedor.json")

# 📌 Ruta del archivo JSON para registrar entradas del vendedor 2
RETIROS_VENDEDOR2_FILE = os.path.join("json", "retiros_vendedor2.json")

# 📌 Ruta del archivo JSON para registrar ventas del vendedor 2
VENTAS_VENDEDOR2_FILE = os.path.join("json", "ventas_vendedor2.json")

# 📌 Diccionario de usuarios (correo → { contraseña encriptada, rol })
usuarios = {
    "gtra@gmail.com": {
        "contraseña": generate_password_hash("gtradmon"),  # 🔐 Contraseña encriptada
        "rol": "admin"
    },
    "gtrs@gmail.com": {
        "contraseña": generate_password_hash("gtr"),
        "rol": "supervisor"
    },
    "gtr@gmail.com": {
        "contraseña": generate_password_hash("gtrven"),
        "rol": "vendedor"
    },
    "gtr2@gmail.com": {
        "contraseña": generate_password_hash("gtrven2"),
        "rol": "vendedor2"
    },
    "gtrpedidos@gmail.com": {
    "contraseña": generate_password_hash("gtrpedido"),
    "rol": "pedido"
    }
}

# Función para cargar el inventario mayor desde el JSON
def cargar_inventario():
    if not os.path.exists(INVENTARIO_FILE):  # Si no existe, crea un JSON vacío
        with open(INVENTARIO_FILE, "w") as f:
            json.dump([], f)

    with open(INVENTARIO_FILE, "r") as f:
        return json.load(f)  # Retorna la lista de productos

# Función para guardar productos en el JSON
def guardar_inventario(productos):
    with open(INVENTARIO_FILE, "w") as f:
        json.dump(productos, f, indent=4)

# Función para cargar el inventario del carro desde el JSON
def cargar_inventario_carro():
    # Asegurarnos de que la carpeta 'json' exista
    if not os.path.exists("json"):
        os.makedirs("json")  # Si no existe, la creamos

    # Si el archivo no existe, lo creamos vacío
    if not os.path.exists(INVENTARIO_CARRO_FILE):
        with open(INVENTARIO_CARRO_FILE, "w") as f:
            json.dump([], f)  # Creamos el archivo vacío con una lista vacía

    # Cargamos el inventario desde el archivo
    with open(INVENTARIO_CARRO_FILE, "r") as f:
        return json.load(f)

# Función para guardar productos en el inventario del carro en el JSON
def guardar_inventario_carro(productos):
    with open(INVENTARIO_CARRO_FILE, "w") as f:
        json.dump(productos, f, indent=4)

# Función para cargar el inventario del carro 2 desde el JSON
def cargar_inventario_carro2():
    # Asegurarnos de que la carpeta 'json' exista
    if not os.path.exists("json"):
        os.makedirs("json")  # Si no existe, la creamos

    # Si el archivo no existe, lo creamos vacío
    if not os.path.exists(INVENTARIO_CARRO2_FILE):
        with open(INVENTARIO_CARRO2_FILE, "w") as f:
            json.dump([], f)  # Creamos el archivo vacío con una lista vacía

    # Cargamos el inventario desde el archivo
    with open(INVENTARIO_CARRO2_FILE, "r") as f:
        return json.load(f)

# Función para guardar productos en el inventario del carro 2 en el JSON
def guardar_inventario_carro2(productos):
    with open(INVENTARIO_CARRO2_FILE, "w") as f:
        json.dump(productos, f, indent=4)
    
# Función para cargar entradas echas del vendedor desde el JSON
def cargar_retiros_vendedor():
    if not os.path.exists(RETIROS_VENDEDOR_FILE):
        with open(RETIROS_VENDEDOR_FILE, "w") as f:
            json.dump([], f)

    with open(RETIROS_VENDEDOR_FILE, "r") as f:
        return json.load(f)

# Función para guardar entradas echas por el vendedor en el JSON
def guardar_retiros_vendedor(retiros):
    with open(RETIROS_VENDEDOR_FILE, "w") as f:
        json.dump(retiros, f, indent=4)

# Función para cargar ventas del vendedor desde el JSON
def cargar_ventas_vendedor():
    if not os.path.exists(VENTAS_VENDEDOR_FILE):
        with open(VENTAS_VENDEDOR_FILE, "w") as f:
            json.dump([], f)

    with open(VENTAS_VENDEDOR_FILE, "r") as f:
        return json.load(f)

# Función para guardar ventas en el JSON
def guardar_ventas_vendedor(ventas):
    with open(VENTAS_VENDEDOR_FILE, "w") as f:
        json.dump(ventas, f, indent=4)

# Función para cargar las entradas hechas por el Vendedor 2 desde el JSON
def cargar_retiros_vendedor2():
    # Asegurarnos de que la carpeta 'json' exista
    if not os.path.exists("json"):
        os.makedirs("json")  # Si no existe, la creamos

    # Si el archivo no existe, lo creamos vacío
    if not os.path.exists(RETIROS_VENDEDOR2_FILE):
        with open(RETIROS_VENDEDOR2_FILE, "w") as f:
            json.dump([], f)  # Creamos el archivo vacío con una lista vacía

    # Cargamos las entradas desde el archivo
    with open(RETIROS_VENDEDOR2_FILE, "r") as f:
        return json.load(f)

# Función para guardar entradas hechas por el Vendedor 2 en el JSON
def guardar_retiros_vendedor2(retiros):
    with open(RETIROS_VENDEDOR2_FILE, "w") as f:
        json.dump(retiros, f, indent=4)

# Función para cargar las ventas del Vendedor 2 desde el JSON
def cargar_ventas_vendedor2():
    # Asegurarnos de que la carpeta 'json' exista
    if not os.path.exists("json"):
        os.makedirs("json")  # Si no existe, la creamos

    # Si el archivo no existe, lo creamos vacío
    if not os.path.exists(VENTAS_VENDEDOR2_FILE):
        with open(VENTAS_VENDEDOR2_FILE, "w") as f:
            json.dump([], f)  # Creamos el archivo vacío con una lista vacía

    # Cargamos las ventas desde el archivo
    with open(VENTAS_VENDEDOR2_FILE, "r") as f:
        return json.load(f)

# Función para guardar ventas del Vendedor 2 en el JSON
def guardar_ventas_vendedor2(ventas):
    with open(VENTAS_VENDEDOR2_FILE, "w") as f:
        json.dump(ventas, f, indent=4)

load_dotenv()

def crear_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY", "clave_super_secreta")

    # 📌 Ruta para mostrar la página de inicio de sesión
    @app.route("/")
    def login():
        return render_template("login.html")  # Página de inicio de sesión
    
    # 📌 Ruta para manejar el inicio de sesión
    @app.route("/login", methods=["POST"])
    def autenticar():
        data = request.json
        correo = data.get("correo")
        contraseña = data.get("password")
        usuario = usuarios.get(correo)
        
        if not usuario or not check_password_hash(usuario["contraseña"], contraseña):
            return jsonify({"error": "Correo o contraseña incorrectos"}), 401
        
        session["usuario_id"] = correo
        session["usuario_rol"] = usuario["rol"]
        
        redireccion = {
            "admin": "/admin",
            "supervisor": "/supervisor",
            "vendedor": "/vendedor",
            "vendedor2": "/vendedor2",
            "pedido": "/pedido"
            }.get(usuario["rol"], "/")
        
        return jsonify({"mensaje": "Inicio de sesión exitoso", "redirect": redireccion})
    
    # 📌 Ruta para el apartado del admin
    @app.route("/admin")
    def admin():
        if "usuario_id" not in session or session.get("usuario_rol") != "admin":
            return redirect(url_for("login"))  # 🔄 Si no es admin, redirigir al login
        
        return render_template("apartado_admin.html")  #Página del admin
    
    # 📌 Ruta para el apartado del supervisor
    @app.route("/supervisor")
    def supervisor():
        if "usuario_id" not in session or session.get("usuario_rol") != "supervisor":
            return redirect(url_for("login"))  # 🔄 Si no es supervisor, redirigir al login
        
        return render_template("apartado_supervisor.html")  #Página del supervisor
    
    # 📌 Ruta para el apartado del vendedor
    @app.route("/vendedor")
    def vendedor():
        if "usuario_id" not in session or session.get("usuario_rol") != "vendedor":
            return redirect(url_for("login"))  # 🔄 Si no es vendedor1, redirigir al login
        
        return render_template("apartado_vendedor.html")  #Página del vendedor
    
    # 📌 Ruta para el apartado del vendedor2
    @app.route("/vendedor2")
    def vendedor2():
        if "usuario_id" not in session or session.get("usuario_rol") != "vendedor2":
            return redirect(url_for("login"))  # 🔄 Si no es vendedor2, redirigir al login
        
        return render_template("apartado_vendedor2.html")  #Página del vendedor2
    
    # 📌 Ruta para regresar al panel del usuario
    @app.route("/regresar_panel")
    def regresar_panel():
        if "usuario_id" not in session:
            return redirect(url_for("login"))  # Si no hay sesión, manda al login
        
        rol = session.get("usuario_rol")  # Obtiene el rol del usuario
        if rol == "admin":
            return redirect(url_for("admin"))  # Redirige al panel del admin
        elif rol == "supervisor":
            return redirect(url_for("supervisor"))  # Redirige al panel del supervisor
        elif rol == "vendedor":
            return redirect(url_for("vendedor"))  # Redirige al panel del vendedor1
        elif rol == "vendedor2":
            return redirect(url_for("vendedor2")) # Redirige al panel del vendedor2
        elif rol == "pedido":
            return redirect(url_for("pedido")) # Redirige al panel del usuario del pedido
        else:
            return redirect(url_for("login"))  # Si algo falla, manda al login
        
    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        
        return response
    
    # 📌 Ruta para ver el Inventario Mayor (Solo Admin y Supervisor)
    @app.route("/inventario_mayor")
    def inventario_mayor():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))  # 🔒 Si no es Admin o Supervisor, lo manda al login
        productos = cargar_inventario()  # 📦 Cargar productos desde JSON
        
        return render_template("inventario_mayor.html", productos=json.dumps(productos))  # 🔥 Pasar productos como JSON
    
    # 📌 Ruta para obtener los productos en formato JSON con filtros y ordenaciones
    @app.route("/api/inventario", methods=["GET"])
    def obtener_inventario():
        productos = cargar_inventario()
        
        # 🔍 Obtener parámetros de filtrado desde la URL
        filtro_nombre_codigo = request.args.get("buscar", "").strip().lower()
        filtro_categoria = request.args.get("categoria", "").strip().lower()
        ordenar_por = request.args.get("ordenar", "").strip().lower()
        
        # 🔎 Filtrar por nombre o código
        if filtro_nombre_codigo:
            productos = [p for p in productos if filtro_nombre_codigo in p["nombre"].lower() or filtro_nombre_codigo in p["codigo"].lower()]
        # 📂 Filtrar por categoría
        if filtro_categoria:
            productos = [p for p in productos if p["categoria"].lower() == filtro_categoria]
            
        # 🔢 Ordenar por cantidad (mayor a menor)
        if ordenar_por == "cantidad":
            productos.sort(key=lambda p: int(p["cantidad"]), reverse=True)
            
        # 💰 Ordenar por costo (mayor a menor)
        elif ordenar_por == "costo":
            productos.sort(key=lambda p: float(p["costo"]), reverse=True)
            
        return jsonify(productos)
        
    # 📌 Ruta para agregar productos (Admin y Supervisor, solo JSON)
    @app.route("/api/agregar_producto", methods=["POST"])
    def api_agregar_producto():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return jsonify({"error": "⚠️ No autorizado"}), 403  # Error 403: No tienes permiso
        
        try:
            data = request.json or {}  # Evita errores si el cuerpo está vacío
            codigo = data.get("codigo", "").strip()
            nombre = data.get("nombre", "").strip()
            categoria = data.get("categoria", "").strip()
            cantidad = int(data.get("cantidad", 0))  # Asegurar número
            costo = float(data.get("costo", 0.0))  # Asegurar número
            
            # 📌 Validar datos
            if not codigo or not nombre or not categoria:
                return jsonify({"error": "⚠️ Todos los campos son obligatorios"}), 400
            
            productos = cargar_inventario()  # Cargar productos existentes
            
            # 📌 Verificar si el código ya existe
            if any(prod["codigo"] == codigo for prod in productos):
                return jsonify({"error": "⚠️ El código ya está registrado"}), 400
            
            # 📌 Agregar producto
            nuevo_producto = {
                "codigo": codigo,
                "nombre": nombre,
                "categoria": categoria,
                "cantidad": cantidad,
                "costo": costo
                }
            productos.append(nuevo_producto)
            guardar_inventario(productos)  # Guardar en JSON
            
            return jsonify({"mensaje": "✅ Producto agregado correctamente"}), 200
        except Exception as e:
            
            return jsonify({"error": f"❌ Error interno: {str(e)}"}), 500
        
    # 📌 Ruta para editar un producto
    @app.route("/api/editar_producto", methods=["POST"])
    def editar_producto():
        datos = request.json
        codigo = datos.get("codigo")
        if not codigo:
            return jsonify({"error": "Código del producto no proporcionado"}), 400
        
        productos = cargar_inventario()
        producto = next((p for p in productos if p["codigo"] == codigo), None)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Actualizar los valores si se enviaron
        producto["nombre"] = datos.get("nombre", producto["nombre"])
        producto["categoria"] = datos.get("categoria", producto["categoria"])
        producto["cantidad"] = int(datos.get("cantidad", producto["cantidad"]))
        producto["costo"] = float(datos.get("costo", producto["costo"]))
        guardar_inventario(productos)
        return jsonify({"mensaje": "Producto actualizado correctamente"}), 200
    
    # 📌 Ruta para eliminar un producto del inventario
    @app.route("/api/eliminar_producto", methods=["POST"])
    def eliminar_producto():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return jsonify({"error": "⚠️ No autorizado"}), 403  # Error 403: No tienes permiso
        try:
            data = request.json or {}
            codigo = data.get("codigo", "").strip()
            
            if not codigo:
                return jsonify({"error": "⚠️ Código de producto requerido"}), 400
            productos = cargar_inventario()
            
            # 📌 Filtrar productos para eliminar el que tenga el código enviado
            nuevos_productos = [p for p in productos if p["codigo"] != codigo]
            if len(nuevos_productos) == len(productos):
                return jsonify({"error": "⚠️ Producto no encontrado"}), 404
            guardar_inventario(nuevos_productos)  # Guardar cambios en JSON
            
            return jsonify({"mensaje": "✅ Producto eliminado correctamente"}), 200
        
        except Exception as e:
            return jsonify({"error": f"❌ Error interno: {str(e)}"}), 500
        
    # Ruta para registrar entradas de productos inventario mayor (Admin y Supervisor)
    @app.route("/api/registrar_entrada", methods=["POST"])
    def registrar_entrada():
        if "usuario_id" not in session:
            return jsonify({"error": "No tienes sesión activa."}), 403
        
        usuario_rol = session.get("usuario_rol")
        if usuario_rol not in ["admin", "supervisor"]:
            return jsonify({"error": "No tienes permiso para registrar entradas."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        cantidad = data.get("cantidad")
        
        if not codigo or not cantidad or cantidad <= 0:
            
            return jsonify({"error": "Datos de entrada inválidos."}), 400
        
        try:
            # Leer el Inventario Mayor
            with open(INVENTARIO_FILE, "r+") as f:
                productos_mayor = json.load(f)
                producto_mayor = next((p for p in productos_mayor if p["codigo"] == codigo), None)
                if producto_mayor:
                    # Aumentar la cantidad en el Inventario Mayor
                    producto_mayor["cantidad"] += cantidad
                else:
                    
                    return jsonify({"error": "Producto no encontrado en el inventario mayor."}), 40
                # Guardar cambios en el archivo JSON
                f.seek(0)
                f.truncate()
                json.dump(productos_mayor, f, indent=4)
                
                return jsonify({"mensaje": "Entrada registrada exitosamente en el Inventario Mayor."})
        except Exception as e:
            return jsonify({"error": f"Hubo un error: {e}"}), 500
        
    # 📌 Ruta para mostrar la página de agregar productos
    @app.route("/agregar_producto", methods=["GET"])
    def agregar_producto():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("agregar_producto.html")  # Solo muestra la 

    # 📌 Ruta para ver los inventarios de los carros
    @app.route("/ver_inventarios_carros")
    def ver_inventario_carros():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))  # 🔒 Si no está logueado, lo redirige al login
        return render_template("ver_inventarios_carros.html")  # Muestra la página con los inventarios de los carros
    
    # 📌 Ruta para Inventario del Carro (Acceso para Admin, Supervisor y Vendedor)
    @app.route("/inventario_carro")
    def inventario_carro():
        if "usuario_id" not in session:
            return redirect(url_for("login"))  # 🔒 Si no está logueado, lo redirige al login
        
        # Pasamos el rol del usuario para controlarlo en el frontend
        rol_usuario = session.get("usuario_rol")
        
        return render_template("inventario_carro.html", rol=rol_usuario)
    
    # 📌 Ruta para obtener los productos del Inventario del Carro con filtros y ordenación
    @app.route("/api/inventario_carro", methods=["GET"])
    def obtener_inventario_carro():
        if "usuario_id" not in session:
            return jsonify({"error": "No tienes sesión activa."}), 403
        
        try:
            # Cargar productos del inventario del carro desde el archivo JSON
            productos_carro = cargar_inventario_carro()
            
            # 🔍 Obtener parámetros de filtrado desde la URL
            filtro_nombre_codigo = request.args.get("buscar", "").strip().lower()
            filtro_categoria = request.args.get("categoria", "").strip().lower()
            ordenar_por = request.args.get("ordenar", "").strip().lower()

            # 🔎 Filtrar por nombre o código
            if filtro_nombre_codigo:
                productos_carro = [p for p in productos_carro if filtro_nombre_codigo in p["nombre"].lower() or filtro_nombre_codigo in p["codigo"].lower()]
                
            # 📂 Filtrar por categoría
            if filtro_categoria:
                productos_carro = [p for p in productos_carro if p["categoria"].lower() == filtro_categoria]
                
            # 🔢 Ordenar por cantidad (mayor a menor)
            if ordenar_por == "cantidad":
                productos_carro.sort(key=lambda p: int(p["cantidad"]), reverse=True)
                
            # 💰 Ordenar por precio (mayor a menor)
            elif ordenar_por == "costo":
                productos_carro.sort(key=lambda p: float(p["precio"]), reverse=True)
                
            return jsonify(productos_carro)  # Devuelve los productos en formato JSON
        except Exception as e:

            return jsonify({"error": f"Hubo un error: {e}"}), 500
        
    # 📌 Ruta para agregar un producto al Inventario del Carro (Admin y Supervisor)
    @app.route("/api/agregar_producto_carro", methods=["POST"])
    def api_agregar_producto_carro():
        if "usuario_id" not in session or session.get("usuario_rol") == "vendedor":
            return jsonify({"error": "No tienes permiso para agregar productos."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        nombre = data.get("nombre")
        categoria = data.get("categoria")
        cantidad = data.get("cantidad")
        precio = data.get("precio")
        
        if not codigo or not nombre or not categoria or not cantidad or not precio:
            
            return jsonify({"error": "Faltan datos del producto."}), 400
        
        try:
            # Leer el inventario actual
            with open(INVENTARIO_CARRO_FILE, "r+") as f:
                productos_carro = json.load(f)
                
                # Añadir el nuevo producto
                productos_carro.append({
                    "codigo": codigo,
                    "nombre": nombre,
                    "categoria": categoria,
                    "cantidad": cantidad,
                    "precio": precio
                    })
                f.seek(0)
                json.dump(productos_carro, f, indent=4)
                
                return jsonify({"mensaje": "Producto agregado al carro exitosamente."})
            
        except Exception as e:
            
            # Mostrar el error exacto para depuración
            print(f"Error al agregar el producto al carro: {e}")
            
            return jsonify({"error": f"Hubo un error: {e}"}), 500
        
    # 📌 Ruta para editar un producto en el inventario del Carro (Admin y Supervisor)
    @app.route("/api/editar_producto_carro", methods=["POST"])
    def editar_producto_carro():
        # Verificación de permisos
        if "usuario_id" not in session or session["usuario_rol"] not in ["admin", "supervisor"]:
            return jsonify({"error": "No tienes permisos para editar productos."}), 403
        
        # Cargar los datos recibidos en la petición
        datos = request.json
        codigo = datos.get("codigo")
        if not codigo:
            return jsonify({"error": "Código del producto no proporcionado"}), 400
        
        # Cargar el inventario del carro
        productos_carro = cargar_inventario_carro()
        
        # Buscar el producto
        producto = next((p for p in productos_carro if p["codigo"] == codigo), None)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404
        
        # Actualizar los campos del producto solo si se proporcionan nuevos valores
        producto["nombre"] = datos.get("nombre", producto["nombre"])
        producto["categoria"] = datos.get("categoria", producto["categoria"])
        
        # Validar y actualizar la cantidad, si se proporciona
        nueva_cantidad = datos.get("cantidad")
        if nueva_cantidad is not None:
            
            try:
                producto["cantidad"] = int(nueva_cantidad)
            except ValueError:
                
                return jsonify({"error": "Cantidad debe ser un número entero válido."}), 400
            
            # Validar y actualizar el precio, si se proporciona
            nuevo_precio = datos.get("precio")
            if nuevo_precio is not None:
                try:
                    producto["precio"] = float(nuevo_precio)
                except ValueError:
                    
                    return jsonify({"error": "Precio debe ser un número válido."}), 400
                
                # Guardar el inventario actualizado
                guardar_inventario_carro(productos_carro)
                
            # Devolver la respuesta con el producto actualizado
            return jsonify({
                "mensaje": "Producto actualizado correctamente",
                "producto_actualizado": producto
                }), 200
        
    # 📌 Ruta para eliminar un producto del Inventario del Carro (Admin y Supervisor)
    @app.route("/api/eliminar_producto_carro", methods=["POST"])
    def eliminar_producto_carro():
        if "usuario_id" not in session or session.get("usuario_rol") == "vendedor":
            return jsonify({"error": "No tienes permiso para eliminar productos."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        
        if not codigo:
            return jsonify({"error": "Falta el código del producto."}), 400
        
        try:
            # Cargar el inventario actual
            productos_carro = cargar_inventario_carro()
            
            # Verificar si el producto existe
            producto = next((p for p in productos_carro if p["codigo"] == codigo), None)
            if not producto:
                return jsonify({"error": "Producto no encontrado."}), 404
            
            # Filtrar productos para eliminar el seleccionado
            productos_carro = [p for p in productos_carro if p["codigo"] != codigo]
            
            # Guardar el inventario actualizado
            guardar_inventario_carro(productos_carro)
            
            return jsonify({"mensaje": "Producto eliminado exitosamente."}), 200
        
        except Exception as e:
            
            return jsonify({"error": f"Hubo un error: {e}"}), 500
    
    # 📌 Ruta para registrar una venta en el Inventario del Carro (Admin, Supervisor y vendedor)
    @app.route("/api/registrar_venta_carro", methods=["POST"])
    def registrar_venta_carro():
        # Verificar si el usuario está autenticado
        if "usuario_id" not in session:
            return jsonify({"error": "No estás autenticado."}), 403
        
        # Permitir que administradores, supervisores y vendedores registren ventas
        usuario_rol = session.get("usuario_rol")
        if usuario_rol not in ["vendedor", "admin", "supervisor"]:
            return jsonify({"error": "No tienes permiso para registrar ventas."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        cantidad = data.get("cantidad")
        
        if not codigo or not cantidad:
            return jsonify({"error": "Faltan datos de venta."}), 400
        
        try:
            # Leer el inventario del carro
            with open(INVENTARIO_CARRO_FILE, "r+") as f:
                productos_carro = json.load(f)
                producto = next((p for p in productos_carro if p["codigo"] == codigo), None)
                if not producto:
                    return jsonify({"error": "Producto no encontrado en el inventario del carro."}), 404
                
                if producto["cantidad"] < cantidad:
                    return jsonify({"error": "Cantidad insuficiente para venta."}), 400
                
                # Disminuir la cantidad en el inventario del carro
                producto["cantidad"] -= cantidad
                
                # Guardar los cambios en el archivo JSON
                f.seek(0)
                f.truncate()
                json.dump(productos_carro, f, indent=4)
                
                # Registrar la venta en ventas_vendedor.json
                with open("json/ventas_vendedor.json", "r+") as f:
                    ventas = json.load(f)
                    nueva_venta = {
                        "dia": datetime.now().strftime("%A"),  # Día de la semana en inglés (puedes traducirlo si quieres)
                        "fecha": datetime.now().strftime("%d/%m/%Y"),  # Fecha en formato día/mes/año
                        "hora": datetime.now().strftime("%H:%M"),  # Hora en formato 24h
                        "producto": producto["nombre"],
                        "cantidad": cantidad,
                        "precio": producto["precio"],
                        "total": cantidad * producto["precio"]
                        }
                    ventas.append(nueva_venta)
                    
                    f.seek(0)
                    f.truncate()
                    json.dump(ventas, f, indent=4)
                    
                    return jsonify({"mensaje": "Venta registrada exitosamente."})
        
        except Exception as e:
            
            return jsonify({"error": f"Hubo un error: {e}"}), 500
        
    # 📌 Ruta para registrar una venta en el Inventario del Carro solo pagina (Admin, Supervisor y vendedor)
    @app.route("/registrar_venta_carro", methods=["GET"])
    def registrar_venta_carro_html():
        
        # Verificar si el usuario está autenticado
        if "usuario_id" not in session:
            return redirect(url_for('login'))

        # Permitir que administradores, supervisores y vendedores accedan a esta página
        usuario_rol = session.get("usuario_rol")
        if usuario_rol not in ["vendedor", "admin", "supervisor"]:
            return redirect(url_for('login'))  # Redirigir a página de inicio si no tiene permiso

        # Renderizar la plantilla HTML para registrar la venta
        return render_template("registrar_venta_carro.html")
    
    # 📌 Ruta para registrar una entrada en el Inventario del Carro (admin/supervisor y vendedor)
    @app.route("/api/registrar_entrada_carro", methods=["POST"])
    def registrar_entrada_carro():
        if "usuario_id" not in session:
            return jsonify({"error": "No tienes sesión activa."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        cantidad = data.get("cantidad")
        
        if not codigo or not cantidad:
            return jsonify({"error": "Faltan datos de entrada."}), 400
        
        try:
            # 📌 Actualizar el inventario del carro: se aumenta la cantidad
            with open(INVENTARIO_CARRO_FILE, "r+") as f:
                productos_carro = json.load(f)
                producto_carro = next((p for p in productos_carro if p["codigo"] == codigo), None)
                
                if producto_carro:
                    producto_carro["cantidad"] += cantidad
                else:
                    return jsonify({"error": "Producto no encontrado en el inventario del carro."}), 404
                
                f.seek(0)
                f.truncate()
                json.dump(productos_carro, f, indent=4)
                
                # 📌 Actualizar el Inventario Mayor: se disminuye la cantidad
                with open(INVENTARIO_FILE, "r+") as f:
                    productos_mayor = json.load(f)
                    producto_mayor = next((p for p in productos_mayor if p["codigo"] == codigo), None)
                    if producto_mayor:
                        if producto_mayor["cantidad"] < cantidad:
                            return jsonify({"error": "Cantidad insuficiente en inventario mayor."}), 400
                        producto_mayor["cantidad"] -= cantidad
                    else:
                        return jsonify({"error": "Producto no encontrado en el inventario mayor."}), 404
                    
                    f.seek(0)
                    f.truncate()
                    json.dump(productos_mayor, f, indent=4)
                    
                    # 📌 Registrar el retiro en retiros_vendedor.json
                    with open("json/retiros_vendedor.json", "r+") as f:
                        retiros = json.load(f)
                        nuevo_retiro = {
                            "dia": datetime.now().strftime("%A"),  # Día de la semana en inglés
                            "fecha": datetime.now().strftime("%d/%m/%Y"),  # Fecha en formato día/mes/año
                            "hora": datetime.now().strftime("%H:%M"),  # Hora en formato 24h
                            "producto": producto_carro["nombre"],
                            "cantidad": cantidad
                            }
                        retiros.append(nuevo_retiro)
                        
                        f.seek(0)
                        f.truncate()
                        json.dump(retiros, f, indent=4)
                        
                        return jsonify({"mensaje": "Entrada registrada exitosamente."})
        except Exception as e:
            
            return jsonify({"error": f"Hubo un error: {e}"}), 500
    
    # 📌 Ruta para mostrar la página de agregar productos al Inventario del Carro
    @app.route("/agregar_producto_carro", methods=["GET"])
    def agregar_producto_carro():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor", "vendedor"]:
            return redirect(url_for("login"))  # 🔒 Si no tiene permiso, lo manda al login
        
        return render_template("agregar_producto_carro.html")  # Solo muestra la página

    # 📌 Ruta para Inventario del Carro 2 (Acceso para Admin, Supervisor y Vendedor2)
    @app.route("/inventario_carro2")
    def inventario_carro2():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor", "vendedor2"]:
            return redirect(url_for("login"))  # Redirige al login si el rol no es permitido
        
        # Pasamos el rol del usuario para controlarlo en el frontend
        rol_usuario = session.get("usuario_rol")
        return render_template("inventario_carro2.html", rol=rol_usuario)

    # 📌 Ruta para obtener los productos del Inventario del Carro con filtros y ordenación
    @app.route("/api/inventario_carro2", methods=["GET"])
    def obtener_inventario_carro2():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor", "vendedor2"]:
            return redirect(url_for("login"))  # Redirige al login si el rol no es permitido
        
        try:
            # Cargar productos del inventario del carro desde el archivo JSON
            productos_carro = cargar_inventario_carro2()

            # 🔍 Obtener parámetros de filtrado desde la URL
            filtro_nombre_codigo = request.args.get("buscar", "").strip().lower()
            filtro_categoria = request.args.get("categoria", "").strip().lower()
            ordenar_por = request.args.get("ordenar", "").strip().lower()

            # 🔎 Filtrar por nombre o código
            if filtro_nombre_codigo:
                productos_carro = [p for p in productos_carro if filtro_nombre_codigo in p["nombre"].lower() or filtro_nombre_codigo in p["codigo"].lower()]

            # 📂 Filtrar por categoría
            if filtro_categoria:
                productos_carro = [p for p in productos_carro if p["categoria"].lower() == filtro_categoria]

            # 🔢 Ordenar por cantidad (mayor a menor)
            if ordenar_por == "cantidad":
                productos_carro.sort(key=lambda p: int(p["cantidad"]), reverse=True)

            # 💰 Ordenar por precio (mayor a menor)
            elif ordenar_por == "costo":
                productos_carro.sort(key=lambda p: float(p["precio"]), reverse=True)

            return jsonify(productos_carro)  # Devuelve los productos en formato JSON
        except Exception as e:
            return jsonify({"error": f"Hubo un error: {e}"}), 500
        
    # 📌 Ruta para agregar un producto al Inventario del Carro2 (Admin y Supervisor)
    @app.route("/api/agregar_producto_carro2", methods=["POST"])
    def api_agregar_producto_carro2():
        if "usuario_id" not in session or session.get("usuario_rol") == "vendedor2":
            return jsonify({"error": "No tienes permiso para agregar productos."}), 403

        data = request.get_json()
        codigo = data.get("codigo")
        nombre = data.get("nombre")
        categoria = data.get("categoria")
        cantidad = data.get("cantidad")
        precio = data.get("precio")

        # Verificar que todos los campos obligatorios estén presentes
        if not all([codigo, nombre, categoria, cantidad, precio]):
            return jsonify({"error": "Faltan datos del producto."}), 400

        try:
            cantidad = int(cantidad)  # Validar que sea un número entero
            precio = float(precio)  # Validar que sea un número flotante
        except ValueError:
            return jsonify({"error": "Cantidad y precio deben ser números válidos."}), 400

        try:
            # Cargar el inventario actual
            productos_carro = cargar_inventario_carro2()

            # Verificar si el producto ya existe en el inventario
            for producto in productos_carro:
                if producto["codigo"] == codigo:
                    return jsonify({"error": "El producto con este código ya existe."}), 400

            # Agregar el nuevo producto
            productos_carro.append({
                "codigo": codigo,
                "nombre": nombre,
                "categoria": categoria,
                "cantidad": cantidad,
                "precio": precio
            })

            # Guardar el inventario actualizado
            guardar_inventario_carro2(productos_carro)

            return jsonify({"mensaje": "Producto agregado al carro exitosamente."}), 201
        except Exception as e:
            print(f"❌ Error al agregar producto al carro: {e}")
            return jsonify({"error": "Hubo un error en el servidor."}), 500
        
    # 📌 Ruta para editar un producto en el inventario del Carro (Admin y Supervisor)
    @app.route("/api/editar_producto_carro2", methods=["POST"])
    def editar_producto_carro2():
        # Verificación de permisos
        if "usuario_id" not in session or session["usuario_rol"] not in ["admin", "supervisor"]:
            return jsonify({"error": "No tienes permisos para editar productos."}), 403

        # Cargar los datos recibidos en la petición
        datos = request.json
        codigo = datos.get("codigo")
        if not codigo:
            return jsonify({"error": "Código del producto no proporcionado"}), 400

        # Cargar el inventario del carro
        productos_carro = cargar_inventario_carro2()

        # Buscar el producto
        producto = next((p for p in productos_carro if p["codigo"] == codigo), None)
        if not producto:
            return jsonify({"error": "Producto no encontrado"}), 404

        # Actualizar los campos del producto solo si se proporcionan nuevos valores
        producto["nombre"] = datos.get("nombre", producto["nombre"])
        producto["categoria"] = datos.get("categoria", producto["categoria"])

        # Validar y actualizar la cantidad, si se proporciona
        nueva_cantidad = datos.get("cantidad")
        if nueva_cantidad is not None:
            try:
                producto["cantidad"] = int(nueva_cantidad)
            except ValueError:
                return jsonify({"error": "Cantidad debe ser un número entero válido."}), 400

        # Validar y actualizar el precio, si se proporciona
        nuevo_precio = datos.get("precio")
        if nuevo_precio is not None:
            try:
                producto["precio"] = float(nuevo_precio)
            except ValueError:
                return jsonify({"error": "Precio debe ser un número válido."}), 400

        # Guardar el inventario actualizado
        guardar_inventario_carro2(productos_carro)

        # Devolver la respuesta con el producto actualizado
        return jsonify({
            "mensaje": "Producto actualizado correctamente",
            "producto_actualizado": producto
        }), 200

    # 📌 Ruta para eliminar un producto del Inventario del Carro 2
    @app.route("/api/eliminar_producto_carro2", methods=["POST"])
    def eliminar_producto_carro2():
        if "usuario_id" not in session or session.get("usuario_rol") == "vendedor2":
            return jsonify({"error": "No tienes permiso para eliminar productos."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        
        if not codigo:
            return jsonify({"error": "Falta el código del producto."}), 400
        
        try:
            productos_carro = cargar_inventario_carro2()
            producto = next((p for p in productos_carro if p["codigo"] == codigo), None)
            if not producto:
                return jsonify({"error": "Producto no encontrado."}), 404
            
            productos_carro = [p for p in productos_carro if p["codigo"] != codigo]
            guardar_inventario_carro2(productos_carro)
            
            return jsonify({"mensaje": "Producto eliminado exitosamente."}), 200
        except Exception as e:
            return jsonify({"error": f"Hubo un error: {e}"}), 500

    # 📌 Ruta para registrar una venta en el Inventario del Carro 2
    @app.route("/api/registrar_venta_carro2", methods=["POST"])
    def registrar_venta_carro2():
        if "usuario_id" not in session:
            return jsonify({"error": "No estás autenticado."}), 403
        
        usuario_rol = session.get("usuario_rol")
        if usuario_rol not in ["vendedor2", "admin", "supervisor"]:
            return jsonify({"error": "No tienes permiso para registrar ventas."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        cantidad = data.get("cantidad")

        if not codigo or not cantidad:
            return jsonify({"error": "Faltan datos de venta."}), 400

        try:
            productos_carro = cargar_inventario_carro2()
            producto = next((p for p in productos_carro if p["codigo"] == codigo), None)

            if not producto:
                return jsonify({"error": "Producto no encontrado en el inventario del carro."}), 404

            if producto["cantidad"] < cantidad:
                return jsonify({"error": "Cantidad insuficiente para venta."}), 400

            producto["cantidad"] -= cantidad
            guardar_inventario_carro2(productos_carro)

            # 📌 Guardar la venta en ventas_vendedor2.json
            with open("json/ventas_vendedor2.json", "r+") as f:
                ventas = json.load(f)
                fecha_hora = datetime.now().strftime("%A %d/%m/%Y %H:%M")  # Formato: Martes 02/04/2025 14:30
                total_final = cantidad * producto["precio"]

                ventas.append({
                    "fecha": fecha_hora,
                    "codigo": codigo,
                    "producto": producto["nombre"],
                    "cantidad": cantidad,
                    "precio": producto["precio"],
                    "total": total_final
                })

                f.seek(0)
                f.truncate()
                json.dump(ventas, f, indent=4)

            return jsonify({"mensaje": "Venta registrada exitosamente para Vendedor 2."})

        except Exception as e:
            return jsonify({"error": f"Hubo un error: {e}"}), 500

    # 📌 Ruta para registrar una entrada en el Inventario del Carro 2
    @app.route("/api/registrar_entrada_carro2", methods=["POST"])
    def registrar_entrada_carro2():
        if "usuario_id" not in session:
            return jsonify({"error": "No tienes sesión activa."}), 403
        
        data = request.get_json()
        codigo = data.get("codigo")
        cantidad = data.get("cantidad")

        if not codigo or not cantidad:
            return jsonify({"error": "Faltan datos de entrada."}), 400

        try:
            productos_carro = cargar_inventario_carro2()
            producto_carro = next((p for p in productos_carro if p["codigo"] == codigo), None)

            if producto_carro:
                producto_carro["cantidad"] += cantidad
            else:
                return jsonify({"error": "Producto no encontrado en el inventario del carro 2."}), 404

            guardar_inventario_carro2(productos_carro)

            # 📌 Descontar del Inventario Mayor
            with open(INVENTARIO_FILE, "r+") as f:
                productos_mayor = json.load(f)
                producto_mayor = next((p for p in productos_mayor if p["codigo"] == codigo), None)

                if producto_mayor:
                    if producto_mayor["cantidad"] < cantidad:
                        return jsonify({"error": "Cantidad insuficiente en inventario mayor."}), 400
                    producto_mayor["cantidad"] -= cantidad
                else:
                    return jsonify({"error": "Producto no encontrado en el inventario mayor."}), 404

                f.seek(0)
                f.truncate()
                json.dump(productos_mayor, f, indent=4)

            # 📌 Guardar retiro en retiros_vendedor2.json
            with open("json/retiros_vendedor2.json", "r+") as f:
                retiros = json.load(f)
                fecha_hora = datetime.now().strftime("%A %d/%m/%Y %H:%M")  # Formato: Martes 02/04/2025 14:30
                retiros.append({
                    "fecha": fecha_hora,
                    "codigo": codigo,
                    "producto": producto_mayor["nombre"],
                    "cantidad": cantidad
                })

                f.seek(0)
                f.truncate()
                json.dump(retiros, f, indent=4)

            return jsonify({"mensaje": "Entrada y retiro registrado exitosamente para Vendedor 2."})

        except Exception as e:
            return jsonify({"error": f"Hubo un error: {e}"}), 500
        
    # 📌 Ruta para mostrar la página de agregar productos al Inventario del Carro 2
    @app.route("/agregar_producto_carro2", methods=["GET"])
    def agregar_producto_carro2():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor", "vendedor2"]:
            return redirect(url_for("login"))
        
        return render_template("agregar_producto_carro2.html")

    # 📌 Ruta para ver la seccion de las notificaciones
    @app.route("/ver_notificaciones")
    def ver_notificaciones():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("ver_notificaciones.html")

    # 📌 Ruta para Notificaciones del Vendedor 1
    @app.route("/notificaciones")
    def notificaciones():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("notificaciones.html")

    # 📌 Ruta para ver Entradas de Productos del Vendedor 1
    @app.route("/notificaciones_entrada")
    def notificaciones_entrada():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("notificaciones_entrada.html")

    # 📌 Ruta para obtener las entradas de productos del vendedor
    @app.route("/api/notificaciones_entrada", methods=["GET"])
    def get_notificaciones_entrada():
        # Verificar si los archivos existen
        if not os.path.exists(RETIROS_VENDEDOR_FILE) or not os.path.exists(INVENTARIO_FILE):
            return jsonify([])  # Si no existen, devolver lista vacía

        # Cargar las entradas
        with open(RETIROS_VENDEDOR_FILE, "r") as f:
            notificaciones = json.load(f)

        # Cargar el inventario mayor
        with open(INVENTARIO_FILE, "r") as f:
            inventario = json.load(f)

        # Crear un diccionario {nombre_producto: {codigo, categoria, precio}}
        inventario_dict = {
            item["nombre"]: {
                "codigo": item["codigo"],
                "categoria": item["categoria"],
                "precio": item.get("costo", 0)  # Suponiendo que el precio está guardado como "costo"
            }
            for item in inventario
        }

        # Traducir días de la semana
        dias_espanol = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }

        # Agregar código, categoría, precio y formato de hora a las entradas
        for entrada in notificaciones:
            # Obtener día de la semana
            if "fecha" in entrada and entrada["fecha"]:
                try:
                    fecha_obj = datetime.strptime(entrada["fecha"], "%d/%m/%Y")
                    entrada["dia"] = dias_espanol[fecha_obj.strftime("%A")]
                except ValueError:
                    entrada["dia"] = "Fecha inválida"
            else:
                entrada["dia"] = "Sin fecha"

            # Asegurar que la hora está en el formato correcto
            entrada["hora"] = entrada.get("hora", "Sin hora")

            # Buscar en el inventario el código, la categoría y el precio
            datos_inventario = inventario_dict.get(entrada["producto"], {"codigo": "Sin código", "categoria": "Sin categoría", "precio": 0})
            entrada["codigo"] = datos_inventario["codigo"]
            entrada["categoria"] = datos_inventario["categoria"]
            entrada["precio"] = datos_inventario["precio"]  # Aquí agregamos el precio

        return jsonify(notificaciones)

    # 📌 Ruta para ver Ventas de Productos del Vendedor 1
    @app.route("/notificaciones_venta")
    def notificaciones_venta():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("notificaciones_venta.html")

    # 📌 Ruta para obtener las ventas del vendedor
    @app.route("/api/notificaciones_venta", methods=["GET"])
    def get_notificaciones_venta():
        # Verificar si los archivos existen
        if not os.path.exists(VENTAS_VENDEDOR_FILE) or not os.path.exists(INVENTARIO_FILE):
            return jsonify([])

        # Cargar las ventas
        with open(VENTAS_VENDEDOR_FILE, "r") as f:
            notificaciones = json.load(f)

        # Cargar el inventario mayor
        with open(INVENTARIO_FILE, "r") as f:
            inventario = json.load(f)

        # Crear un diccionario {nombre_producto: {codigo, categoria}}
        inventario_dict = {item["nombre"]: {"codigo": item["codigo"], "categoria": item["categoria"]} for item in inventario}

        # Traducir días de la semana
        dias_espanol = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }

        # Agregar código, categoría y formato de hora a las ventas
        for venta in notificaciones:
            # Obtener día de la semana
            if "fecha" in venta and venta["fecha"]:
                try:
                    fecha_obj = datetime.strptime(venta["fecha"], "%d/%m/%Y")
                    venta["dia"] = dias_espanol[fecha_obj.strftime("%A")]
                except ValueError:
                    venta["dia"] = "Fecha inválida"
            else:
                venta["dia"] = "Sin fecha"

            # Asegurar que la hora está en el formato correcto
            venta["hora"] = venta.get("hora", "Sin hora")

            # Buscar en el inventario el código y la categoría
            datos_inventario = inventario_dict.get(venta["producto"], {"codigo": "Sin código", "categoria": "Sin categoría"})
            venta["codigo"] = datos_inventario["codigo"]
            venta["categoria"] = datos_inventario["categoria"]

        return jsonify(notificaciones)

    # 📌 Ruta para eliminar notificaciones (ventas o entradas)
    @app.route("/api/notificaciones/eliminar", methods=["POST"])
    def eliminar_notificaciones():
        data = request.json
        tipo = data.get("tipo")  # "entrada" o "venta"
        dias = data.get("dias")  # "todas" o número de días

        # Determinar el archivo a modificar
        archivo = RETIROS_VENDEDOR_FILE if tipo == "entrada" else VENTAS_VENDEDOR_FILE

        if not os.path.exists(archivo):
            return jsonify({"mensaje": "No hay notificaciones para eliminar"}), 200

        # Cargar notificaciones desde el archivo JSON
        with open(archivo, "r", encoding="utf-8") as f:
            notificaciones = json.load(f)

        # Si el usuario selecciona "todas", se vacía la lista
        if dias == "todas":
            notificaciones_filtradas = []
        else:
            try:
                dias = int(dias)
                fecha_limite = datetime.now() - timedelta(days=dias)

                # Filtrar las notificaciones recientes
                notificaciones_filtradas = []
                for n in notificaciones:
                    try:
                        fecha_noti = datetime.strptime(n["fecha"], "%Y-%m-%d %H:%M:%S")  # Con hora
                    except ValueError:
                        fecha_noti = datetime.strptime(n["fecha"], "%Y-%m-%d")  # Sin hora
                    
                    if fecha_noti > fecha_limite:
                        notificaciones_filtradas.append(n)
            
            except ValueError:
                return jsonify({"mensaje": "El valor de 'dias' no es válido"}), 400

        # Guardar las notificaciones actualizadas
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump(notificaciones_filtradas, f, indent=4)

        return jsonify({"mensaje": "Notificaciones eliminadas correctamente"})

    # 📌 Ruta para Notificaciones del Vendedor 2
    @app.route("/notificaciones2")
    def notificaciones2():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("notificaciones2.html")

    # 📌 Ruta para ver las entradas del vendedor 2
    @app.route("/notificaciones_entrada2")
    def notificaciones_entrada2():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("notificaciones_entrada2.html")

    # 📌 Ruta para obtener las entradas del vendedor 2
    @app.route("/api/notificaciones_entrada2", methods=["GET"])
    def get_notificaciones_entrada2():
        if not os.path.exists(RETIROS_VENDEDOR2_FILE) or not os.path.exists(INVENTARIO_FILE):
            return jsonify([])

        with open(RETIROS_VENDEDOR2_FILE, "r") as f:
            notificaciones = json.load(f)

        with open(INVENTARIO_FILE, "r") as f:
            inventario = json.load(f)

        inventario_dict = {
            item["nombre"]: {
                "codigo": item["codigo"],
                "categoria": item["categoria"],
                "precio": item.get("costo", 0)
            }
            for item in inventario
        }

        dias_espanol = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }

        for entrada in notificaciones:
            # 🔹 Obtener fecha y hora correctamente
            fecha_str = entrada.get("fecha", "")
            if fecha_str:
                try:
                    # Si la fecha incluye hora (como "Wednesday 02/04/2025 14:27")
                    if any(day in fecha_str for day in dias_espanol.keys()):
                        fecha_obj = datetime.strptime(fecha_str, "%A %d/%m/%Y %H:%M")
                    else:
                        fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")

                    entrada["dia"] = dias_espanol[fecha_obj.strftime("%A")]
                    entrada["fecha"] = fecha_obj.strftime("%d/%m/%Y")
                    entrada["hora"] = fecha_obj.strftime("%H:%M")  # Extraer la hora correctamente
                except ValueError:
                    entrada["dia"] = "Fecha inválida"
                    entrada["fecha"] = "Fecha inválida"
                    entrada["hora"] = "Sin hora"
            else:
                entrada["dia"] = "Sin fecha"
                entrada["fecha"] = "Sin fecha"
                entrada["hora"] = "Sin hora"

            datos_inventario = inventario_dict.get(entrada["producto"], {"codigo": "Sin código", "categoria": "Sin categoría", "precio": 0})
            entrada["codigo"] = datos_inventario["codigo"]
            entrada["categoria"] = datos_inventario["categoria"]
            entrada["precio"] = datos_inventario["precio"]

        return jsonify(notificaciones)

    # 📌 Ruta para ver las ventas del vendedor 2
    @app.route("/notificaciones_venta2")
    def notificaciones_venta2():
        if "usuario_id" not in session or session.get("usuario_rol") not in ["admin", "supervisor"]:
            return redirect(url_for("login"))
        
        return render_template("notificaciones_venta2.html")

    # 📌 Ruta para obtener las ventas del vendedor 2
    @app.route("/api/notificaciones_venta2", methods=["GET"])
    def get_notificaciones_venta2():
        if not os.path.exists(VENTAS_VENDEDOR2_FILE) or not os.path.exists(INVENTARIO_FILE):
            return jsonify([])

        with open(VENTAS_VENDEDOR2_FILE, "r") as f:
            notificaciones = json.load(f)

        with open(INVENTARIO_FILE, "r") as f:
            inventario = json.load(f)

        # Crear un diccionario {nombre_producto: {codigo, categoría}}
        inventario_dict = {
            item["nombre"]: {"codigo": item["codigo"], "categoria": item["categoria"]}
            for item in inventario
        }

        # Traducir días de la semana
        dias_espanol = {
            "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Miércoles",
            "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "Sábado", "Sunday": "Domingo"
        }

        for venta in notificaciones:
            fecha_original = venta.get("fecha", "")

            if fecha_original:
                # Ignorar el primer campo (el día de la semana en inglés) y procesar solo la fecha
                fecha_sin_dia = " ".join(fecha_original.split(" ")[1:])

                formatos_fecha = ["%d/%m/%Y %H:%M", "%d/%m/%Y"]  # Soportar dos formatos posibles
                fecha_valida = False

                for formato in formatos_fecha:
                    try:
                        fecha_obj = datetime.strptime(fecha_sin_dia, formato)
                        venta["dia"] = dias_espanol[fecha_obj.strftime("%A")]
                        venta["fecha"] = fecha_obj.strftime("%d/%m/%Y")  # Mantener formato estándar
                        venta["hora"] = fecha_obj.strftime("%H:%M") if " " in fecha_original else "Sin hora"
                        fecha_valida = True
                        break  # Si se pudo parsear con un formato, salir del loop
                    except ValueError:
                        continue  # Intentar el siguiente formato

                if not fecha_valida:
                    venta["dia"] = "Fecha inválida"
                    venta["fecha"] = "Fecha inválida"
                    venta["hora"] = "Sin hora"
            else:
                venta["dia"] = "Sin fecha"
                venta["fecha"] = "Sin fecha"
                venta["hora"] = "Sin hora"

            # Buscar en el inventario el código y la categoría
            datos_inventario = inventario_dict.get(venta["producto"], {"codigo": "Sin código", "categoria": "Sin categoría"})
            venta["codigo"] = datos_inventario["codigo"]
            venta["categoria"] = datos_inventario["categoria"]

        return jsonify(notificaciones)

    # 📌 Ruta para cerrar sesión
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("login"))
    
    return app

# Ejecutar la aplicación directamente
if __name__ == "__main__":
    app = crear_app()
    app.run(host="0.0.0.0", port=8080, debug=True)