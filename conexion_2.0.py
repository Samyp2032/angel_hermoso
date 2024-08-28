import psycopg2
from psycopg2 import sql
from datetime import datetime


connection = psycopg2.connect(
        user="postgres",
        password="prueba123",
        host="localhost",
        port="5432",
        database="postgres"
)
        
cur = connection.cursor()
cursor = connection.cursor()

def llego_carro(connection):
    cursor = connection.cursor()
    try:

        print("¿Quieres reutilizar un proveedor existente o agregar uno nuevo?")
        print("1) Reutilizar existente")
        print("2) Agregar nuevo")
        opcion_proveedor = input("Elige una opción: ")
        
        if opcion_proveedor == '1':

            query_proveedores = "SELECT id_proveedor, nombres, apellido_paterno, apellido_materno FROM proveedor;"
            cursor.execute(query_proveedores)
            proveedores = cursor.fetchall()
            print("Proveedores existentes:")
            for proveedor in proveedores:
                print("ID:", proveedor[0], "- Nombre:", proveedor[1], proveedor[2], proveedor[3])
            

            id_proveedor = input("Elige el ID del proveedor: ")
        
        elif opcion_proveedor == '2':

                print("Datos del Proveedor")
                
                nombres = input("Nombre: ").upper()
                apellido_paterno = input("Apellido Paterno: ").upper()
                apellido_materno = input("Apellido Materno: ").upper()
                telefono = input("Teléfono: ")
                correo = input("Correo Electrónico: ").upper()

                query_proveedor = "INSERT INTO proveedor(nombres, apellido_paterno, apellido_materno, telefono, correo) VALUES (%s, %s, %s, %s, %s) RETURNING id_proveedor;"
                cursor.execute(query_proveedor, (nombres, apellido_paterno, apellido_materno, telefono, correo))
                id_proveedor = cursor.fetchone()[0]
                print("Proveedor agregado correctamente. ID:", id_proveedor)
                
                print("Datos del Proveedor")
                print("Se van a pedir por separado calle,colonia,num. exterior")
                calle = input("Calle: ").upper()
                colonia = input("Colonia: ").upper()
                num_exterior = input("Num. Exterior: ").upper()
                query_direccion = """INSERT INTO direccion_proveedor(calle, colonia, num_exterior) VALUES (%s, %s, %s) RETURNING id_direccion_proveedor;"""
                cursor.execute(query_direccion, (calle, colonia, num_exterior))
                id_direccion_proveedor = cursor.fetchone()[0]
                print("Dirección agregada correctamente. ID:", id_direccion_proveedor)

                print("Datos del Proveedor")

                print("Se van a pedir por separado ciudad,estado,pais")
                ciudad = input("Ciudad: ").upper()
                estado = input("Estado: ").upper()
                pais = input("Pais: ").upper()

                query_ciudad = """INSERT INTO ciudad(ciudad, estado, pais) VALUES (%s, %s, %s) RETURNING id_ciudad;"""
                cursor.execute(query_ciudad, (ciudad, estado, pais))
                id_ciudad = cursor.fetchone()[0]
                print("Ciudad agregada correctamente. ID:", id_ciudad)
                
                query_update_proveedor = "UPDATE proveedor SET id_direccion_proveedor = %s WHERE id_proveedor = %s;"
                cursor.execute(query_update_proveedor, (id_direccion_proveedor, id_proveedor))
                print("Proveedor actualizado con la direccion correctamente.")

                query_update_direccion_proveedor = "UPDATE direccion_proveedor SET id_ciudad = %s WHERE id_direccion_proveedor = %s;"
                cursor.execute(query_update_direccion_proveedor, (id_ciudad, id_direccion_proveedor))
                print("Direccion del proveedor actualizado con la ciudad correctamente.")
         

        print("Datos del Carro")
        marca = input("Marca: ").upper()
        modelo = input("Modelo: ").upper()
        año = input("Año: ").upper()
        precio = input("Precio: ").upper()
        kilometraje = input("Kilometraje: ").upper()
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query_carro = "INSERT INTO carros(id_proveedor, marca, modelo, año, precio, kilometraje, fecha_llegada) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_carro;"
        cursor.execute(query_carro, (id_proveedor, marca, modelo, año, precio, kilometraje, fecha_registro))
        id_carro = cursor.fetchone()[0]
        print("Carro agregado correctamente. ID:", id_carro)

        print("Datos del Carro")
        pantalla = input("Tiene pantalla true/false: ").lower()
        piel = input("Tiene piel true/false: ").lower()
        color = input("Color: ").upper()

        query_estilo = "INSERT INTO estilo(pantalla, piel, color) VALUES (%s, %s, %s) RETURNING id_estilo;"
        cursor.execute(query_estilo, (pantalla, piel, color))
        id_estilo = cursor.fetchone()[0]
        print("Estilo agregado correctamente. ID:", id_estilo)

        query_update_carro = "UPDATE carros SET id_estilo = %s WHERE id_carro = %s;"
        cursor.execute(query_update_carro, (id_estilo, id_carro))
        print("Carro actualizado con el estilo correctamente.")
        


        connection.commit()
                        
    except Exception as e:
        connection.rollback()
        print("Error:", e)
                                
