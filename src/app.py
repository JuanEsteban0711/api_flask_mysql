from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app=Flask(__name__)

conexion=MySQL(app)

##### USUARIOS #####
# RUTA PARA REGISTRAR USUARIO
@app.route('/usuarios', methods=['POST'])
def registrar_usuario():
    try:
        cursor=conexion.connection.cursor()
        sql="""INSERT INTO usuario (id_usuario,nombre,domicilio,telefono) 
            VALUES({0},'{1}','{2}','{3}')""".format(request.json['id_usuario'],request.json['nombre'],request.json['domicilio'],request.json['telefono'])
        cursor.execute(sql)
        conexion.connection.commit() # Confirma el ingreso
        return jsonify({'mensaje':'Usuario registrado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error {}'.format(ex)})

# RUTA PARA ELIMINAR USUARIO
@app.route('/usuarios/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        cursor=conexion.connection.cursor()
        sql="DELETE FROM usuario WHERE id_usuario={}".format(id)
        cursor.execute(sql)
        conexion.connection.commit() # Confirma la eliminación
        conexion.connect.close()
        return jsonify({'mensaje':'Usuario eliminado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error {}'.format(ex)})

# RUTA PARA MODIFICAR USUARIO
@app.route('/usuarios/<id>', methods=['PUT'])
def modificar_usuario(id):
    try:
        cursor = conexion.connection.cursor()
        campos_actualizables = ['domicilio', 'telefono']
        cambios = {campo: request.json[campo] for campo in campos_actualizables if campo in request.json}
        
        if cambios:
            cambios_sql = ', '.join(["{}='{}'".format(campo, cambios[campo]) for campo in cambios])
            sql = "UPDATE Usuario SET {} WHERE id_usuario={}".format(cambios_sql, id)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la modificación
            return jsonify({'mensaje': 'Usuario actualizado correctamente.'})
        else:
            return jsonify({'mensaje': 'No se proporcionaron campos válidos para actualizar.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA CONSULTAR USUARIOS
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT nombre, domicilio, telefono FROM usuario"
        cursor.execute(sql)
        datos=cursor.fetchall()
        usuarios=[]
        for fila in datos:
            usuario={'nombre':fila[0],'domicilio':fila[1],'telefono':fila[2]}
            usuarios.append(usuario)
        return jsonify({'usuarios':usuarios,'mensaje':'Usuarios registrados.'})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})

# RUTA PARA CONSULTAR USUARIO INDIVIDUAL  
@app.route('/usuarios/<id>',methods=['GET'])
def leer_usuario(id):
    try:
        cursor=conexion.connection.cursor()
        sql='SELECT nombre, domicilio, telefono FROM usuario where id_usuario={0}'.format(id)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos!=None:
            usuario={'nombre':datos[0],'domicilio':datos[1],'telefono':datos[2]}
            return jsonify({'usuarios':usuario,'mensaje':'Usuarios registrados.'})
        else:
            return jsonify({'mensaje':'Usuario no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje':'Error'})
    
##### ESTADOS #####    
# RUTA PARA CONSULTAR ESTADOS
@app.route('/estados', methods=['GET'])
def listar_estados():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_estado, nombre FROM Estado"
        cursor.execute(sql)
        datos = cursor.fetchall()
        estados = [{'id_estado': fila[0], 'nombre': fila[1]} for fila in datos]
        return jsonify({'estados': estados})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# RUTA PARA CONSULTAR ESTADO INDIVIDUAL
@app.route('/estados/<id>', methods=['GET'])
def leer_estado(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT nombre FROM Estado WHERE id_estado={}".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            estado = {'id_estado': id, 'nombre': datos[0]}
            return jsonify({'estado': estado})
        else:
            return jsonify({'mensaje': 'Estado no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

##### SERVICIO #####
# RUTA PARA REGISTRAR SERVICIO
@app.route('/servicios', methods=['POST'])
def registrar_servicio():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Servicio (fecha, precio, id_usuario, id_estado) 
                 VALUES ('{0}', {1}, {2}, {3})""".format(request.json['fecha'], request.json['precio'], request.json['id_usuario'], request.json['id_estado'])
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma el ingreso
        return jsonify({'mensaje': 'Servicio registrado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA ELIMINAR SERVICIO
@app.route('/servicios/<id>', methods=['DELETE'])
def eliminar_servicio(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM Servicio WHERE id_servicio={}".format(id)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la eliminación
        return jsonify({'mensaje': 'Servicio eliminado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA MODIFICAR SERVICIO
@app.route('/servicios/<id>', methods=['PUT'])
def modificar_servicio(id):
    try:
        cursor = conexion.connection.cursor()
        campos_actualizables = ['fecha', 'precio', 'id_estado']
        cambios = {campo: request.json[campo] for campo in campos_actualizables if campo in request.json}
        
        if cambios:
            cambios_sql = ', '.join(["{}='{}'".format(campo, cambios[campo]) for campo in cambios])
            sql = "UPDATE Servicio SET {} WHERE id_servicio={}".format(cambios_sql, id)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la modificación
            return jsonify({'mensaje': 'Servicio actualizado correctamente.'})
        else:
            return jsonify({'mensaje': 'No se proporcionaron campos válidos para actualizar.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})
    
# RUTA PARA CONSULTAR SERVICIOS
@app.route('/servicios', methods=['GET'])
def listar_servicios():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT s.id_servicio, s.fecha, s.precio, s.id_usuario, e.nombre AS nombre_estado
                 FROM Servicio s
                 INNER JOIN Estado e ON s.id_estado = e.id_estado"""
        cursor.execute(sql)
        datos = cursor.fetchall()
        servicios = [{'id_servicio': fila[0], 'fecha': fila[1], 'precio': fila[2], 'id_usuario': fila[3], 'nombre_estado': fila[4]} for fila in datos]
        return jsonify({'servicios': servicios})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# RUTA PARA CONSULTAR SERVICIO INDIVIDUAL  
@app.route('/servicios/<id>', methods=['GET'])
def leer_servicio(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT s.fecha, s.precio, s.id_usuario, e.nombre AS nombre_estado
                 FROM Servicio s
                 INNER JOIN Estado e ON s.id_estado = e.id_estado
                 WHERE s.id_servicio={}""".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            servicio = {'id_servicio': id, 'fecha': datos[0], 'precio': datos[1], 'id_usuario': datos[2], 'nombre_estado': datos[3]}
            return jsonify({'servicio': servicio})
        else:
            return jsonify({'mensaje': 'Servicio no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

##### PRODUCTO #####
# RUTA PARA REGISTRAR PRODUCTO
@app.route('/productos', methods=['POST'])
def registrar_producto():
    try:
        cursor = conexion.connection.cursor()
        sql = "INSERT INTO Producto (nombre) VALUES ('{}')".format(request.json['nombre'])
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma el ingreso
        return jsonify({'mensaje': 'Producto registrado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA ELIMINAR PRODUCTO
@app.route('/productos/<id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM Producto WHERE id_producto={}".format(id)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la eliminación
        return jsonify({'mensaje': 'Producto eliminado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA MODIFICAR PRODUCTO
@app.route('/productos/<id>', methods=['PUT'])
def modificar_producto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "UPDATE Producto SET nombre='{}' WHERE id_producto={}".format(request.json['nombre'], id)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la modificación
        return jsonify({'mensaje': 'Producto actualizado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA CONSULTAR PRODUCTOS
@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT id_producto, nombre FROM Producto"
        cursor.execute(sql)
        datos = cursor.fetchall()
        productos = [{'id_producto': fila[0], 'nombre': fila[1]} for fila in datos]
        return jsonify({'productos': productos, 'mensaje': 'Productos registrados.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# RUTA PARA CONSULTAR PRODUCTO INDIVIDUAL  
@app.route('/productos/<id>', methods=['GET'])
def leer_producto(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT nombre FROM Producto WHERE id_producto={}".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            producto = {'id_producto': id, 'nombre': datos[0]}
            return jsonify({'producto': producto, 'mensaje': 'Producto encontrado.'})
        else:
            return jsonify({'mensaje': 'Producto no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

##### TRABAJO #####
# RUTA PARA REGISTRAR TRABAJO
@app.route('/trabajos', methods=['POST'])
def registrar_trabajo():
    try:
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO Trabajo (precio, ancho, alto, id_producto, id_servicio) 
                 VALUES ({}, {}, {}, {}, {})""".format(request.json['precio'], request.json['ancho'], request.json['alto'], request.json['id_producto'], request.json['id_servicio'])
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma el ingreso
        return jsonify({'mensaje': 'Trabajo registrado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA ELIMINAR TRABAJO
@app.route('/trabajos/<id>', methods=['DELETE'])
def eliminar_trabajo(id):
    try:
        cursor = conexion.connection.cursor()
        sql = "DELETE FROM Trabajo WHERE id_trabajo={}".format(id)
        cursor.execute(sql)
        conexion.connection.commit()  # Confirma la eliminación
        return jsonify({'mensaje': 'Trabajo eliminado correctamente.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})
    
# RUTA PARA MODIFICAR TRABAJO
@app.route('/trabajos/<id>', methods=['PUT'])
def modificar_trabajo(id):
    try:
        cursor = conexion.connection.cursor()
        campos_actualizables = ['precio', 'ancho', 'alto', 'id_producto']
        cambios = {campo: request.json[campo] for campo in campos_actualizables if campo in request.json}
        
        if cambios:
            cambios_sql = ', '.join(["{}={}".format(campo, cambios[campo]) for campo in cambios])
            sql = "UPDATE Trabajo SET {} WHERE id_trabajo={}".format(cambios_sql, id)
            cursor.execute(sql)
            conexion.connection.commit()  # Confirma la modificación
            return jsonify({'mensaje': 'Trabajo actualizado correctamente.'})
        else:
            return jsonify({'mensaje': 'No se proporcionaron campos válidos para actualizar.'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error {}'.format(ex)})

# RUTA PARA CONSULTAR TRABAJOS
@app.route('/trabajos', methods=['GET'])
def listar_trabajos():
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT id_trabajo, precio, ancho, alto, id_producto, id_servicio 
                 FROM Trabajo"""
        cursor.execute(sql)
        datos = cursor.fetchall()
        trabajos = [{'id_trabajo': fila[0], 'precio': fila[1], 'ancho': fila[2], 'alto': fila[3], 'id_producto': fila[4], 'id_servicio': fila[5]} for fila in datos]
        return jsonify({'trabajos': trabajos})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})

# RUTA PARA CONSULTAR TRABAJO INDIVIDUAL  
@app.route('/trabajos/<id>', methods=['GET'])
def leer_trabajo(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """SELECT precio, ancho, alto, id_producto, id_servicio 
                 FROM Trabajo 
                 WHERE id_trabajo={}""".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos is not None:
            trabajo = {'id_trabajo': id, 'precio': datos[0], 'ancho': datos[1], 'alto': datos[2], 'id_producto': datos[3], 'id_servicio': datos[4]}
            return jsonify({'trabajo': trabajo})
        else:
            return jsonify({'mensaje': 'Trabajo no encontrado'})
    except Exception as ex:
        return jsonify({'mensaje': 'Error'})



# FUNCIÓN PARA PÁGINA NO ENCONTRADA
def pagina_no_encotrada(error):
    return '<h1>La página que intentas buscar no existe ...</h1>',404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404,pagina_no_encotrada)
    app.run()