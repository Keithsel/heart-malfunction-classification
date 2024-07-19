import streamlit as st
import tensorflow as tf
import numpy as np
import pandas as pd
import sys, os
from sklearn.preprocessing import MinMaxScaler

if 'cp_test' not in st.session_state:
    st.session_state.cp_test = "Typical angina"
if 'oldpeak_test' not in st.session_state:
    st.session_state.oldpeak_test = 0.0
if 'thalachh_test' not in st.session_state:
    st.session_state.thalachh_test = 71

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.title("Heart Disease Prediction")

model = tf.keras.models.load_model("model/heart_model.h5")

cp_class_to_index = {
    "Typical angina": 0, 
    "Atypical angina": 1, 
    "Non-anginal pain": 2, 
    "Asymptomatic": 3
}

st.session_state.cp_test = st.selectbox(
    "Select chest pain type", 
    ["Typical angina", "Atypical angina", "Non-anginal pain", "Asymptomatic"], 
    index=list(cp_class_to_index.keys()).index(st.session_state.cp_test)
)
cp_test = cp_class_to_index[st.session_state.cp_test]

st.session_state.oldpeak_test = st.number_input(
    "Enter oldpeak", 
    min_value=0.0, 
    max_value=6.2, 
    value=st.session_state.oldpeak_test
)

st.session_state.thalachh_test = st.number_input(
    "Enter thalachh", 
    min_value=71, 
    max_value=202, 
    value=st.session_state.thalachh_test
)

df = pd.read_csv("data/heart.csv")
x = df[['oldpeak', 'cp', 'thalachh']]
scaler = MinMaxScaler()
scaler.fit(x)

x_input = np.array([[st.session_state.oldpeak_test, cp_test, st.session_state.thalachh_test]])
x_normalized = scaler.transform(x_input)

if st.button("Predict"):
    prediction = model.predict(x_normalized)

    st.write(f"The prediction is {int(prediction[0][0] > 0.5)}")
    st.write(f"The probability of having heart disease is {prediction[0][0]:.2f}")
    
    if prediction[0][0] > 0.5:
        st.write("The patient is likely to have heart disease")
    else:
        st.write("The patient is not likely to have heart disease")
        
    st.session_state.cp_test = "Typical angina"
    st.session_state.oldpeak_test = 0.0
    st.session_state.thalachh_test = 71