def llego_cliente(connection):      
        cursor = connection.cursor()
        print("Buenos dias estos son los carros que tenemos: ")


        query_mostrar_carros = """SELECT * FROM carros WHERE vendido IS NULL; """
        cursor.execute(query_mostrar_carros)
        carros = cursor.fetchall()

        for carro in carros:
                print("ID:", carro[0])
                print("Marca:", carro[1])
                print("Modelo:", carro[2])
                print("Año:", carro[3])
                print("Precio:", carro[4])
                print("Kilometraje:", carro[7])
                print("------------------------")

        while True:
                respuesta = input("Le interesa alguno? (si/no): ").strip().lower()
                if respuesta == 'si':
                        ID = input("Pon su id: ").strip()

                        print("Datos del Cliente")
                        nombres_cliente = input("Dame todos tus Nombres(No apellidos): ").strip().upper()
                        apellido_paterno_cliente = input("Apellido Paterno: ").strip().upper()
                        apellido_materno_cliente = input("Apellido Materno: ").strip().upper()
                        telefono_cliente = input("Telefono (###-###-####): ").strip()
                        correo_cliente = input("Correo Electrónico: ").strip().upper()
                        curp_cliente = input("Curp (formato: 18 valores): ").strip()
                        sexo_cliente = input("Genero: ").strip().upper()

                        query_cliente = """
                        INSERT INTO clientes(nombres, apellido_paterno, apellido_materno, telefono, correo, curp, sexo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_cliente;
                        """
                        cursor.execute(query_cliente, (nombres_cliente, apellido_paterno_cliente, apellido_materno_cliente, telefono_cliente, correo_cliente, curp_cliente, sexo_cliente))
                        id_cliente = cursor.fetchone()[0]
                        
                        print("Datos del cliente")
                        print("Se van a pedir por separado calle,colonia,num. exterior")
                        calle = input("Calle: ").upper()
                        colonia = input("Colonia: ").upper()
                        num_exterior = input("Num. Exterior: ").upper()

                        query_direccion_empleado = """INSERT INTO direccion(calle, colonia, num_exterior) VALUES (%s, %s, %s) RETURNING id_direccion;"""
                        cursor.execute(query_direccion_empleado, (calle, colonia, num_exterior))
                        id_direccion_clientes = cursor.fetchone()[0]
                        print("Dirección agregada correctamente. ID:", id_direccion_clientes)

                        print("Datos del Cliente")
                        print("Se van a pedir por separado ciudad,estado,pais")
                        ciudad = input("Ciudad: ").upper()
                        estado = input("Estado: ").upper()
                        pais = input("Pais: ").upper()

                        query_ciudad = """INSERT INTO ciudad(ciudad, estado, pais) VALUES (%s, %s, %s) RETURNING id_ciudad;"""
                        cursor.execute(query_ciudad, (ciudad, estado, pais))
                        id_ciudad = cursor.fetchone()[0]
                        print("Ciudad agregada correctamente. ID:", id_ciudad)

                        query_update_direccion_empleados = "UPDATE direccion_empleados SET id_ciudad = %s WHERE id_direccion = %s;"
                        cursor.execute(query_update_direccion_empleados, (id_ciudad, id_direccion_clientes))
                        print("Direccion del empleado actualizado con la ciudad correctamente.")

                        query_mostrar_empleados = "SELECT * FROM empleado;"
                        cursor.execute(query_mostrar_empleados)
                        empleado = cursor.fetchall()

                        print("Empleados disponibles:")
                        for empleado in empleado:
                                print("ID:", empleado[13])
                                print("Nombre:", empleado[4])
                                print("Apellido Paterno:", empleado[5])
                                print("Apellido Materno:", empleado[6])
                                print("------------------------")

                                id_empleado = input("ID del empleado que realiza la venta: ").strip()
                                fecha_venta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                pago_completo = input("Pago completo true/false: ").lower()
                                
                                query_venta = """ INSERT INTO ventas(id_cliente, id_carro, id_empleado, fecha_venta, pago_completo)VALUES (%s, %s, %s, %s, %s ) RETURNING id_venta;"""
                                cursor.execute(query_venta, (id_cliente, ID, id_empleado,fecha_venta,pago_completo))
                                id_venta = cursor.fetchone()[0]

                                query_update_carro = """UPDATE carros SET fecha_vendido = CURRENT_TIMESTAMP, vendido = TRUE    WHERE id_carro = %s;"""
                                cursor.execute(query_update_carro, (ID,))



                                connection.commit() 
                                print("Cliente agregado correctamente. ID:", id_cliente)
                                print("Venta registrada correctamente. ID Venta:", id_venta)
                                break  
                        

                elif respuesta == 'no':
                        print("Gracias por su tiempo.")
                        break

                else:
                        print("Elección no válida. Por favor, elige una opción si/no.")

