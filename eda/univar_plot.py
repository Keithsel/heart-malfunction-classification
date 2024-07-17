import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(layout="wide")

st.title("Univariate Analysis")

df = pd.read_csv("data/heart.csv")

numerical_column = ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']
categorical_column = [col for col in df.columns if col not in numerical_column]

col_type = st.selectbox("Select column type", ["Numerical", "Categorical"])
if col_type == "Numerical":
    column = st.selectbox("Select column", numerical_column)
else:
    column = st.selectbox("Select column", categorical_column)

description = df[column].describe().to_frame().T
st.dataframe(description, use_container_width=True)

col1, col2 = st.columns(2)

if column in numerical_column:
    with col1:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.histplot(df[column], kde=True, ax=ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.boxplot(y=df[column], ax=ax)
        st.pyplot(fig)

else:
    with col1:
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.countplot(x=df[column], palette="viridis", ax=ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(10, 8))
        df[column].value_counts().plot.pie(autopct="%1.1f%%", colors=sns.color_palette("viridis"), startangle=90, ax=ax)
        st.pyplot(fig)
