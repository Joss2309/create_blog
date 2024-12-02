import pandas as pd
import sqlite3
import os
import numpy as np

#Solicito la ruta donde voy mapear traer la base de datos
def mapear_datos(nombre_bd, formato): 
    carpeta = os.path.dirname(__file__)
    db_path = os.path.join(carpeta, '..', 'data', f'{nombre_bd}{formato}')
    return db_path

#Le solicito me traiga las tablas de la Base de datos y me lo guarde como dicionario
def cargar_datos(ruta_archivo):
    conn = sqlite3.connect(ruta_archivo)
    
    dataframes = {}
    
    tablas = pd.read_sql('SELECT name FROM sqlite_master WHERE type = "table"', conn)
    
    for tabla in tablas['name']:
        dataframes[tabla] = pd.read_sql(f'SELECT * FROM "{tabla}"', conn)
    
    conn.close()   
    
    return dataframes

#Le muestro la ruta para almacenar la base de datos
ruta = mapear_datos("sakila_master",".db")
#Me muestra la ruta de la base de datos
data = cargar_datos(ruta)

#Tabla de la BBDD
categorias = data["category"]
peliculas = data["film"]
tienda = data["store"]
pagos = data["payment"]
clientes = data["customer"]
rentas = data["rental"]
inventario = data["inventory"]
peliculas_categorizadas = data["film_category"]
equipo_trabajo = data["staff"]
ciudad = data["city"]
pais = data["country"]

datos_pelis = categorias.merge(peliculas_categorizadas, on="category_id" )

datos_pelis


