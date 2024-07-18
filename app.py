import streamlit as st
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

intro = st.Page('general/introduction.py', title='Introduction', icon=':material/home:', default=True)
knowledge = st.Page('general/knowledge_and_research.py', title='Knowledge and Research', icon=':material/insights:')

example_1 = st.Page('logistic_regression/example1.py', title='Prediction example', icon=':material/analytics:')
example_2 = st.Page('logistic_regression/example2.py', title='Gradient Descent example', icon=':material/manufacturing:')

data_table = st.Page('eda/data_table.py', title='Data Table', icon=':material/table_chart:')
univariate = st.Page('eda/univar_plot.py', title='Univariate Analysis', icon=':material/show_chart:')
mulvar = st.Page('eda/mulvar_plot.py', title='Multivariate Analysis', icon=':material/monitoring:')
correlation = st.Page('eda/correlation.py', title='Correlation', icon=':material/stacked_line_chart:')

train = st.Page('model/train.py', title='Train', icon=':material/rebase:')
predict = st.Page('model/predict.py', title='Predict', icon=':material/pivot_table_chart:')
final_visu = st.Page('model/final_visualization.py', title='Final Visualization', icon=':material/view_in_ar:')

pg = st.navigation(
    {
        "General": [intro, knowledge],
        "Logistic Regression": [example_1, example_2],
        "Exploratory Data Analysis": [data_table, univariate, mulvar, correlation],
        "Model": [train, predict, final_visu]
    }
)

pg.run()