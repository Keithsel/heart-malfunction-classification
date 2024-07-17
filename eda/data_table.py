import streamlit as st
import pandas as pd
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(layout="wide")

st.title("Data table view")

df = pd.read_csv("data/heart.csv")

st.dataframe(df, use_container_width=True)