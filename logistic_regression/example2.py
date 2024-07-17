import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(layout="wide")

if 'weight' not in st.session_state:
    st.session_state.weight = 0.0
if 'bias' not in st.session_state:
    st.session_state.bias = 0.0
if 'errors' not in st.session_state:
    st.session_state.errors = []
if 'iterations' not in st.session_state:
    st.session_state.iterations = 0

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def compute_error(weight, bias, data):
    total_error = 0
    for _, row in data.iterrows():
        x = row['Temperature (C)']
        y = row['Weather']
        prediction = sigmoid(weight * x + bias)
        total_error += -y * np.log(prediction) - (1 - y) * np.log(1 - prediction)
    return total_error / len(data)

def gradient_descent_step(data, learning_rate=0.1):
    weight_gradient = 0
    bias_gradient = 0
    n = len(data)

    for _, row in data.iterrows():
        x = row['Temperature (C)']
        y = row['Weather']
        prediction = sigmoid(st.session_state.weight * x + st.session_state.bias)
        weight_gradient += (prediction - y) * x
        bias_gradient += (prediction - y)

    st.session_state.weight -= (weight_gradient / n) * learning_rate
    st.session_state.bias -= (bias_gradient / n) * learning_rate

    st.session_state.iterations += 1
    error = compute_error(st.session_state.weight, st.session_state.bias, data)
    st.session_state.errors.append((st.session_state.iterations, error))

def fahrenheit_to_celsius(f):
    return (f - 32) * 5.0/9.0

def sigmoid_celsius(x):
    # Adjust the sigmoid function to work with Celsius
    return 1 / (1 + np.exp(-0.75 * (x - 15.56)))

spacing2, col3, spacing, col4 = st.columns([1, 4, 1.5, 7], vertical_alignment="center")

data = pd.read_csv("data/weather_scatter.csv")
data["Temperature (C)"] = data["Temperature"].apply(fahrenheit_to_celsius)

with col3:
    with st.expander("Weight and Bias", expanded=True):
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            if st.button("1 step"):
                gradient_descent_step(data, learning_rate=0.1)
        with col6:
            if st.button("5 steps"):
                for _ in range(5):
                    gradient_descent_step(data, learning_rate=0.1)
        with col7:
            if st.button("10 steps"):
                for _ in range(10):
                    gradient_descent_step(data, learning_rate=0.1)
        with col8:
            if st.button("25 steps"):
                for _ in range(25):
                    gradient_descent_step(data, learning_rate=0.1)

        st.session_state.weight = st.slider("Weight", -3.0, 3.0, float(st.session_state.weight), 0.05)
        st.session_state.bias = st.slider("Bias", -50.0, 10.0, float(st.session_state.bias), 1.0)

        if st.button("Reset",key="reset"):
            st.session_state.weight = 0.0
            st.session_state.bias = 0.0
            st.session_state.errors = []
            st.session_state.iterations = 0

    model_equation = f"P(y = 1|x) = \\frac{{1}}{{1 + e^{{-({st.session_state.bias:.2f} + {st.session_state.weight:.2f}x)}}}}"
    st.latex(model_equation)

with col4:
    scatter_fig = go.Figure()
    scatter_fig.add_trace(go.Scatter(x=data['Temperature (C)'], y=data['Weather'], mode='markers', name='Data Points'))
    
    x_range = np.linspace(min(data['Temperature (C)']), max(data['Temperature (C)']), 100)
    y_range = sigmoid(st.session_state.weight * x_range + st.session_state.bias)
    scatter_fig.add_trace(go.Scatter(x=x_range, y=y_range, mode='lines', name='Regression Line'))

    scatter_fig.update_layout(
        title="Gradient Descent Scatter Plot",
        xaxis_title="Temperature (C)",
        yaxis_title="Weather"
    )
    st.plotly_chart(scatter_fig)

    error_fig = go.Figure()
    if st.session_state.errors:
        iterations, errors = zip(*st.session_state.errors)
        error_fig.add_trace(go.Scatter(x=iterations, y=errors, mode='lines+markers', name='Error'))

    error_fig.update_layout(
        title="Gradient Descent Error Plot",
        xaxis_title="Iterations",
        yaxis_title="Error"
    )
    st.plotly_chart(error_fig)
