import streamlit as st
import pandas as pd
import strong
from PIL import Image
import matplotlib.pyplot as plt
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ----- Sidebar -------
background_image = Image.open('strong_logo.png')
st.sidebar.image(background_image, use_column_width=True)
st.sidebar.header('Strong analytics `version 1`')
st.sidebar.subheader('Choose training period')
start_date = st.sidebar.date_input('Starting date').strftime("%Y-%m-%d")
end_date =  st.sidebar.date_input('Ending date').strftime("%Y-%m-%d")
st.sidebar.subheader('Choose exercise to view one rep max')
exercise =  st.sidebar.selectbox('Select exercise', strong.get_exercises(strong.cleaned))
st.sidebar.subheader('Choose sets to count')
plot_data = st.sidebar.multiselect('Select sets', ['Set one', 'Set two'], ['Set one', 'Set two'])
st.sidebar.markdown('''
---
Created by Linus Jacobsson.
''')



num_workouts = strong.workouts_between_dates(strong.cleaned, start_date, end_date)
num_exercises = strong.number_of_exercises(strong.cleaned, start_date, end_date)
sum_volume = strong.total_volume(strong.get_date_range(strong.cleaned, start_date, end_date))

# ---- First row --------
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Number of workouts", num_workouts)
col2.metric("Number of different exercises", num_exercises)
col3.metric("Total volume", str(round(sum(sum_volume)))+ " kg")
# ------------------------------------------

category_counts = strong.cleaned['category'].value_counts().reset_index()
category_counts['category'] = category_counts['category'].replace({'machine': 'Machine', 'Smith Machine': 'Machine'})
category_counts.columns = ['category', 'count']

set_1 = "Set one"
set_2 = "Set two"
first_set = strong.cleaned[strong.cleaned['Set Order'] == 1]
data_first_set = strong.one_rep_max_exercise(first_set, exercise, start_date, end_date)
y1 = [item[0] for item in data_first_set]
x1 = [item[1] for item in data_first_set]

second_set = strong.cleaned[strong.cleaned['Set Order'] == 2]
data_second_set = strong.one_rep_max_exercise(second_set, exercise, start_date, end_date)
y2 = [item[0] for item in data_second_set]
x2 = [item[1] for item in data_second_set]
c1, c2 = st.columns((6,4))
with c1:
    st.markdown("**One rep max progression**")
    fig, ax = plt.subplots()
    if set_1 in plot_data:
        ax.plot(x1, y1, linestyle = '--', color = "blue")
    if set_2 in plot_data:
        ax.plot(x2, y2, linestyle = '--', color = "red")

    ax.set_xticklabels(x1, rotation=45)
    ax.legend(['First Set', 'Second Set'])
    ax.set_ylabel("kg")
    st.pyplot(fig)
with c2:
    st.markdown("**Exercise categories**")
    plost.donut_chart(
        data= category_counts,
        theta= 'count',
        color= 'category',
        legend='top', 
        use_container_width=True,
        height = 350,)
week_counts = strong.get_weekly_workouts(strong.cleaned, start_date, end_date)

st.markdown("**Weekly workouts**")

fig, ax = plt.subplots(figsize=(10,5))
ax.bar(week_counts.index, week_counts.values)
ax.set_xlabel('Start of week')
ax.set_ylabel('Number of workouts')
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
ax.set_xticks(week_counts.index)
ax.set_xticklabels(week_counts.index, rotation=45, fontsize = 8)

st.pyplot(fig)