def nuevo_empleado(connection):
        try:
                print("Datos del Empleado")
                nombres_empleado = input("Dame todos tus Nombres(No apellidos): ").upper()
                apellido_paterno_empleado  = input("Apellido Paterno: ").upper()
                apellido_materno_empleado  = input("Apellido Materno: ").upper()
                telefono_empleado  = input("Teléfono (###-###-####): ")
                salario_empleado  = input("Salario: ")
                correo_empleado  = input("Correo Electrónico: ").upper()
                posicion_empleado = input("Cargo: ").upper()
                sexo_empleado = input("Genero: ").upper()
                curp_empleado = input("Curp (formato: 18 valores): ").upper()
                rfc_empleado = input("RFC(formato: 12 valores fisico y 13 si eres moral): ").upper()
                fecha_registro_empleado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                query_empleado = "INSERT INTO empleado(nombres, apellido_paterno, apellido_materno, telefono, salario, correo, posicion, sexo, curp, rfc, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_empleado;"
                cursor.execute(query_empleado, (nombres_empleado, apellido_paterno_empleado, apellido_materno_empleado, telefono_empleado, salario_empleado, correo_empleado, posicion_empleado, sexo_empleado, curp_empleado, rfc_empleado, fecha_registro_empleado))
                id_empleado = cursor.fetchone()[0]
                print("Proveedor agregado correctamente. ID:", id_empleado)
                
                print("Datos del empleado")
                print("Se van a pedir por separado calle,colonia,num. exterior")
                calle = input("Calle: ").upper()
                colonia = input("Colonia: ").upper()
                num_exterior = input("Num. Exterior: ").upper()

                query_direccion_empleado = """INSERT INTO direccion_empleados(calle, colonia, num_exterior) VALUES (%s, %s, %s) RETURNING id_direccion_empleados;"""
                cursor.execute(query_direccion_empleado, (calle, colonia, num_exterior))
                id_direccion_empleados = cursor.fetchone()[0]
                print("Dirección agregada correctamente. ID:", id_direccion_empleados)

                print("Datos del Empleado")
                print("Se van a pedir por separado ciudad,estado,pais")
                ciudad = input("Ciudad: ").upper()
                estado = input("Estado: ").upper()
                pais = input("Pais: ").upper()

                query_ciudad = """INSERT INTO ciudad(ciudad, estado, pais) VALUES (%s, %s, %s) RETURNING id_ciudad;"""
                cursor.execute(query_ciudad, (ciudad, estado, pais))
                id_ciudad = cursor.fetchone()[0]
                print("Ciudad agregada correctamente. ID:", id_ciudad)

                query_update_direccion_empleados = "UPDATE direccion_empleados SET id_ciudad = %s WHERE id_direccion_empleados = %s;"
                cursor.execute(query_update_direccion_empleados, (id_ciudad, id_direccion_empleados))
                print("Direccion del empleado actualizado con la ciudad correctamente.")
                
                print("Datos del Empleado")
                dia_empleado = input("Dia en que nacio: ").upper()
                mes_empleado = input("Mes en que nacio: ").upper()
                año_empleado = input("Año en que nacio: ").upper()
                
                query_nacimiento_empleado = """INSERT INTO fecha_nacimiento(dia, mes, año) VALUES (%s, %s, %s) RETURNING id_nacimiento;"""
                cursor.execute(query_nacimiento_empleado, (dia_empleado, mes_empleado, año_empleado))
                id_nacimiento = cursor.fetchone()[0]
                print("Ciudad agregada correctamente. ID:", id_nacimiento)
                
                query_update_empleado = "UPDATE empleado SET id_direccion_empleados = %s, id_nacimiento = %s WHERE id_empleado = %s;"
                cursor.execute(query_update_empleado, (id_direccion_empleados, id_nacimiento, id_empleado))
                print("Empleado actualizado con la direccion correctamente.")

                connection.commit()
        
        except Exception as e:
                connection.rollback()
                print("Error:", e)

