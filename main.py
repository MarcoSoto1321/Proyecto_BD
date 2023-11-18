from flask import Flask, request, render_template
import psycopg2
import base64
from io import BytesIO
from PIL import Image
import os

host = "localhost"
database = "restaurante_bd"
user = "postgres"
password = "postgres"

app = Flask(__name__)

#======================================================
#============Funciones para enlaces====================
#=====================================================

datos_empleado = []

# En todos los casos, sería bueno agregar una ventana de alerta cuando suceda un error

#para definir la ruta base en la que buscar "@app.route"

@app.route('/')
def inicio():
  datos_empleado.clear()
  return render_template('index.html')


@app.route('/agregarEmpleado')
def agregarEmpleado():
  return render_template('agregar-empleado.html')


@app.route('/mostrarEmpleado')
def mostrarEmpleado():
  return render_template('mostrar-empleado.html')

# ESTOY LO ESTOY PROBANDO YO
@app.route('/obtenerInfoEmpleado')
def obtenerInfoEmpleado():
  # Se tiene que eliminar la imagen para no tener basura en el html
  ruta_del_archivo = 'static/images/empleado.jpg'
  if os.path.exists(ruta_del_archivo):
    try:
      os.remove(ruta_del_archivo)
      print(f'Archivo {ruta_del_archivo} borrado con éxito.')
    except OSError as e:
      print(f'Error al borrar el archivo: {e}')
  return render_template('obtener-info-empleado.html')

@app.route('/agregarCliente')
def agregarCliente():
  return render_template('agregar-cliente.html')

# Para mostrar la información de las ordenes
@app.route('/obtenerInformacion')
def obtenerInformacion():
  return render_template('info-ordenes.html')

# Mostrar el formulario de registro de una categoría
@app.route('/agregarCategoria')
def agregarCategoria():
  return render_template('agregar-categoria.html')

# Mostrar el formulario para registrar dependientes
@app.route('/agregarDependiente')
def agregarDependiente():
  return render_template('agregar-dependiente.html')

@app.route('/agregarProducto')
def agregarProducto():
  return render_template('agregar-producto.html')

@app.route('/ventasPorFecha')
def ventasPorFecha():
  return render_template('ventas-por-fecha.html')

@app.route('/ventasPorFechas')
def ventasPorFechas():
  return render_template('ventas-por-fechas.html')

@app.route('/agregarOrden')
def agregarOrden():
  return render_template('agregar-orden.html')

# TERMINAR DE IMPLEMENTAR EL AGREGAR EMPLEADO
#Valor "action" de la encuesta que llena el formulario
@app.route('/agregar_empleado', methods=['POST'])
def agregar_empleado():
  if request.method == 'POST':
    #Variables para ingresar a la base
    ruta_destino = ""
    rfc = request.form['rfc']
    nombre = request.form['nombre']
    appat = request.form['appat']
    apmat = request.form['apmat']
    fechanac = request.form['fechanac']
    edad = request.form['edad']
    if 'foto' in request.files:
        imagen = request.files['foto']
        # Guardar la imagen en el sistema de archivos
        ruta_destino = 'static/images/' + imagen.filename
        imagen.save(ruta_destino)
    else:
      print("No se recibió ninguna imagen")
      return "ERROR: No se adjuntó una imagen de empleado"
        # Puedes hacer más operaciones con la imagen si es necesario
    # Aquí puedes procesar los datos y realizar acciones adicionales
    # ...
    with open(ruta_destino, 'rb') as file:
        imagen_bytes = file.read()
        # Insertar la imagen en la base de datos

    estado = request.form['estado']
    cp = request.form['cp']
    colonia = request.form['colonia']
    calle = request.form['calle']
    numero = request.form['numero']
    descripcion = request.form['descripcion']
    rol = request.form['puesto']

    # En este punto ya se tiene toda la información
    # Una vez obtenido esto, es necesario eliminar el archivo
    try:
      os.remove(ruta_destino)
      print(f'Archivo {ruta_destino} borrado con éxito.')
    except OSError as e:
      print(f'Error al borrar el archivo: {e}')


    # Hasta este punto va bien
    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = "CALL restaurante.agregar_empleado(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      #Los datos son las variables declaradas
      data = (rfc, nombre, appat, apmat, fechanac, edad, estado, cp, colonia,
              calle, numero, rol, descripcion, psycopg2.Binary(imagen_bytes))
      # Falta la parte del teléfono
      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      connection.commit()
      cur.close()
      connection.close()

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-empleado.html', msg='Formulario enviado')
  else:
    return render_template('agregar-empleado.html',
                           msg='Metodo HTTP incorrecto')

