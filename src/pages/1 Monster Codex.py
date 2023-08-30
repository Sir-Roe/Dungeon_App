from pathlib import Path
import pandas as pd
import streamlit as st
import os
import sys
import numpy as np

#--------------------Set File Path---------------
filepath = os.path.join(Path(__file__).parents[1])
sys.path.insert(0, filepath)
folder_dir = os.path.join(Path(__file__).parents[1], 'data')
#------------grab our sql functions-------
from dnd_sql import PGSQL
from aiscripts import *
c= PGSQL()
cursor= c.cur

#centered title
st.markdown("<h1 style='text-align: center; '>Monster Codex</h1>", unsafe_allow_html=True)

df = pd.read_sql("select * from monsters",c.SQL_URL)

df.columns=df.columns.str.title().str.strip().str.replace('_',' ')

mon_list = df['Name']
selection = st.selectbox('Monster Select Box:', placeholder="Aboleth", options=sorted(mon_list))
dfmaster = df[(df['Name']==selection)]
col1t,col2t = st.columns(2)

try:
    mimage = dfmaster['Image'][0]
    col2t.image(f'https://www.dnd5eapi.co{mimage}')
    
except:
   
    if os.path.isfile(f'{folder_dir}\{selection}.png'):
        col2t.image(f'{folder_dir}\{selection}.png')
        col2t.write("AI pre-Generated Image")
    else:
        col2t.image(generateImage(selection))
        col2t.write("AI New Generated Image")

#Description Block, completely worthless right now
col1t.markdown("<h3 style='text-align: center;'>Description </h3>", unsafe_allow_html=True)
if ''.join(str(val) for val in dfmaster['Descrip'].values) != "None":
    col1t.write(''.join(str(val) for val in dfmaster['Descrip'].values))
elif os.path.isfile(f'{folder_dir}\{selection}.txt'):
    f = open(f'{folder_dir}\{selection}.txt','r')
    col1t.write(f.read())
    col1t.write('Deep AI pre-generated description')
else:
    col1t.write(generateDesc(selection))
    col1t.write('Deep AI Generated description')
#centered subheader

st.markdown("<h2 style='text-align: center;'>Base Creature Stats </h2>", unsafe_allow_html=True)
st.data_editor(dfmaster[['Size','Type','Alignment','Natural Ac','Xp','Challenge Rating']],hide_index=True)
st.data_editor(dfmaster[['Strength','Dexterity','Intelligence','Constitution','Wisdom','Charisma']],hide_index=True)
st.data_editor(dfmaster[['Speed Walk','Speed Swim','Speed Fly','Speed Burrow']],hide_index=True)

#build our attack blocks
monster_id= ''.join(str(val) for val in dfmaster['Monster Id'].values)
st.write(monster_id)
#grab selected table values
df_attk= pd.read_sql(f"SELECT * FROM monster_actions where monster_id = '{monster_id}'",c.SQL_URL)
df_attk.columns=df_attk.columns.str.title().str.strip().str.replace('_',' ')
#
df_res= pd.read_sql(f"SELECT * FROM monster_resists where monster_id = '{monster_id}'",c.SQL_URL)
df_res.columns=df_res.columns.str.title().str.strip().str.replace('_',' ')
#
df_char= pd.read_sql(f"SELECT * FROM monster_characteristics where monster_id = '{monster_id}' order by characteristic desc",c.SQL_URL)
df_char.columns=df_char.columns.str.title().str.strip().str.replace('_',' ')

#Build Our Stats Columns
col1,col2,col3 = st.columns(3)

#we will be using df attack here and do some looping to make a clean list
col1.image(f'{folder_dir}/sword.png')
col1.write("<h3 style='text-align: center;'>|     Actions     |   </h3>", unsafe_allow_html=True)
col1.write("---------------------------------------------")
for index, row in df_attk.iloc[:,1:10].iterrows():
    
    col1.write(f"<h5 style='text-align: center;'>|{row['Action Name']}|   </h5>", unsafe_allow_html=True)
    
    for column_name, cell_value in row.items():
        if cell_value != None and column_name!= "Action Name":
            col1.write(column_name + " : " + str(cell_value))
    col1.write("---------------------------------------------")

#makecharacteristics table    
col2.image(f'{folder_dir}/Brain.png')
col2.write("<h3 style='text-align: center;'>|  Characteristics|  </h3>", unsafe_allow_html=True)

last_rowc2 =''
for index, row in df_char.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Characteristic']!= last_rowc2:
        col2.write("---------------------------------------------")
        col2.write(f"<h5 style='text-align: center;'>|{row['Characteristic'].title()}|   </h5>", unsafe_allow_html=True)
    last_rowc2 =row['Characteristic']
    for column_name, cell_value in row.items():
        if cell_value != np.nan and column_name!= 'Characteristic':
            col2.write(column_name + " : " + str(cell_value))
#Build Resistances Tables
col3.image(f'{folder_dir}/shields.png')
col3.write("<h3 style='text-align: center;'>|   Resistances   | </h3>", unsafe_allow_html=True)
last_rowc3 =''
for index, row in df_res.iloc[:,1:].iterrows():
    if row['Type']!= last_rowc2:
        col3.write("---------------------------------------------")   
        col3.write(f"<h5 style='text-align: center;'>|{row['Type'].title()}|   </h5>", unsafe_allow_html=True)
    for column_name, cell_value in row.items():
        if cell_value != None and column_name!= "Type":
            col3.write(column_name + " : " + str(cell_value))

st.write(folder_dir)