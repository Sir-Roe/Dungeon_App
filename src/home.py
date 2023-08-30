from pathlib import Path
import streamlit as st
import os

folder_dir = os.path.join(Path(__file__).parents[0], 'data')


st.set_page_config(
    page_title="DnD 5e Companion App", #<------- Change this to the page you're currently on when copying/pasting after your imports
    page_icon="🎲",
    menu_items={
        'About': """This is an app developed during my Capstone Week at Coding Temple. Here is my
        Github account: \n\rLogan : https://github.com/Sir-Roe"""}
)



st.markdown("<h1 style='text-align: center; '>DnD 5e Companion App</h1>", unsafe_allow_html=True)
st.image(f'{folder_dir}/battle.jpg',width=800)
st.text("Logan Roe's capstone application utilizing the following:")
        
st.text(""">Streamlit 
>Python
>Pandas
>Postgres SQL
>D&D 5e API
>Plotly
>Deep AI API""")

st.header("Here are the different pages of my application:")

st.subheader('Monster Codex')

st.text('Search and pull up critical monster information!\nAI Generated description and Art for missing values from the compendium!')

#st.image('https://cdnb.artstation.com/p/assets/images/images/007/366/345/large/cyril-merle-table-sorcery-rvb.jpg?1505654683')

st.subheader('Monster Stats')

st.text('Simple visualizations of Monster stats by chosen slicers.')

st.subheader('Summary')

st.text('Simple visualizations of Monster stats by chosen slicers.')