# REVISAR
def agregar_producto_orden():
  if request.method == 'POST':
    #Variables para ingresar a la base
    folio_orden = request.form['']
    id_producto_agregado = request.form['']
    cantidad = request.form['']

    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres

      instruction = "DO $$ BEGIN PERFORM restaurante.agregar_producto_orden(%s,%s,%s); END $$;"
      #Los datos son las variables declaradas
      data = (folio_orden,id_producto_agregado,cantidad)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      connection.commit()

      cur.close() 
      connection.close()

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-empleado.html', msg='Formulario enviado')
  else:
    return render_template('agregar-empleado.html',
                           msg='Metodo HTTP incorrecto')


@app.route('/info_ordenes', methods=['POST'])
def info_ordenes():
  if request.method == 'POST':
    #Variables para ingresar a la base
    id_empleado = request.form['id_empleado']

    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = "SELECT * FROM restaurante.info_ordenes(%s)"
      #Los datos son las variables declaradas
      data = (id_empleado)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      records = cur.fetchall()    
      # Se tiene la información de las órdenes que ha tomado el empleado.
      for record in records:
          print(record)
      cur.close()
      connection.close()
      numero, total = records[0]
      # Se renderiza la página con los valores
      return render_template('info-ordenes.html', msg='Se obtuvieron los siguientes datos para el empleado: ' ,numero=numero,total=total,datos=records)


    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)
      # En este caso se deberá de mandar una alerta con el error
      if str(error) == 'string index out of range':
        return render_template('info-ordenes.html')
      # Encuentra la posición de la palabra clave
      msg=str(error)
      posicion_palabra_clave = msg.find('CONTEXT')

      # Verifica si la palabra clave está presente
      if posicion_palabra_clave != -1:
          # Extrae la parte de la cadena antes de la palabra clave
          msg = msg[:posicion_palabra_clave]
      else:
          # La palabra clave no se encontró, mantener la cadena original
          print(msg)
      return render_template('info-ordenes.html', msg=msg, tipo='error')

  else:
    return render_template('info-ordenes.html',
                           msg='Metodo HTTP incorrecto')


# FALTA IMPLEMENTAR LA PARTE DE MOSTRAR LA INFORMACIÓN BIEN. IGUALMENTE, FALTA CONSIDERAR CUANDO VARIOS EMPLEADOS SE LLAMAN IGUAL
@app.route('/obtener_info_empleado', methods=['POST'])
def obtener_info_empleados():
  if request.method == 'POST':
    #Variables para ingresar a la base
    nombre_empleado = request.form['nombre']

    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = f"SELECT * FROM restaurante.obtener_info_empleados(\'{nombre_empleado}\');"
      #Los datos son las variables declaradas
      #cur.execute para ejecutar la instrucción
      cur.execute(instruction)
      # Recuperar los resultados de la consulta
      records = cur.fetchall()    
      # Se tiene el registro de todos los empleados que tienen dicho nombre. En caso de que haya más empleados
      # habrá que ver cómo seleccionar al deseado. Estaría bien poner una lista de los nombres y datos de cada uno, y mediante la selección
      # de alguno, se muestra su información y su imagen.
      for record in enumerate(records):
          datos_empleado.append(record)
      # Veamos el caso en que haya un solo empleado
      if len(records) == 1:
        imagen = records[0][13] # REVISAR LA RECUPERACIÓN DE LA IMAGEN
        output_image_path = 'static/images/empleado.jpg'
        datos_empleado.clear()
        # Crear una imagen desde los bytes
        image = Image.open(BytesIO(imagen))
        # Guardar la imagen
        image.save(output_image_path)
        # En este punto ya es posible utilizar la imagen
        cur.close()
        connection.close()
        return render_template('mostrar-info-empleado.html',ruta_imagen=output_image_path,datos=records[0])
      else:
        # Debemos mostrar la información de los empleados con el mismo nombre con la opción de seleccionar alguno
        cur.close()
        connection.close()
        # En datos_empleado se tienen todos los registros de los trabajadores. Estos los mandaremos para que se seleccione el deseado
        return render_template('obtener-info-empleado.html',datos=datos_empleado)

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)
    return render_template('obtener-info-empleado.html')
    # return render_template('mostrar-empleado.html', empleados = data)
  else:
    return render_template('obtener-info-empleado.html',
                           msg='Metodo HTTP incorrecto')