def consultas_join(connection):
    cursor = connection.cursor()
    print("¿Qué consulta deseas realizar?")
    print("1) Mostrar carros con su proveedor")
    print("2) Mostrar ventas con detalles de clientes y empleados")
    print("3) Mostrar ventas completadas con detalles de clientes, empleados y carros")
    print("4) Mostrar total de ventas por modelo de carro")
    print("5) Mostrar carros con su estilo")
    print("6) Mostrar empleados con su dirección y ciudad")


    opcion = input("Elige una opción: ")

    if opcion == '1':
        query_carros_proveedores = """
        SELECT c.id_carro, c.marca, c.modelo, p.nombres, p.apellido_paterno, p.apellido_materno
        FROM carros c
        JOIN proveedor p ON c.id_proveedor = p.id_proveedor;
        """
        cursor.execute(query_carros_proveedores)
        resultados = cursor.fetchall()
        print("Carros con su proveedor:")
        for resultado in resultados:
            print(f"ID Carro: {resultado[0]}, Marca: {resultado[1]}, Modelo: {resultado[2]}, Proveedor: {resultado[3]} {resultado[4]} {resultado[5]}")
    
    elif opcion == '2':
        query_ventas_detalles = """
        SELECT v.id_venta, c.nombres, c.apellido_paterno, c.apellido_materno, e.nombres, e.apellido_paterno, e.apellido_materno, ca.marca, ca.modelo
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN empleado e ON v.id_empleado = e.id_empleado
        JOIN carros ca ON v.id_carro = ca.id_carro;
        """
        cursor.execute(query_ventas_detalles)
        resultados = cursor.fetchall()
        print("Ventas con detalles de clientes y empleados:")
        for resultado in resultados:
            print(f"ID Venta: {resultado[0]}, Cliente: {resultado[1]} {resultado[2]} {resultado[3]}, Empleado: {resultado[4]} {resultado[5]} {resultado[6]}, Carro: {resultado[7]} {resultado[8]}")

    elif opcion == '3':
        query_ventas_completadas = """
        SELECT v.id_venta, c.nombres, c.apellido_paterno, c.apellido_materno, e.nombres, e.apellido_paterno, e.apellido_materno, ca.marca, ca.modelo
        FROM ventas v
        JOIN clientes c ON v.id_cliente = c.id_cliente
        JOIN empleado e ON v.id_empleado = e.id_empleado
        JOIN carros ca ON v.id_carro = ca.id_carro
        WHERE v.pago_completo = true;
        """
        cursor.execute(query_ventas_completadas)
        resultados = cursor.fetchall()
        print("Ventas completadas con detalles de clientes, empleados y carros:")
        for resultado in resultados:
            print(f"ID Venta: {resultado[0]}, Cliente: {resultado[1]} {resultado[2]} {resultado[3]}, Empleado: {resultado[4]} {resultado[5]} {resultado[6]}, Carro: {resultado[7]} {resultado[8]}")
    
    elif opcion == '4':
        query_total_ventas_por_modelo = """
        SELECT ca.modelo, COUNT(v.id_venta) AS total_ventas
        FROM ventas v
        JOIN carros ca ON v.id_carro = ca.id_carro
        GROUP BY ca.modelo;
        """
        cursor.execute(query_total_ventas_por_modelo)
        resultados = cursor.fetchall()
        print("Total de ventas por modelo de carro:")
        for resultado in resultados:
            print(f"Modelo: {resultado[0]}, Total de Ventas: {resultado[1]}")
    elif opcion == '5':
        # Consulta para mostrar carros con su estilo
        query_carros_estilo = """
        SELECT c.id_carro, c.marca, c.modelo, e.pantalla, e.piel, e.color
        FROM carros c
        JOIN estilo e ON c.id_estilo = e.id_estilo;
        """
        cursor.execute(query_carros_estilo)
        resultados = cursor.fetchall()
        print("Carros con su estilo:")
        for resultado in resultados:
            print(f"ID Carro: {resultado[0]}, Marca: {resultado[1]}, Modelo: {resultado[2]}, Pantalla: {resultado[3]}, Piel: {resultado[4]}, Color: {resultado[5]}")


    elif opcion == '6':
        # Consulta para mostrar empleados con su dirección y ciudad
        query_empleados_direccion_ciudad = """
        SELECT e.id_empleado, e.nombres, e.apellido_paterno, e.apellido_materno, 
               d.calle, d.colonia, d.num_exterior, 
               ci.ciudad, ci.estado, ci.pais
        FROM empleado e
        JOIN direccion_empleados d ON e.id_direccion_empleados = d.id_direccion_empleados
        JOIN ciudad ci ON d.id_ciudad = ci.id_ciudad;
        """
        cursor.execute(query_empleados_direccion_ciudad)
        resultados = cursor.fetchall()
        print("Empleados con su dirección y ciudad:")
        for resultado in resultados:
            print(f"ID Empleado: {resultado[0]}, Nombre: {resultado[1]} {resultado[2]} {resultado[3]}, "
                  f"Dirección: {resultado[4]} {resultado[5]} {resultado[6]}, "
                  f"Ciudad: {resultado[7]}, Estado: {resultado[8]}, País: {resultado[9]}")
    
    
    else:
        print("Opción no válida.")

