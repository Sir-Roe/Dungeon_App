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
dfmaster = df[(df['Name']==selection)].reset_index()

#top logic for pictures and base information
col1t,col2t = st.columns(2)
#col 1------------Logic

#add top line stats
size_type=(f"{dfmaster['Size'][0]} {dfmaster['Type'][0]}, {dfmaster['Alignment'][0]}")
col1t.markdown(f"<h5 style='text-align: left;'>{size_type}</h5>", unsafe_allow_html=True)
#loop and print stats
for index, row in dfmaster[['Challenge Rating','Natural Ac','Hit Points','Xp']].iterrows():
    for column_name, cell_value in row.items():
        col1t.write(f"{column_name} : {cell_value}")
#add movement speeds
for index, row in dfmaster[['Speed Walk','Speed Swim','Speed Fly','Speed Burrow']].iterrows():
    for column_name, cell_value in row.items():
        if cell_value > 0:
            col1t.write(f"{column_name} : {int(cell_value)} Feet")
#custom emojis for stats for style
col1t.markdown("__________________________________")
col1t.write(f"💪Strength: {dfmaster['Strength'][0]} ({(dfmaster['Strength'][0]-10)//2})")
col1t.write(f"🏹Dexterity: {dfmaster['Dexterity'][0]} ({(dfmaster['Dexterity'][0]-10)//2})")
col1t.write(f"🪄Intelligence: {dfmaster['Intelligence'][0]} ({(dfmaster['Intelligence'][0]-10)//2})")
col1t.write(f"🦉Wisdom: {dfmaster['Wisdom'][0]} ({(dfmaster['Wisdom'][0]-10)//2})")
col1t.write(f"🐂Constitution: {dfmaster['Constitution'][0]} ({(dfmaster['Constitution'][0]-10)//2})")
col1t.write(f"🎭Charisma: {dfmaster['Charisma'][0]} ({(dfmaster['Charisma'][0]-10)//2})")
col1t.markdown("__________________________________")


#col 2----------- Logic ----------------   
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
col2t.markdown("<h3 style='text-align: center;'>Description </h3>", unsafe_allow_html=True)
if ''.join(str(val) for val in dfmaster['Descrip'].values) != "None":
    col2t.write(''.join(str(val) for val in dfmaster['Descrip'].values))
elif os.path.isfile(f'{folder_dir}\{selection}.txt'):
    f = open(f'{folder_dir}\{selection}.txt','r')
    col2t.write(f.read())
    col2t.write('Deep AI pre-generated description')
else:
    col2t.write(generateDesc(selection))
    col2t.write('Deep AI Generated description')

#build our attack blocks
monster_id= dfmaster['Monster Id'][0]


#grab selected table values for the following stat block dfs
df_attk= pd.read_sql(f"SELECT * FROM monster_actions where monster_id = '{monster_id}' order by action_type asc, multi_attack asc",c.SQL_URL)
df_attk.columns=df_attk.columns.str.title().str.strip().str.replace('_',' ')
#
df_res= pd.read_sql(f"SELECT * FROM monster_resists where monster_id = '{monster_id}' order by type asc",c.SQL_URL)
df_res.columns=df_res.columns.str.title().str.strip().str.replace('_',' ')
#
df_char= pd.read_sql(f"SELECT * FROM monster_characteristics where monster_id = '{monster_id}' order by characteristic desc",c.SQL_URL)
df_char.columns=df_char.columns.str.title().str.strip().str.replace('_',' ')

#------------------stylized senses block
senses=''
for index, row in df_char.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Characteristic'] == 'senses':
        for column_name, cell_value in row.items():
            if cell_value  and column_name!= 'Characteristic':
                if type(cell_value)==float:
                    if (cell_value)>0:
                        senses+= f" {str(cell_value).replace('_',' ')} Feet "
                else:
                    senses+= f"🔎{str(cell_value).replace('_',' ')} "
        senses+="\n\r" 
   
col1t.write(senses)

#------------------stylized Language block
lang=''
for index, row in df_char.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Characteristic'] == 'language':
        for column_name, cell_value in row.items():
            if cell_value  and column_name!= 'Characteristic':
                if type(cell_value)==float:
                    if(cell_value)>0:
                        lang+= f" {str(cell_value).replace('_',' ')} Feet "
                else:
                    lang+= f"🗣️{str(cell_value).replace('_',' ')} "
        lang+="\n\r" 
   
col1t.write(lang)

#-----------------Proficiency Block

