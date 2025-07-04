from controllers.funciones_login import *
from app import app
from flask import render_template, request, flash, redirect, url_for, session,  jsonify
from mysql.connector.errors import Error


# Importando cenexión a BD
from controllers.funciones_home import *


# ------------------------------------------------------------
# RUTA: LISTA DE ÁREAS
# ------------------------------------------------------------
# Muestra la lista de áreas registradas en el sistema.
# Solo accesible si el usuario está autenticado ('conectado' en sesión).
# Si no está autenticado, redirige a la página de inicio con mensaje de error.

@app.route('/lista-de-areas', methods=['GET'])
def lista_areas():
    if 'conectado' in session:
        return render_template('public/usuarios/lista_areas.html', areas=lista_areasBD(), dataLogin=dataLoginSesion())
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    

# ------------------------------------------------------------
# RUTA: LISTA DE USUARIOS
# ------------------------------------------------------------
# lO MISMO DEL PRIMERO.
@app.route("/lista-de-usuarios", methods=['GET'])
def usuarios():
    if 'conectado' in session:
        return render_template('public/usuarios/lista_usuarios.html',  resp_usuariosBD=lista_usuariosBD(), dataLogin=dataLoginSesion(), areas=lista_areasBD(), roles = lista_rolesBD())
    else:
        return redirect(url_for('inicioCpanel'))
    

# ------------------------------------------------------------
# RUTA: LISTA DE AUTORES
# ------------------------------------------------------------
# lO MISMO DEL PRIMERO.
@app.route("/lista-de-autores", methods=['GET'])
def autores():
    """
    Ruta para mostrar la lista de autores.
    Requiere que el usuario esté conectado.
    """
    if 'conectado' in session:
        # Renderiza la plantilla HTML para la lista de autores
        # Pasando los datos de los autores y la información de la sesión
        return render_template(
            'public/usuarios/autores.html',
            resp_autoresBD=lista_autoresBD(), # Datos de los autores desde la base de datos
            dataLogin=dataLoginSesion()       # Datos del usuario logueado
        )
    else:
        # Si el usuario no está conectado, redirige a la página de inicio del cPanel
        return redirect(url_for('inicioCpanel'))
    
# ------------------------------------------------------------
# RUTA: LISTA DE CATEGORÍAS
# ------------------------------------------------------------
# lO MISMO DEL PRIMERO.
@app.route("/lista-de-categorias", methods=['GET'])
def categorias():
    """
    Ruta para mostrar la lista de categorías.
    Requiere que el usuario esté conectado.
    """
    if 'conectado' in session:
        # Renderiza la plantilla HTML para la lista de categorías
        # Pasando los datos de las categorías obtenidos de la base de datos
        # y la información de la sesión.
        return render_template(
            'public/usuarios/lista_categorias.html', # Asegúrate de que esta sea la ruta correcta
            resp_categoriasBD=lista_categoriasBD(),    # Datos de las categorías desde la base de datos
            dataLogin=dataLoginSesion()                # Datos del usuario logueado
        )
    else:
        # Si el usuario no está conectado, redirige a la página de inicio del cPanel
        return redirect(url_for('inicioCpanel'))
    

# ------------------------------------------------------------
# RUTA: LISTA DE UBICACIONES
# ------------------------------------------------------------
# lO MISMO DEL PRIMERO.   
@app.route("/lista-de-ubicaciones", methods=['GET'])
def ubicaciones():
    """
    Ruta para mostrar la lista de ubicaciones.
    Requiere que el usuario esté conectado.
    """
    if 'conectado' in session:
        # Renderiza la plantilla HTML para la lista de ubicaciones
        # Pasando los datos de las ubicaciones obtenidos de la base de datos
        # y la información de la sesión.
        return render_template(
            'public/usuarios/lista_ubicaciones.html', # La ruta de la plantilla asumiendo que está en esta ubicación
            resp_ubicacionesBD=lista_ubicacionesBD(),    # Datos de las ubicaciones desde la base de datos
            dataLogin=dataLoginSesion()                  # Datos del usuario logueado
        )
    else:
        # Si el usuario no está conectado, redirige a la página de inicio del cPanel
        return redirect(url_for('inicioCpanel'))
    
    
# ------------------------------------------------------------
# RUTA: LISTA DE LIBROS
# ------------------------------------------------------------
# lO MISMO DEL PRIMERO.  
@app.route("/lista-de-libros1", methods=['GET'])
def libros1():
    if 'conectado' in session:
        return render_template(
            'public/biblioteca/lista_libros1.html',
            libros=lista_librosBD(),      # <--- Cambia a 'libros'
            dataLogin=dataLoginSesion()
        )
    else:
        return redirect(url_for('inicioCpanel'))
    
    

