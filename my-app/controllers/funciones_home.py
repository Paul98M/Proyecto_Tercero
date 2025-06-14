
# Para subir archivo tipo foto al servidor
from werkzeug.utils import secure_filename
import uuid  # Modulo de python para crear un string

from conexion.conexionBD import connectionBD  # Conexión a BD

import datetime
import re
import os

from os import remove  # Modulo  para remover archivo
from os import path  # Modulo para obtener la ruta o directorio


import openpyxl  # Para generar el excel
# biblioteca o modulo send_file para forzar la descarga
from flask import send_file, session

def accesosReporte():
    if session['rol'] == 1 :
        try:
            with connectionBD() as conexion_MYSQLdb:
                with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                    querySQL = ("""
                        SELECT a.id_acceso, u.cedula, a.fecha, r.nombre_area, a.clave 
                        FROM accesos a 
                        JOIN usuarios u 
                        JOIN area r
                        WHERE u.id_area = r.id_area AND u.id_usuario = a.id_usuario
                        ORDER BY u.cedula, a.fecha DESC
                                """) 
                    cursor.execute(querySQL)
                    accesosBD=cursor.fetchall()
                return accesosBD
        except Exception as e:
            print(
                f"Errro en la función accesosReporte: {e}")
            return None
    else:
        cedula = session['cedula']
        try:
            with connectionBD() as conexion_MYSQLdb:
                with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                    querySQL = ("""
                        SELECT 
                            a.id_acceso, 
                            u.cedula, 
                            a.fecha,
                            r.nombre_area, 
                            a.clave 
                            FROM accesos a 
                            JOIN usuarios u JOIN area r 
                            WHERE u.id_usuario = a.id_usuario AND u.id_area = r.id_area AND u.cedula = %s
                            ORDER BY u.cedula, a.fecha DESC
                                """) 
                    cursor.execute(querySQL,(cedula,))
                    accesosBD=cursor.fetchall()
                return accesosBD
        except Exception as e:
            print(
                f"Errro en la función accesosReporte: {e}")
            return None


def generarReporteExcel():
    dataAccesos = accesosReporte()
    wb = openpyxl.Workbook()
    hoja = wb.active

    # Agregar la fila de encabezado con los títulos
    cabeceraExcel = ("ID", "CEDULA", "FECHA", "ÁREA", "CLAVE GENERADA")

    hoja.append(cabeceraExcel)

    # Agregar los registros a la hoja
    for registro in dataAccesos:
        id_acceso = registro['id_acceso']
        cedula = registro['cedula']
        fecha = registro['fecha']
        area = registro['nombre_area']
        clave = registro['clave']

        # Agregar los valores a la hoja
        hoja.append((id_acceso, cedula, fecha,area, clave))

    fecha_actual = datetime.datetime.now()
    archivoExcel = f"Reporte_accesos_{session['cedula']}_{fecha_actual.strftime('%Y_%m_%d')}.xlsx"
    carpeta_descarga = "../static/downloads-excel"
    ruta_descarga = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), carpeta_descarga)

    if not os.path.exists(ruta_descarga):
        os.makedirs(ruta_descarga)
        # Dando permisos a la carpeta
        os.chmod(ruta_descarga, 0o755)

    ruta_archivo = os.path.join(ruta_descarga, archivoExcel)
    wb.save(ruta_archivo)

    # Enviar el archivo como respuesta HTTP
    return send_file(ruta_archivo, as_attachment=True)

def buscarAreaBD(search):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                querySQL = ("""
                        SELECT 
                            a.id_area,
                            a.nombre_area
                        FROM area AS a
                        WHERE a.nombre_area LIKE %s 
                        ORDER BY a.id_area DESC
                    """)
                search_pattern = f"%{search}%"  # Agregar "%" alrededor del término de búsqueda
                mycursor.execute(querySQL, (search_pattern,))
                resultado_busqueda = mycursor.fetchall()
                return resultado_busqueda

    except Exception as e:
        print(f"Ocurrió un error en def buscarEmpleadoBD: {e}")
        return []


# Lista de Usuarios creados
def lista_usuariosBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id_usuario, cedula, nombre_usuario, apellido_usuario, id_area, id_rol FROM usuarios"
                cursor.execute(querySQL,)
                usuariosBD = cursor.fetchall()
        return usuariosBD
    except Exception as e:
        print(f"Error en lista_usuariosBD : {e}")
        return []

def lista_areasBD():
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT id_area, nombre_area FROM area"
                cursor.execute(querySQL,)
                areasBD = cursor.fetchall()
        return areasBD
    except Exception as e:
        print(f"Error en lista_areas : {e}")
        return []

