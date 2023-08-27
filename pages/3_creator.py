import streamlit as st 
from PIL import Image

st.header("Tejas Mhaiskar")

image = Image.open('pages\photome.jpg')
st.image(image , use_column_width=True)

st.write("""
    ### IIT Dharwad 
    ### tejasmhaiskar@gmail.com
""")