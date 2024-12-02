import sys 
from pathlib import Path 
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go 
from plotly._subplots import make_subplots
 

root = Path(__file__).parent.parent
sys.path.append(str(root))
from utils.dependencias import *

st.markdown('''
## Base de Datos Sakila
            ''')

fig = px.bar(
   datos_pelis,
    x="category_id",
    y="name",
    title='Conteo de peliculas por categoria'
)

st.plotly_chart(fig)


fig = px.line(
   datos_pelis,
    x="inventory_id",
    y="rental_date",
    title='Películas que mayor renta tuvieron por mes'
)

st.plotly_chart(fig)