def eliminar_carro(connection):
    cursor = connection.cursor()
    try:
        # Mostrar carros existentes
        query_carros = """SELECT * FROM carros WHERE vendido IS NULL; """
        cursor.execute(query_carros)
        carros = cursor.fetchall()
        print("Carros existentes:")
        for carro in carros:
            print("ID:", carro[0], "- Marca:", carro[1], "- Modelo:", carro[2])
        
        # Seleccionar carro a eliminar
        id_carro = input("Elige el ID del carro a eliminar: ")
        
        # Eliminar el carro
        query_eliminar_carro = "DELETE FROM carros WHERE id_carro = %s;"
        cursor.execute(query_eliminar_carro, (id_carro,))
        connection.commit()
        print("Carro eliminado correctamente.")
        
    except Exception as e:
        connection.rollback()
        print("Error:", e)

def eliminar_empleado(connection):
    cursor = connection.cursor()
    try:
        # Mostrar empleados existentes
        query_empleados = "SELECT id_empleado, nombres, apellido_paterno, apellido_materno FROM empleado;"
        cursor.execute(query_empleados)
        empleados = cursor.fetchall()
        print("Empleados existentes:")
        for empleado in empleados:
            print("ID:", empleado[0], "- Nombre:", empleado[1], empleado[2], empleado[3])
        
        # Seleccionar empleado a eliminar
        id_empleado = input("Elige el ID del empleado a eliminar: ")

        # Obtener id_direccion asociado
        query_direccion_empleado = "SELECT id_direccion_empleados FROM empleado WHERE id_empleado = %s;"
        cursor.execute(query_direccion_empleado, (id_empleado,))
        id_direccion_empleados = cursor.fetchone()
        
        query_nacimiento = "SELECT id_nacimiento FROM empleado WHERE id_empleado = %s;"
        cursor.execute(query_nacimiento, (id_empleado,))
        id_nacimiento = cursor.fetchone()
        
        query_ciudad = "SELECT id_ciudad FROM direccion_empleados WHERE id_direccion_empleados = %s;"
        cursor.execute(query_ciudad, (id_direccion_empleados,))
        id_ciudad = cursor.fetchone()
        
        # Eliminar empleado
        query_eliminar_empleado = "DELETE FROM empleado WHERE id_empleado = %s;"
        cursor.execute(query_eliminar_empleado, (id_empleado,))
        
         # Eliminar dirección asociada
        if id_direccion_empleados:
            query_eliminar_direccion = "DELETE FROM direccion_empleados WHERE id_direccion_empleados = %s;"
            cursor.execute(query_eliminar_direccion, (id_direccion_empleados,))
        
        # Eliminar nacimiento asociado
        if id_nacimiento:
            query_eliminar_nacimiento = "DELETE FROM fecha_nacimiento WHERE id_nacimiento = %s;"
            cursor.execute(query_eliminar_nacimiento, (id_nacimiento,))
        
        # Eliminar ciudad asociada
        if id_ciudad:
            query_eliminar_ciudad = "DELETE FROM ciudad WHERE id_ciudad = %s;"
            cursor.execute(query_eliminar_ciudad, (id_ciudad,))
        



        
        connection.commit()
        print("Empleado y todas sus referencias eliminados correctamente.")
    except Exception as e:
        connection.rollback()
        print("Error:", e)
        
while True:
    print("\nElige qué quieres hacer")
    print("1) Llego carro")
    print("2) Llego cliente")
    print("3) Nuevo empleado")
    print("4) Consultas JOIN")
    print("5) Eliminar carro")
    print("6) Eliminar empleado")
    print("7) Salir")
    
    choice = input("Introduce tu elección: ")

    if choice == '1':
        llego_carro(connection)
    elif choice == '2':
        llego_cliente(connection)
    elif choice == '3':
        nuevo_empleado(connection)
    elif choice == '4':
        consultas_join(connection)
    elif choice == '5':
        eliminar_carro(connection)
    elif choice == '6':
        eliminar_empleado(connection)
    elif choice == '7':
        break
    else:
        print("Elección no válida. Por favor, elige una opción del 1 al 7.")

connection.close()    