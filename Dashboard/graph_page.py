from turtle import window_width
import streamlit as st
import streamlit.components.v1 as components

# Show Tableau Dashboard
def show_table_page():
    box1, tableau_box, box3 = st.columns((1,8,1))
    with tableau_box:
        HtmlFile=open('Dashboard/static/tableau_dashboard.html')
        components.html(HtmlFile.read(), height=1000)
