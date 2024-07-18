import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import sys, os
from sklearn.preprocessing import MinMaxScaler

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.title("Heart Disease Prediction")

# Load the model
model = tf.keras.models.load_model("model/heart_model.h5")

cp_test = st.selectbox("Select chest pain type", ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"])
cp_class_to_index = {"Typical angina": 0, "Atypical angina": 1, "Non-anginal pain": 2, "Asymptomatic": 3}
cp_test = cp_class_to_index[cp_test]

oldpeak_test = st.number_input("Enter oldpeak", min_value=0.0, max_value=6.2, value=0.0)

thalachh_test = st.number_input("Enter thalachh", min_value=71, max_value=202, value=71)

df = pd.read_csv("data/heart.csv")

# Assuming 'x' is your feature matrix (select the relevant columns)
x = df[['oldpeak', 'cp', 'thalachh']]

# Create a MinMaxScaler object
scaler = MinMaxScaler()

# Fit the scaler on the entire dataset
scaler.fit(x)

# Normalize the single input point
x_normalized = scaler.transform([[oldpeak_test, cp_test, thalachh_test]])
st.write(x_normalized)

# Make predictions
prediction = model.predict(x_normalized)
st.write(prediction)