# ------------------------------------------------------------
# RUTA: ELIMINAR USUARIO
# ------------------------------------------------------------
# Elimina un usuario específico por su ID.
# Si la eliminación es exitosa, muestra mensaje de éxito
# y redirige a la lista de usuarios.
@app.route('/borrar-usuario/<string:id>', methods=['GET'])
def borrarUsuario(id):
    resp = eliminarUsuario(id)
    if resp:
        flash('El Usuario fue eliminado correctamente', 'success')
        return redirect(url_for('usuarios'))
    


# ------------------------------------------------------------
# RUTA: ELIMINAR ÁREA
# ------------------------------------------------------------
# Elimina un área específica por su ID.
# Si la eliminación es exitosa, muestra mensaje de éxito
# y redirige a la lista de áreas.
# Si existen usuarios asociados a esa área, muestra error
# y no elimina el área.
@app.route('/borrar-area/<string:id_area>/', methods=['GET'])
def borrarArea(id_area):
    resp = eliminarArea(id_area)
    if resp:
        flash('El Empleado fue eliminado correctamente', 'success')
        return redirect(url_for('lista_areas'))
    else:
        flash('Hay usuarios que pertenecen a esta área', 'error')
        return redirect(url_for('lista_areas'))


# ------------------------------------------------------------
# RUTA: DESCARGAR INFORME DE ACCESOS
# ------------------------------------------------------------
# Permite descargar un reporte de accesos en formato Excel.
# Solo accesible si el usuario está autenticado ('conectado' en sesión).
# Si no está autenticado, muestra mensaje de error y redirige al inicio.
@app.route("/descargar-informe-accesos/", methods=['GET'])
def reporteBD():
    if 'conectado' in session:
        return generarReporteExcel()
    else:
        flash('primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))
    

# ------------------------------------------------------------
# RUTA: VISTA DE REPORTE DE ACCESOS
# ------------------------------------------------------------
# Muestra en pantalla el reporte de accesos del usuario.
# Solo accesible si el usuario está autenticado ('conectado' en sesión).
@app.route("/reporte-accesos", methods=['GET'])
def reporteAccesos():
    if 'conectado' in session:
        userData = dataLoginSesion()
        return render_template('public/perfil/reportes.html',  reportes=dataReportes(),lastAccess=lastAccessBD(userData.get('cedula')), dataLogin=dataLoginSesion())


# ------------------------------------------------------------
# RUTA: INTERFAZ PARA GENERAR CLAVES
# ------------------------------------------------------------
# Muestra la interfaz para generar o administrar claves.
# Accesible mediante métodos GET y POST.
@app.route("/interfaz-clave", methods=['GET','POST'])
def claves():
    return render_template('public/usuarios/generar_clave.html', dataLogin=dataLoginSesion())


# ------------------------------------------------------------
# RUTA: DASHBOARD PRINCIPAL
# ------------------------------------------------------------
# Muestra la página principal de control (dashboard) del sistema.
# Accesible mediante métodos GET y POST.
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template('public/usuarios/dashboard.html', dataLogin=dataLoginSesion())
#DASBOARD


# ------------------------------------------------------------
# RUTA: GENERAR Y GUARDAR CLAVE PARA USUARIO
# ------------------------------------------------------------
# Genera una clave nueva para el usuario con el ID especificado.
# Guarda la clave en la auditoría y devuelve la clave generada.
# Accesible mediante métodos GET y POST.
    
@app.route('/generar-y-guardar-clave/<string:id>', methods=['GET','POST'])
def generar_clave(id):
    print(id)
    clave_generada = crearClave()  # Llama a la función para generar la clave
    guardarClaveAuditoria(clave_generada,id)
    return clave_generada


# ------------------------------------------------------------
# RUTA: CREAR ÁREA
# ------------------------------------------------------------
# Permite crear una nueva área a través de un formulario.
# En método POST guarda el área y muestra mensaje de éxito o error.
# En método GET muestra el formulario para crear un área.
@app.route('/crear-area', methods=['GET','POST'])
def crearArea():
    if request.method == 'POST':
        area_name = request.form['nombre_area']  # Asumiendo que 'nombre_area' es el nombre del campo en el formulario
        resultado_insert = guardarArea(area_name)
        if resultado_insert:
            # Éxito al guardar el área
            flash('El Area fue creada correctamente', 'success')
            return redirect(url_for('lista_areas'))
            
        else:
            # Manejar error al guardar el área
            return "Hubo un error al guardar el área."
    return render_template('public/usuarios/lista_areas')


# ------------------------------------------------------------
# RUTA: ACTUALIZAR ÁREA
# ------------------------------------------------------------
# Actualiza el nombre de un área existente mediante formulario POST.
# Muestra mensaje de éxito o error según el resultado de la actualización.
@app.route('/actualizar-area', methods=['POST'])
def updateArea():
    if request.method == 'POST':
        nombre_area = request.form['nombre_area']  # Asumiendo que 'nuevo_nombre' es el nombre del campo en el formulario
        id_area = request.form['id_area']
        resultado_update = actualizarArea(id_area, nombre_area)
        if resultado_update:
           # Éxito al actualizar el área
            flash('El actualizar fue creada correctamente', 'success')
            return redirect(url_for('lista_areas'))
        else:
            # Manejar error al actualizar el área
            return "Hubo un error al actualizar el área."


    return redirect(url_for('lista_areas'))


    

# ============================================
# SECCIÓN: BIBLIOTECA
# SECCIÓN: BIBLIOTECA
# SECCIÓN: BIBLIOTECA
# ============================================


# =====================================
# ELIMINAR LIBRO POR ID
# =====================================
@app.route('/borrar-libro/<string:id>', methods=['GET'])
def borrarLibro(id):
    eliminado = eliminarLibro(id)
    if eliminado:
        flash('✅ El libro fue eliminado correctamente.', 'success')
    else:
        flash('❌ Hubo un error al eliminar el libro.', 'danger')
    return redirect(url_for('libros1'))  # Asegúrate que este endpoint existe



# =====================================
# MOSTRAR FORMULARIO DE EDICIÓN DE LIBRO
# =====================================
@app.route("/editar-libro/<id_libro>", methods=['GET'])
def viewEditarLibro(id_libro):
    if 'conectado' in session:
        libro = buscarLibroUnico(id_libro)  # <--- Cambia aquí
        if libro:
            return render_template('public/biblioteca/form_libro_update.html', libro=libro, dataLogin=dataLoginSesion())
        else:
            flash('El libro no existe.', 'error')
            return redirect(url_for('libros1'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('login'))


# =====================================
# ACTUALIZAR DATOS DE UN LIBRO
# =====================================
@app.route("/actualizar-libro", methods=['POST'])
def actualizarLibro():  
    if request.method == 'POST':
        try:
            id_libro = request.form['id_libro']
            titulo = request.form['titulo']
            autores = request.form['autores']
            categoria = request.form['categoria']
            ubicacion = request.form['ubicacion']
            cantidad_disponible = request.form.get('cantidad_disponible', 0)
            stock_total = request.form.get('stock_total', 0)
            anio_publicacion = request.form.get('anio_publicacion', None)
            estado = request.form.get('estado', 'activo')

            datos = {
                'titulo': titulo,
                'autores': autores,
                'ubicacion': ubicacion,
                'categoria': categoria,
                'cantidad_disponible': cantidad_disponible,
                'stock_total': stock_total,
                'anio_publicacion': anio_publicacion,
                'estado': estado
            }

            resultado_update = actualizarLibroBD(id_libro, datos)

            if resultado_update:
                flash('El libro fue actualizado correctamente.', 'success')
                return redirect(url_for('libros1'))
            else:
                flash('No se realizaron cambios en el libro.', 'error')
                return redirect(url_for('viewEditarLibro', id_libro=id_libro))

        except Exception as e:
            print(f"Error en actualizarLibro(): {e}")
            flash('Error en el formulario de actualización.', 'error')
            return redirect(url_for('libros1'))

    else:
        flash('Método no permitido.', 'error')
        return redirect(url_for('libros1'))
    

# ============================================
# SECCIÓN: SENSORES
# SECCIÓN: SENSORES
# SECCIÓN: SENSORES
# ============================================

#Datos sensor humo
@app.route('/sensor-humo', methods=['GET'])
def sensor_hum():
    if 'conectado' in session:
        try:
            # Obtiene los datos de los sensores de temperatura desde la base de datos
            datos_sensor_humo = sensor_humo()

            # Renderiza la plantilla con los datos
            return render_template('public/sensores/sensor_humo.html', datos_sensor_humo = sensor_humo(), dataLogin=dataLoginSesion())
        except Exception as e:
            flash(f"Error al obtener datos de sensor de humo: {e}", 'error')
            return redirect(url_for('inicio'))
    else:
        flash('Primero debes iniciar sesión.', 'error')
        return redirect(url_for('inicio'))