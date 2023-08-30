import streamlit as st
from pathlib import Path
import os


st.set_page_config(
    page_title="DnD 5e Companion App", #<------- Change this to the page you're currently on when copying/pasting after your imports
    page_icon="🎲",
    menu_items={
        'About': """This is an app developed during my Capstone Week at Coding Temple. Here is my
        Github account: \n\rLogan : https://github.com/Sir-Roe"""}
)

st.header("DnD 5e Companion App Summary")
st.text("""
        The purpose of this application is to create an application using the
        Dungeons and Dragons 5e Open Api. The first steps to do this was pulling the data,
        cleaning the data, pushing the data to Elepgant SQL. After, I created a
        virtual environment that will house all of the python installs and
        the application. Using my dnd_sql class I query my database and pull the data
        into my streamlit pages and present it. In the case of missing data for
        description or images I utilized the DEEP AI API to fill in the gaps. 
        In order to improve speed and reduce the calls to the DEEP AI API I 
        store the generated outputs and save them in the data folder of the 
        Application. In future versions I can add a RE GENERATE function to 
        re-create these outputs with custom tags.
        
        For the visualiztions I utilized select box on filtered dataframes.
        The first option is the select for histogram for any column in the data set.
        The second option is to select an x and y value to scatter plot!
        """)

st.image('https://logos-world.net/wp-content/uploads/2021/12/DnD-Logo.png',width=400)


st.text("""
        A special thanks to the https://www.dnd5eapi.co/
        """)

