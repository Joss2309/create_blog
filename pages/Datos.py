import sys 
from pathlib import Path 
import streamlit as st 
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go 
from plotly._subplots import make_subplots

#Cargar la base de datos SQLITE
root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import *


# Conversión de la columna 'rental_date' a datetime
merge_6['rental_date'] = pd.to_datetime(merge_6['rental_date'])

def load_overall_analysis():
    st.title("Análisis General Base de Datos Sakila de Películas")

    # Cálculos principales
    total_peliculas = merge_6['title'].nunique()  # Total de películas únicas
    total_categorias = merge_6['name'].nunique()  # Total de categorías únicas
    promedio_inversion = round(merge_6['amount'].mean(), 2)  # Promedio de inversión
    cantidad_peliculas_por_año = merge_6.groupby(merge_6['rental_date'].dt.year)['title'].count()  # Cantidad por año
    
    # Desglose por los dos años disponibles
    years = cantidad_peliculas_por_año.index.tolist()
    year_1 = years[0] if len(years) > 0 else "No Data"
    year_2 = years[1] if len(years) > 1 else "No Data"
    peliculas_year_1 = cantidad_peliculas_por_año[year_1] if year_1 != "No Data" else 0
    peliculas_year_2 = cantidad_peliculas_por_año[year_2] if year_2 != "No Data" else 0

    # Columnas para las métricas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Películas", total_peliculas)
    with col2:
        st.metric("Total Categorías", total_categorias)
    with col3:
        st.metric("Promedio Inversión", f"${promedio_inversion}")

    # Tarjetas separadas para las películas por año
    st.subheader(f"Películas por Año")
    col5, col6 = st.columns(2)
    
    with col5:
        st.metric(f"Películas en {year_1}", peliculas_year_1)
    with col6:
        st.metric(f"Películas en {year_2}", peliculas_year_2)

# Llamada a la función
load_overall_analysis()


# Organizar los gráficos en 2 columnas
col5, col6 = st.columns(2)

# Primer gráfico: Conteo de Películas por Categoría
with col5:
    st.subheader("Conteo de Películas por Categoría")
    fig1 = px.bar(
        merge_6,
        x="name",  # 'name' para las categorías
        y="title",  # 'title' para contar las películas por categoría
        labels={"name": "Categoría", "title": "Cantidad de Películas"},
        color="name",  # Agrega color por categoría
        category_orders={"name": merge_6['name'].unique()}  # Para mantener el orden de categorías
    )
    st.plotly_chart(fig1)

# Segundo gráfico: Inversión en las 10 Principales Categorías (gráfico circular con porcentaje)
with col6:
    st.subheader("Promedio de las 10 Principales Categorías")
    top_categorias = merge_6.groupby('name')['amount'].sum().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.pie(
        top_categorias,
        names='name',
        values='amount',
        labels={"name": "Categoría", "amount": "Monto de Inversión"},
        hole=0.3,  # Hace que el gráfico sea un gráfico de dona
        color='name',  # Agrega color por categoría
        color_discrete_sequence=px.colors.qualitative.Set1,  # Define los colores
        template="plotly_dark",  # Usar tema oscuro (opcional)
        hover_data=['amount']  # Muestra el monto en el hover
    )
    st.plotly_chart(fig2)





#Grafico filtros y barras
st.title("Análisis de Inversión en Películas")

# Conversión de la columna 'rental_date' a datetime
merge_6['rental_date'] = pd.to_datetime(merge_6['rental_date'])

# Selector de análisis
st.subheader("Películas con Mayor Inversión")
option1 = st.selectbox('Basado en:', ['General', 'Mes'])

if option1 == 'Mes':
    # Películas con mayor inversión por año
    top_movies_month = merge_6.sort_values(by='amount', ascending=False).groupby(merge_6['rental_date'].dt.month).head(1)[['rental_date', 'title', 'amount']]
    top_movies_month['month'] = top_movies_month['rental_date'].dt.month  # Extraer el año

    # Gráfico interactivo con Plotly
    fig7 = go.Figure()
    for i, row in top_movies_month.iterrows():
        fig7.add_trace(go.Bar(
            x=[row['month']],
            y=[row['amount']],
            name=row['title']
        ))
    fig7.update_layout(
        title="Películas con Mayor Inversión por Mes",
        xaxis_title="Mes",
        yaxis_title="Inversión (Amount)",
        barmode='stack'
    )
    st.plotly_chart(fig7, use_container_width=True)

else:
    # Películas con mayor inversión general
    top_movies_overall = merge_6.groupby('title')['amount'].sum().sort_values(ascending=False).head(10).reset_index()

    # Gráfico horizontal interactivo con Plotly
    fig8 = go.Figure(go.Bar(
        x=top_movies_overall['amount'],
        y=top_movies_overall['title'],
        orientation='h'
    ))
    fig8.update_layout(
        title="Top 10 Películas con Mayor Inversión",
        xaxis_title="Inversión (Amount)",
        yaxis_title="Películas",
        yaxis=dict(autorange="reversed")  # Para mostrar el top en orden descendente
    )
    st.plotly_chart(fig8, use_container_width=True)

   
merge_6['rental_date'] = pd.to_datetime(merge_6['rental_date'])

def load_overall_analysis():
    st.title("Análisis General Base de Datos Sakila de Películas")

    # Gráfico Multiselector de barras para el staff
    st.subheader("Análisis de Rentas por Staff")

    # Filtrar los datos para los dos encargados
    staff_mapping = {1: 'Mike', 2: 'Jon'}  # Mapear staff_id a nombres
    merge_6['staff_name'] = merge_6['staff_id'].map(staff_mapping)  # Agregar columna con nombres

    encargados = list(staff_mapping.values())  # Usar nombres de staff
    seleccion = st.multiselect("Seleccione los encargados", encargados, default=encargados)

    if seleccion:
        rentas_staff = merge_6[merge_6['staff_name'].isin(seleccion)]
        conteo_rentas = rentas_staff['staff_name'].value_counts()

        st.bar_chart(conteo_rentas)
    else:
        st.write("Seleccione al menos un encargado para visualizar los datos.")

# Llamada a la función
load_overall_analysis()
