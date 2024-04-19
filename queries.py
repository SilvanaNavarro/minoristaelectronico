    
import mysql.connector
from mysql.connector import Error

def querie(consulta):
    try:
        conexion = mysql.connector.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'valkiria123',
            db= 'minoristaelectronicos'
        )
        if conexion.is_connected():
            cursor = conexion.cursor()
            cursor.execute(consulta)   
            resultado=cursor.fetchall()
            
            for fila in resultado:
                resp=str(fila[0])
                for i in range(1,len(fila)):
                    resp=resp+','+str(fila[i])
                print(resp)
            cursor.close()   
            
    except Error as ex:
        print('Error al conectar base de datos: {}'.format(ex))
    finally:
        if conexion.is_connected():
            conexion.close()


total_ventas='SELECT SUM(ventas.cantidad*productos.precio) AS total_ventas FROM ventas INNER JOIN productos ON productos.id=ventas.id_producto'
print('total ventas:')
querie(total_ventas)
print()

total_unidades='SELECT SUM(ventas.cantidad) AS total_cantidad FROM ventas'
print('total unidades vendidas:')
querie(total_unidades)
print()

mas_vendidos='SELECT productos.nombre AS producto, SUM(ventas.cantidad*productos.precio) AS total_ventas, SUM(ventas.cantidad) AS cantidad FROM ventas INNER JOIN productos ON productos.id=ventas.id_producto GROUP BY producto ORDER BY total_ventas DESC LIMIT 10'
print('Top 10 productos más vendidos: (producto,total ventas, cantidad)')
querie(mas_vendidos)
print()

promedio_mensual='SELECT ROUND(AVG(ventas.cantidad * productos.precio),0) as promedio, EXTRACT(MONTH FROM ventas.fecha) AS num_mes FROM  ventas INNER JOIN productos ON productos.id=ventas.id_producto GROUP BY num_mes ORDER BY num_mes'
print('Promedio de ventas por mes: (promedio de ventas, mes(numero))')
querie(promedio_mensual)
print()

promedio_diario='SELECT DATE_FORMAT(ventas.fecha,"%Y-%m-%d") AS dia,COUNT(ventas.id) AS cantidad_transacciones,ROUND(AVG(productos.precio*ventas.cantidad),0) AS promedio_venta FROM ventas JOIN productos ON productos.id=ventas.id_producto GROUP BY dia ORDER BY dia ASC LIMIT 5;'
print('Promedio de ventas por día (5 muestras): (fecha, cantidad transacciones, promedio de venta diaria)')
querie(promedio_diario)
print()

pref_genero='SELECT clientes.genero, productos.nombre, SUM(ventas.cantidad) AS cantidad, cantidad*productos.precio AS total_ventas FROM ventas INNER JOIN clientes ON ventas.id_cliente=clientes.id INNER JOIN productos ON productos.id=ventas.id_producto GROUP BY productos.nombre, clientes.genero,total_ventas ORDER BY total_ventas DESC LIMIT 10'
print('Los más preferidos por género de clientes (10 muestras): (género, producto, cantidad vendida, total vendido)')
querie(pref_genero)