# En caso de múltiples registros, se deberá de obtener el seleccionado
@app.route('/empleado_seleccionado', methods=['POST'])
def empleado_seleccionado():
  # Se debe de procesar la información del empleado
  indice = int(request.form['seleccion'])
  empleado = datos_empleado[indice][1]
  print(empleado)
  # Nada más tenemos que ver cómo eliminar la información de la variable global
  datos_empleado.clear()
  # return render_template('mostrar-info-empleado.html')
  imagen = empleado[13]
  output_image_path = 'static/images/empleado.jpg'
  datos_empleado.clear()
  imagen = Image.open(BytesIO(imagen))
  # Guardar la imagen
  imagen.save(output_image_path)
  # En este punto ya es posible utilizar la imagen
  return render_template('mostrar-info-empleado.html',ruta_imagen=output_image_path,datos=empleado)


# Podemos comenzar a analizar esta parte
# Falta corregir y agregar HTML
@app.route('/productos_no_disponibles')
def productos_no_disponibles():
  try:
    #Parametros para coneccion a la base
    connection = psycopg2.connect(host=host,
                                  database=database,
                                  user=user,
                                  password=password)
    #/

    # Crear un cursor para ejecutar consultas
    cur = connection.cursor()

    #Instruccion a ejecutar en sintaxis postgres
    instruction = "SELECT * FROM restaurante.productos_no_disponibles();"
    #Los datos son las variables declaradas
    data = ()

    #cur.execute para ejecutar la instrucción
    cur.execute(instruction, data)
    # Recuperar los resultados de la consulta
    records = cur.fetchall()    
    # Records contiene los productos que no están disponibles
    for record in records:
        print(record)
    # En este caso se tienen los productos que no están disponibles dentro del record
    cur.close()
    connection.close()
  except (Exception, psycopg2.Error) as error:
    print("Error al conectarse a la base de datos:", error)

  # Se manda al html de productos-no-disponibles los platillos que no están disponibles, los cuales se deberán de mostrar
  return render_template('productos-no-disponibles.html', msg='Formulario enviado',platillos=records)

# Revisar la información que mandamos
@app.route('/ventas_por_fecha', methods=['POST'])
def ventas_por_fecha():
  if request.method == 'POST':
    fecha = request.form['fecha_inferior']
    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = f"SELECT * FROM restaurante.ventas_por_fecha(\'{fecha}\');"
      #Los datos son las variables declaradas
      data = (fecha)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      # Recuperar los resultados de la consulta
      records = cur.fetchall()    
      # Records contiene las ventas generadas en la fecha seleccionada
      for record in records:
          print(record)
      cur.close()
      connection.close()

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)
  else:
    return render_template('ventas-por-fecha.html', msg='Metodo HTTP incorrecto')  
  # Aquí debemos de renderizar las ventas generadas (parecido al de mesero)
  return render_template('ventas-por-fecha.html', msg='Formulario enviado')

