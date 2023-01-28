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
category_counts['category'] = category_counts['category'].replace({'machine': 'Machine', 'Smith Machine': 'Machine'})

category_counts.columns = ['category', 'count']
print(category_counts)
#labels = strong.cleaned['category'].unique()
#values = strong.cleaned['category'].value_counts().tolist()
first_set = strong.cleaned[strong.cleaned['Set Order'] == 1]
second_set = strong.cleaned[strong.cleaned['Set Order'] == 2]
data_first_set = strong.one_rep_max_exercise(first_set, "Bicep Curl (Cable)")
data_second_set = strong.one_rep_max_exercise(second_set, "Bicep Curl (Cable)")
c1, c2 = st.columns((6,4))
with c1:
    y1 = [item[0] for item in data_first_set]
    x1 = [item[1] for item in data_first_set]
    y2 = [item[0] for item in data_second_set]
    x2 = [item[1] for item in data_second_set]
    fig, ax = plt.subplots()
    ax.plot(x1, y1, linestyle = '--', color = "blue")
    ax.plot(x2, y2, linestyle = '--', color = "red")
    ax.set_xticklabels(x1, rotation=45)
    ax.legend(['First Set', 'Second Set'])

    st.pyplot(fig)
with c2:
    plost.donut_chart(
        data= category_counts,
        theta= 'count',
        color= 'category',
        legend='top', 
        use_container_width=True,
        height = 350,
        title = "Exercise categories")



plot_data = st.sidebar.multiselect('Select data', ['temp_min', 'temp_max'], ['temp_min', 'temp_max'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)
#seattle_weather = pd.read_csv('https://raw.githubusercontent.com/tvst/plost/master/data/seattle-weather.csv', parse_dates=['date'])
#st.line_chart(seattle_weather, height = plot_height)