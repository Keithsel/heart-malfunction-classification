import streamlit as st
import streamlit.components.v1 as components
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.title("The classification space")

st.write("The visualization for the train set")

with open('model/plot1.html', 'r') as file:
    body1 = file.read()

components.html(body1, height=512)

st.write("The visualization for the test set")

with open('model/plot2.html', 'r') as file:
    body2 = file.read()

components.html(body2, height=512)