@app.route('/ventas_por_fechas',methods=['POST'])
def ventas_por_fecha2():
    if request.method == 'POST':
      fechainferior = request.form['fecha_inferior']
      fechaSuperior = request.form['fecha_superior']
      try:
        #Parametros para coneccion a la base
        connection = psycopg2.connect(host=host,
                                      database=database,
                                      user=user,
                                      password=password)
        #/

        # Crear un cursor para ejecutar consultas
        cur = connection.cursor()

        #Instruccion a ejecutar en sintaxis postgres
        instruction = "SELECT * FROM restaurante.ventas_por_fecha(%s,%s);"
        #Los datos son las variables declaradas
        data = (fechainferior,fechaSuperior)

        #cur.execute para ejecutar la instrucción
        cur.execute(instruction, data)
        # Recuperar los resultados de la consulta
        records = cur.fetchall()    

        # Aquí se tienen las ventas dadas en el intervalo de fechas dado
        for record in records:
            print(record)

        connection.commit()
        cur.close()
        connection.close()


      except (Exception, psycopg2.Error) as error:
        print("Error al conectarse a la base de datos:", error)
    else:
      return render_template('ventas-por-fechas.html', msg='Metodo HTTP incorrecto')  
    return render_template('ventas-por-fechas.html', msg='Formulario enviado')


# Ya es posible agregar la categoría de forma adecuada
@app.route('/agregar_categoria', methods=['POST'])
def agregar_categoria():
  if request.method == 'POST':
    #Variables para ingresar a la base
    nombre = request.form['nombre']
    descripcion = request.form['desc']

    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = "CALL restaurante.agregar_categoria(%s,%s);"
      #Los datos son las variables declaradas
      data = (nombre,descripcion)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      connection.commit()
      cur.close()
      connection.close()
    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-categoria.html', msg='Formulario enviado')
  else:
    return render_template('agregar-categoria.html',
                           msg='Metodo HTTP incorrecto')

# REVISAR ESTA PARTE CON LA CUESTIÓN DE LA FACTURA
@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente(): # Revisar que empaten los nombres
  if request.method == 'POST':
    #Variables para ingresar a la base
    folio_orden = request.form['folio']
    rfc = request.form['rfc']
    nombre = request.form['nombre']
    appat = request.form['appat']
    apmat = request.form['apmat']
    fechanac = request.form['fechanac']
    estado = request.form['estado']
    cp = request.form['cp']
    colonia = request.form['colonia']
    calle = request.form['calle']
    numero = request.form['numero']
    email = request.form['email']
    razon_social = request.form['razon']

    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = "CALL restaurante.agregar_cliente(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s)"
      #Los datos son las variables declaradas
      data = (folio_orden,rfc, nombre, appat, apmat, fechanac, estado, cp, colonia,
              calle, numero, email,razon_social)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      connection.commit()

      cur.close()
      connection.close()

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-empleado.html', msg='Formulario enviado')
  else:
    return render_template('agregar-empleado.html',
                           msg='Metodo HTTP incorrecto')


# Esta parte ya la podemos implementar
@app.route('/agregar_dependiente',methods=['POST'])
def agregar_dependiente():
  if request.method == 'POST':
    #Variables para ingresar a la base
    curp = request.form['curp']
    nombre = request.form['nombre']
    appat = request.form['appat']
    apmat = request.form['apmat']
    parentesco = request.form['parent']
    num_empleado = request.form['num_emp']

    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = "CALL restaurante.agregar_dependiente(%s, %s,%s, %s,%s, %s);"
      #Los datos son las variables declaradas
      data = (curp,nombre,appat,apmat,parentesco,num_empleado)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      connection.commit()
      cur.close()
      connection.close()

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)
      # Ver cómo informar que no fue posible realizar la operación (Para todos los casos)

    return render_template('agregar-dependiente.html', msg='Formulario enviado')
  else:
    return render_template('agregar-dependiente.html',
                           msg='Metodo HTTP incorrecto')

# Primero se solicita el número del mesero --> Revisar este pedo
@app.route('/agregar_orden',methods=['POST'])
def agregar_orden():
  if request.method == 'POST':
    #Variables para ingresar a la base
    id_mesero = request.form['id_mesero']
    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = "CALL restaurante.agregar_orden(%s);"
      #Los datos son las variables declaradas
      data = (id_mesero)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      connection.commit()
      cur.close()
      connection.close()
    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-orden.html', msg='Formulario enviado')
  else:
    return render_template('agregar-orden.html',
                           msg='Metodo HTTP incorrecto')


