import streamlit as st 
import pickle 
from PIL import Image

st.header("Our Model : Linear Regression")
image = Image.open('pages/visualise.png')
st.image(image , use_column_width=True , caption='Model Visualisation')


load_model = pickle.load(open('solubility_model.pkl' , 'rb'))

st.header("Derived Formula : ")
st.write("""
    ##### logS = -0.74*molLogP - 0.01*Molar weight + -0.42*Aromatic Proportion + 0.26\n
    ***Above coefficients are truncated upto 2 decimals*** \n
    Intresting to note that , our formula is independent of number of rotatable bonds !
""")
