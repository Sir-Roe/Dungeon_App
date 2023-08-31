import plotly.express as px
from pathlib import Path
import streamlit as st
import pandas as pd
import os
import sys

filepath = os.path.join(Path(__file__).parents[1])
sys.path.insert(0, filepath)

from dnd_sql import PGSQL 
c = PGSQL()
df = pd.read_sql("select * from monsters",c.SQL_URL)
df_histo = df[['hit_points','size','alignment','xp','natural_ac','challenge_rating','strength','dexterity','intelligence','wisdom','constitution','charisma']]


df_histo.columns= df_histo.columns.str.title().str.strip().str.replace('_',' ')

histo = st.selectbox('Histogram data select', placeholder="Natural Ac", options=sorted(df_histo.columns))
if histo:
    try:
        st.plotly_chart(px.histogram(df_histo,histo))
    except BaseException:
        st.error(f'''
                 {histo.title()} could not be plotted into a histogram!
                 ''')

df_scatter = df[['hit_points','xp','natural_ac','challenge_rating','strength','dexterity','intelligence','wisdom','constitution','charisma']]
df_scatter.columns= df_scatter.columns.str.title().str.strip().str.replace('_',' ')

col1,col2 = st.columns(2)

sx = col1.selectbox('Choose your X Coordinate', placeholder="Challenge Rating", options=sorted(df_scatter.columns))

sy = col2.selectbox('Choose your Y Coordinate', placeholder="Xp", options=sorted(df_scatter.columns))

if histo:
    try:
        st.plotly_chart(px.scatter(df_histo,sx,sy))
    except BaseException:
        st.error(f'''
                 {sx.title()} could not be plotted into a histogram!
                 ''')