prof=''
for index, row in df_char.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Characteristic'] == 'proficiency':
        for column_name, cell_value in row.items():
            if cell_value  and column_name!= 'Characteristic':
                if type(cell_value)==float:
                    prof+= f" + ({str(cell_value).replace('_',' ')})"
                else:
                    prof+= f"🧠{str(cell_value).replace('_',' ')} "
        prof+="\n\r" 
   
col2t.write(prof)
#---------------Vulns------------------
dv=''
for index, row in df_res.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Type'] == 'damage_resistances':
        dv+=f"💔{str(row['Type']).replace('_',' ').title()} : {str(row['Value']).replace('_',' ').title()}"
    dv+="\n\r" 
   
col2t.write(dv)

#---------------Resistances------------------
dr=''
for index, row in df_res.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Type'] == 'damage_resistances':
        dr+=f"🛡️{str(row['Type']).replace('_',' ').title()} : {str(row['Value']).replace('_',' ').title()}"
    dr+="\n\r" 
   
col2t.write(dr)

#---------------Immunities------------------
di=''
for index, row in df_res.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Type'] == 'damage_immunities':
        di+=f"🪨{str(row['Type']).replace('_',' ').title()} : {str(row['Value']).replace('_',' ').title()}"
    di+="\n\r" 
   
col2t.write(di)

#---------------Conditional Immunities------------------
cond=''
for index, row in df_res.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Type'] == 'condition_immunities':
        cond+=f"☔{str(row['Type']).replace('_',' ').title()} : {str(row['Value']).replace('_',' ').title()}"
    cond+="\n\r" 
   
col2t.write(cond)


#------------------Action Block
df_attk = df_attk[['Monster Id','Action Type','Action Name','Multi Attack','Damage Dice','Attack Bonus','Damage Type', 'Dc Type', 'Dc Value','Descrip']]
action=''
for index, row in df_attk.iloc[:,1:9].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Action Type'] == 'actions':
        for column_name, cell_value in row.items():
            if cell_value  and column_name!= 'Action Type':
                if column_name == 'Action Name':
                    action+= f"⚔️{str(cell_value).replace('_',' ')}⚔️"
                elif type(cell_value)==float:
                    if cell_value>0:
                        action+= f"{column_name} : {str(cell_value).replace('_',' ')}"
                else:
                    action+= f"{column_name} : {str(cell_value).replace('_',' ')}"

                action+="\n\r" 
   

#----------------Special Actions------------------------------
df_attk = df_attk[['Monster Id','Action Type','Action Name','Multi Attack','Damage Dice','Attack Bonus','Damage Type', 'Dc Type', 'Dc Value','Descrip']]
spec_action=''
for index, row in df_attk.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Action Type'] == 'special_abilities':
        for column_name, cell_value in row.items():
            if cell_value  and column_name!= 'Action Type':
                if column_name == 'Action Name':
                    spec_action+= f"✨{str(cell_value).replace('_',' ')}✨"
                elif type(cell_value)==float:
                    if cell_value>0:
                        spec_action+= f"{column_name} : {str(cell_value).replace('_',' ')}"
                else:
                    spec_action+= f"{column_name} : {str(cell_value).replace('_',' ')}"

                spec_action+="\n\r" 
   

#--------------- Legendary Actions---------------------------
df_attk = df_attk[['Monster Id','Action Type','Action Name','Multi Attack','Damage Dice','Attack Bonus','Damage Type', 'Dc Type', 'Dc Value','Descrip']]
leg_action=''
for index, row in df_attk.iloc[:,1:].iterrows():
    #We did a sort query to make characteristic blocks
    if row['Action Type'] == 'legendary_actions':
        for column_name, cell_value in row.items():
            if cell_value  and column_name!= 'Action Type':
                if column_name == 'Action Name':
                    leg_action+= f"🐉{str(cell_value).replace('_',' ')}🐉"
                elif type(cell_value)==float:
                    if cell_value>0:
                        leg_action+= f"{column_name} : {str(cell_value).replace('_',' ')}"
                else:
                    leg_action+= f"{column_name} : {str(cell_value).replace('_',' ')}"

                leg_action+="\n\r" 
   


tab1, tab2, tab3 = col1t.tabs(["⚔️Actions⚔️", "✨Specials✨", "🐉Legendary Skills🐉"])

with tab1:
    st.write(action)

with tab2:
    st.write(spec_action)

with tab3:
    st.write(leg_action)


