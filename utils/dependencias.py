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

#Me muestra la ruta de la base de datos donde estan almacenados como un dicionario 
data = cargar_datos(ruta)

#Tablas BBDD
category = data["category"]
film = data["film"]
store = data["store"]
payment = data["payment"]
customer = data["customer"]
rental = data["rental"]
inventory = data["inventory"]
film_category = data["film_category"]
staff = data["staff"]
city = data["city"]
country = data["country"]

#Filtro de las columnas
rentas = rental[['rental_id','rental_date','inventory_id','customer_id','staff_id']]
inventario = inventory[['inventory_id','film_id','store_id']]
peliculas = film[['film_id','title','release_year','length','rating']]
equipo_trabajo = staff[['staff_id','first_name']]
peliculas_categorizadas = film_category[['film_id','category_id']]
categorias = category[['category_id','name']]
pagos = payment[['payment_id','rental_id','amount']]


#Unir merges del DataFrame
merge_1 = rentas.merge(pagos,on='rental_id')
merge_2 = merge_1.merge(inventario,on='inventory_id')
merge_3 = merge_2.merge(peliculas,on='film_id')
merge_4 = merge_3.merge(equipo_trabajo,on='staff_id')
merge_5 = merge_4.merge(peliculas_categorizadas,on='film_id')
merge_6 = merge_5.merge(categorias,on='category_id')


#Creación de columnas mes.
merge_6['month'] = pd.to_datetime(merge_6['rental_date']).dt.month_name()

#Data Frame 
dataframe = merge_6

#Gráfico de Barras TOP 10
top_categorias = merge_6.groupby('name')['amount'].sum().sort_values(ascending=False).head(10).reset_index()

