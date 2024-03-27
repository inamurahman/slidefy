import streamlit as st
import reveal_slides as rs

st.set_page_config(initial_sidebar_state="collapsed")

with open("presentation.md", "r") as file:
    content = file.read()

rs.slides(content)