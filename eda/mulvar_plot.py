import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.title("Multivariate Analysis")

data = pd.read_csv("data/heart.csv")
numerical_columns = data.select_dtypes(include=[np.number]).columns.tolist()

st.subheader("Select Columns for Analysis")
selected_columns = st.multiselect("Choose columns for analysis", numerical_columns, default=numerical_columns[:4])

if st.button("Generate Pairplot", key="pairplot"):
    st.write("Generating pairplot...")
    pairplot = sns.pairplot(data=data[selected_columns])
    st.pyplot(pairplot)

if st.button("")