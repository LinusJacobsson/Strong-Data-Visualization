import streamlit as st
import pandas as pd
import strong
from PIL import Image

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.markdown('### Titel')  
st.sidebar.header('Strong analytics `version 1`')

st.sidebar.subheader('Choose training period')
start_date = st.sidebar.date_input('Starting date').strftime("%Y-%m-%d")
end_date =  st.sidebar.date_input('Ending date').strftime("%Y-%m-%d")



num_workouts = strong.workouts_between_dates(strong.cleaned, start_date, end_date)
num_exercises = strong.number_of_exercises(strong.cleaned, start_date, end_date)
# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Number of workouts",num_workouts, "1.2 °F")
col2.metric("Number of different exercises", num_exercises, "-8%")


