import streamlit as st
import plotly.express as px
import sqlite3 

st.title("CETAV")
st.title("Centro Tecnología y Artes Visuales")

         
st.header("Curso:Taller de Programación para Análisis de Datos III")
         
st.header("Proyecto Final: Base de Datos Sakila")         
         
st.header("Profesor: Nayib Vargas")

st.header("Estudiante:Joselyn Martínez")

st.write("""Objetivo: Analizar las películas según su rendimiento de alquileres, que 
         muestre el comportamiento de las categorías de películas, ventas por mes y
         distribución por tienda según la tendencia del lanzamiento de la película.""")

st.markdown("""
- Gráfico Barras: Conteo de Películas por Categoría
- Gráfico Circular: Promedio de 10 Principales Categorías
- Gráfico de Barras: Horizontales Top 10 Películas con Mayor Inversión
- Gráfico Barras: Análisis de Rentas del Staff
""")


