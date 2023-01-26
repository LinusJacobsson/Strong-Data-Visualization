import streamlit as st
import pandas as pd
import strong
from PIL import Image
import matplotlib.pyplot as plt
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

background_image = Image.open('strong_logo.png')
#st.sidebar.image(background_image, use_column_width=True,  )
st.markdown('### Titel')  
st.sidebar.header('Strong analytics `version 1`')

st.sidebar.subheader('Choose training period')
start_date = st.sidebar.date_input('Starting date').strftime("%Y-%m-%d")
end_date =  st.sidebar.date_input('Ending date').strftime("%Y-%m-%d")



num_workouts = strong.workouts_between_dates(strong.cleaned, start_date, end_date)
num_exercises = strong.number_of_exercises(strong.cleaned, start_date, end_date)
sum_volume = strong.total_volume(strong.get_date_range(strong.cleaned, start_date, end_date))
# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Number of workouts", num_workouts)
col2.metric("Number of different exercises", num_exercises)
col3.metric("Total volume", str(round(sum(sum_volume)))+ " kg")

st.markdown('One rep max progression')
exercise = st.selectbox('Select exercise', strong.get_exercises(strong.cleaned))
st.write('You chose: ', exercise)


st.markdown('Distribution of exercises')
category_counts = strong.cleaned['category'].value_counts().reset_index()
category_counts.columns = ['category', 'count']
print(category_counts)
#labels = strong.cleaned['category'].unique()
#values = strong.cleaned['category'].value_counts().tolist()
c1, c2 = st.columns((7,3))
with c1:
    plost.donut_chart(
        data= category_counts,
        theta= 'count',
        color= 'category',
        legend='bottom', 
        use_container_width=True)
    """fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    st.pyplot(fig)"""


plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)
#seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
#st.line_chart(seattle_weather, height = plot_height)