# Eliminar usuario
def eliminarUsuario(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM usuarios WHERE id_usuario=%s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarUsuario : {e}")
        return []    

def eliminarArea(id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                querySQL = "DELETE FROM area WHERE id_area=%s"
                cursor.execute(querySQL, (id,))
                conexion_MySQLdb.commit()
                resultado_eliminar = cursor.rowcount
        return resultado_eliminar
    except Exception as e:
        print(f"Error en eliminarArea : {e}")
        return []
    
def dataReportes():
    try:
        with connectionBD() as conexion_MYSQLdb:
            with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                querySQL = """
                SELECT a.id_acceso, u.cedula, a.fecha, r.nombre_area, a.clave 
                FROM accesos a 
                JOIN usuarios u 
                JOIN area r
                WHERE u.id_area = r.id_area AND u.id_usuario = a.id_usuario
                ORDER BY u.cedula, a.fecha DESC
                """
                cursor.execute(querySQL)
                reportes = cursor.fetchall()
        return reportes
    except Exception as e:
        print(f"Error en listaAccesos : {e}")
        return []

def lastAccessBD(id):
    try:
        with connectionBD() as conexion_MYSQLdb:
            with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT a.id_acceso, u.cedula, a.fecha, a.clave FROM accesos a JOIN usuarios u WHERE u.id_usuario = a.id_usuario AND u.cedula=%s ORDER BY a.fecha DESC LIMIT 1"
                cursor.execute(querySQL,(id,))
                reportes = cursor.fetchone()
                print(reportes)
        return reportes
    except Exception as e:
        print(f"Error en lastAcceso : {e}")
        return []
import random
import string
def crearClave():
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y dígitos
    longitud = 6  # Longitud de la clave

    clave = ''.join(random.choice(caracteres) for _ in range(longitud))
    print("La clave generada es:", clave)
    return clave
##GUARDAR CLAVES GENERADAS EN AUDITORIA
def guardarClaveAuditoria(clave_audi,id):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                    sql = "INSERT INTO accesos (fecha, clave, id_usuario) VALUES (NOW(),%s,%s)"
                    valores = (clave_audi,id)
                    mycursor.execute(sql, valores)
                    conexion_MySQLdb.commit()
                    resultado_insert = mycursor.rowcount
                    return resultado_insert 
        
    except Exception as e:
        return f'Se produjo un error en crear Clave: {str(e)}'
    
def lista_rolesBD():
    try:
        with connectionBD() as conexion_MYSQLdb:
            with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                querySQL = "SELECT * FROM rol"
                cursor.execute(querySQL)
                roles = cursor.fetchall()
                return roles
    except Exception as e:
        print(f"Error en select roles : {e}")
        return []
##CREAR AREA
def guardarArea(area_name):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                    sql = "INSERT INTO area (nombre_area) VALUES (%s)"
                    valores = (area_name,)
                    mycursor.execute(sql, valores)
                    conexion_MySQLdb.commit()
                    resultado_insert = mycursor.rowcount
                    return resultado_insert 
        
    except Exception as e:
        return f'Se produjo un error en crear Area: {str(e)}' 
    
##ACTUALIZAR AREA
def actualizarArea(area_id, area_name):
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as mycursor:
                sql = """UPDATE area SET nombre_area = %s WHERE id_area = %s"""
                valores = (area_name, area_id)
                mycursor.execute(sql, valores)
                conexion_MySQLdb.commit()
                resultado_update = mycursor.rowcount
                return resultado_update 
        
    except Exception as e:
        return f'Se produjo un error al actualizar el área: {str(e)}'
    
    #--------consulta de datos de los roles-----------:

    
#--------------------- metodo de graficas ----------------------
def obtenerroles():
    try:
        with connectionBD() as conexion_MYSQLdb:
            with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                query = """
                    SELECT r.nombre_rol
                    FROM rol r
                    ORDER BY r.nombre_rol ASC
                """
                cursor.execute(query)
                roles = cursor.fetchall()
        return roles
    except Exception as e:
        print(f"Error en obtenerroles: {e}")
        return []
    
#------------------------ area de graficas -----------------------
def obtener_areas():
    try:
        with connectionBD() as conexion_MYSQLdb:
            with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                query = """
                    SELECT nombre_area, numero_personas
                    FROM area
                    ORDER BY nombre_area ASC
                """
                cursor.execute(query)
                areas = cursor.fetchall()
        return areas
    except Exception as e:
        print(f"Error en obtener_areas: {e}")
        return []
    #------------------------ entrada de accesos --------------------------
def obtener_accesos_por_fecha(fecha_inicio, fecha_fin):
    try:
        with connectionBD() as conexion_MYSQLdb:
            with conexion_MYSQLdb.cursor(dictionary=True) as cursor:
                query = """
                    SELECT clave, COUNT(id_acceso) AS cantidad
                    FROM accesos
                    WHERE fecha BETWEEN %s AND %s
                    GROUP BY clave
                    ORDER BY clave ASC
                """
                cursor.execute(query, (fecha_inicio, fecha_fin))
                accesos = cursor.fetchall()
        return accesos
    except Exception as e:
        print(f"Error en obtener_accesos_por_fecha: {e}")
        return []
    


    
def lista_autoresBD():
    """
    Obtiene la lista de autores desde la base de datos.
    Consulta las columnas id_autor, nombre_completo y nacionalidad de la tabla 'autores'.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para seleccionar los datos necesarios de la tabla 'autores'
                querySQL = "SELECT id_autor, nombre_completo, nacionalidad FROM autores"
                cursor.execute(querySQL)
                autoresBD = cursor.fetchall()
        return autoresBD
    except Exception as e:
        # Imprime cualquier error que ocurra durante la conexión o la consulta a la base de datos
        print(f"Error en lista_autoresBD: {e}")
        return [] # Retorna una lista vacía en caso de error
    
def lista_categoriasBD():
    """
    Obtiene la lista de categorías desde la base de datos.
    Consulta las columnas id_categoria, nombre_categoria y descripcion de la tabla 'categorias'.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para seleccionar los datos necesarios de la tabla 'categorias'
                querySQL = "SELECT id_categoria, nombre_categoria, descripcion FROM categorias"
                cursor.execute(querySQL)
                categoriasBD = cursor.fetchall()
        return categoriasBD
    except Exception as e:
        # Imprime cualquier error que ocurra durante la conexión o la consulta a la base de datos
        print(f"Error en lista_categoriasBD: {e}")
        return [] # Retorna una lista vacía en caso de error
    
def lista_ubicacionesBD():
    """
    Obtiene la lista de ubicaciones desde la base de datos.
    Consulta las columnas id_ubicacion, nombre_ubicacion y referencia de la tabla 'ubicaciones'.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # Consulta SQL para seleccionar los datos necesarios de la tabla 'ubicaciones'
                querySQL = "SELECT id_ubicacion, nombre_ubicacion, referencia FROM ubicaciones"
                cursor.execute(querySQL)
                ubicacionesBD = cursor.fetchall()
        return ubicacionesBD
    except Exception as e:
        # Imprime cualquier error que ocurra durante la conexión o la consulta a la base de datos
        print(f"Error en lista_ubicacionesBD: {e}")
        return [] # Retorna una lista vacía en caso de error
    
def lista_librosBD():
    """
    Obtains the list of books from the database, including author, category,
    location, and calculated available quantity.
    """
    try:
        with connectionBD() as conexion_MySQLdb:
            with conexion_MySQLdb.cursor(dictionary=True) as cursor:
                # SQL query to select necessary data from multiple tables and calculate available quantity
                querySQL = """
                    SELECT
                        L.id_libro AS Codigo,
                        L.nombre_libro AS Titulo,
                        A.nombre_completo AS Autor_es,
                        U.nombre_ubicacion AS Ubicacion,
                        C.nombre_categoria AS Categoria,
                        L.stock_total - COALESCE(SUM(CASE WHEN D.id_devolucion IS NULL THEN DP.cantidad ELSE 0 END), 0) AS Cant_Disponibles
                    FROM
                        libros L
                    JOIN
                        autores A ON L.codigo_autor = A.id_autor
                    JOIN
                        categorias C ON L.id_categoria = C.id_categoria
                    JOIN
                        ubicaciones U ON L.id_ubicacion = U.id_ubicacion
                    LEFT JOIN 
                        detalle_prestamos DP ON L.id_libro = DP.id_libro
                    LEFT JOIN
                        prestamos P ON DP.id_prestamo = P.id_prestamo
                    LEFT JOIN
                        devoluciones D ON P.id_prestamo = D.id_prestamo
                    WHERE
                        L.estado_libro = 'activo'
                    GROUP BY
                        L.id_libro, L.nombre_libro, A.nombre_completo, U.nombre_ubicacion, C.nombre_categoria, L.stock_total
                    ORDER BY
                        L.id_libro;
                """
                cursor.execute(querySQL)
                librosBD = cursor.fetchall()
        return librosBD
    except Exception as e:
        # Prints any error that occurs during database connection or query
        print(f"Error en lista_librosBD: {e}")
        return [] # Returns an empty list in case of error