import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sys,os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(layout="wide")

def fahrenheit_to_celsius(f):
    return (f - 32) * 5.0/9.0

def sigmoid_celsius(x):
    # Adjust the sigmoid function to work with Celsius
    return 1 / (1 + np.exp(-0.75 * (x - 15.56)))

spacing1, col1, spacing, col2 = st.columns([1, 4, 1.5, 7], vertical_alignment="center")

with col1:
    with st.expander("Model Parameters", expanded=True):
        temperature_celsius = st.slider("Temperature (°C)", -5.0, 40.0, 15.56, 0.5, key="temperature")
        threshold = st.slider("Classification Threshold", 0.0, 1.0, 0.5, 0.01, key="threshold")
    
    info_placeholder = st.empty()

with col2:
    chart_placeholder = st.empty()

weather_data = pd.read_csv("data/weather_scatter.csv")

def update_chart_and_info(temperature, threshold):
    x_celsius = np.linspace(-10, 40, 100)

    y = sigmoid_celsius(x_celsius)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x_celsius, y=y, mode='lines', name='Probability', line=dict(color='black')))

    fig.add_trace(go.Scatter(x=x_celsius, y=[threshold]*len(x_celsius), mode='lines', name='Threshold', 
                             line=dict(color='black', dash='dash')))
    
    fig.add_trace(go.Scatter(x=[temperature_celsius], y=[sigmoid_celsius(temperature_celsius)], mode='markers', 
                             marker=dict(size=16, color='RoyalBlue', line=dict(color='white', width=3)), name='Current Temperature'))
    
    sunny_data = weather_data[weather_data["Weather"] == 1]
    rainy_data = weather_data[weather_data["Weather"] == 0]

    fig.add_trace(go.Scatter(x=fahrenheit_to_celsius(sunny_data["Temperature"]), y=sunny_data["Weather"], 
                             mode='markers', name='Sunny Days', 
                             marker=dict(size=13, color='#FFA500', opacity=0.75)))
    
    fig.add_trace(go.Scatter(x=fahrenheit_to_celsius(rainy_data["Temperature"]), y=rainy_data["Weather"], 
                             mode='markers', name='Rainy Days', 
                             marker=dict(size=13, color='#4169E1', opacity=0.75)))
    fig.update_layout(
        xaxis_title="Temperature (°C)",
        yaxis_title="Probability of Sunny Day",
        yaxis=dict(range=[-0.05, 1.05]),
        height=600
    )

    fig.update_xaxes(showgrid=True, gridcolor='#333333', zerolinecolor='#666666')
    fig.update_yaxes(showgrid=True, gridcolor='#333333', zerolinecolor='#666666')

    chart_placeholder.plotly_chart(fig, use_container_width=True)

    prediction = "Sunny" if sigmoid_celsius(temperature) > threshold else "Rainy"
    probability = sigmoid_celsius(temperature)

    info_placeholder.markdown(f"At **{temperature_celsius}°C**, there's a **{probability:.2f}** probability of a sunny day, predicting a **{prediction.lower()}** day.")

update_chart_and_info(temperature_celsius, threshold)