@app.route('/agregar_producto',methods=['POST'])
def agregar_producto():
  if request.method == 'POST':
    #Variables para ingresar a la base
    nombre = request.form['nombre']
    descripcion = request.form['desc']
    precio = request.form['precio']
    disponibilidad = request.form['disp']
    receta = request.form['receta']
    id_categoria = request.form['id_cat']


    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cur = connection.cursor()

      #Instruccion a ejecutar en sintaxis postgres
      instruction = "CALL restaurante.agregar_producto(%s,%s,%s,%s,%s,%s)"
      #Los datos son las variables declaradas
      data = (nombre,descripcion,precio,disponibilidad,receta,id_categoria)

      #cur.execute para ejecutar la instrucción
      cur.execute(instruction, data)
      connection.commit()

      cur.close()
      connection.close()

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-producto.html', msg='Formulario enviado')
  else:
    return render_template('agregar-producto.html',
                           msg='Metodo HTTP incorrecto')


def generar_factura():
  if request.method == 'POST':
    #Variables para ingresar a la base
    folio_orden = request.form['']
    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(host=host,
                                    database=database,
                                    user=user,
                                    password=password)
      #/

      # Crear un cursor para ejecutar consultas
      cursor = connection.cursor()
      instruction = "SELECT * FROM restaurante.generar_factura(%s, 'Ref1', 'Ref2');"
      data = (folio_orden)
      # call a stored procedure
      cursor.execute(instruction,data)
      cursor.execute('FETCH ALL IN "Ref1";')
      tbl1 = cursor.fetchall()
      print(tbl1)
      cursor.execute('FETCH ALL IN "Ref2";')
      tbl2 = cursor.fetchall()
      print(tbl2)
      # Cerrar el cursor y la conexión
      cursor.close()
      connection.close()

    except (Exception, psycopg2.Error) as error:
      print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-empleado.html', msg='Formulario enviado')
  else:
    return render_template('agregar-empleado.html',
                           msg='Metodo HTTP incorrecto')

@app.route('/producto_mas_vendido',methods=['POST'])
def producto_mas_vendido():
  if request.method == 'POST':
    #Variables para ingresar a la base
    try:
        #Parametros para coneccion a la base
        connection = psycopg2.connect(host=host,
                                        database=database,
                                        user=user,
                                        password=password)
        #/

        # Crear un cursor para ejecutar consultas
        cur = connection.cursor()

        #Instruccion a ejecutar en sintaxis postgres
        instruction = "CALL restaurante.producto_mas_vendido();"

        #cur.execute para ejecutar la instrucción
        cur.execute(instruction)
        connection.commit()

        # Posteriormente es necesario obtener la vista para mostrar la información del platillo más vendido
        instruction = "SELECT * FROM restaurante.platillo_mas_vendido;"
        cur.execute(instruction)
        # En este caso se tiene la vista de las ventas. Puede darse el caso de que haya varios productos.

        records = cur.fetchall()    

        for record in records:
            print(record)
        cur.close()
        connection.close()
    except (Exception, psycopg2.Error) as error:
        print("Error al conectarse a la base de datos:", error)

    return render_template('agregar-empleado.html', msg='Formulario enviado')
  else:
    return render_template('agregar-empleado.html',
                          msg='Metodo HTTP incorrecto')

@app.route('/mostrar_empleado')
def mostrar_empleado():
    try:
      #Parametros para coneccion a la base
      connection = psycopg2.connect(
          host=host,
          database=database,
          user=user,
          password=password
      )
      cur = connection.cursor()
      instruction = "SELECT * FROM restaurante.empleado;"
      cur.execute(instruction)
      data = cur.fetchall()
    except (Exception, psycopg2.Error) as error:
            print("Error al conectarse a la base de datos:", error)
    return render_template('mostrar-empleado.html', empleados = data)

if __name__ == '__main__':
  app.run(debug=True)
