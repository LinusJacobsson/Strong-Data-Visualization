

""" Program for visualizing training data from Strong using Streamlit"""

""" Ideas for analysis:
1. Total number of workouts (between dates).
2. Number of different exercises (between dates).
3. Plot the calculated 1RM for different exercises over time.
4. Calculate the (average) total volume for different training days
5. Perform linear regession for the 1RM and predict future values.
6. 

 """

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


df = pd.read_csv("strong.csv")

cleaned = df[["Date", "Workout Name", "Duration", "Exercise Name", "Set Order", "Weight", "Reps"]]


def get_date_range(data_frame, start_date, end_date):
    """ Slices a dataframe between a start date and end date"""
    return data_frame[(data_frame["Date"] > start_date) & (data_frame["Date"] < end_date)]


def workouts_between_dates(data_frame, start_date, end_date):
    """ Takes a dataframe and two dates and prints the number
        of workouts between the dates.
    """
    date_range = get_date_range(data_frame, start_date, end_date)
    unique_dates = date_range['Date'].nunique()
    print(f'During this period, you have completed {unique_dates} workouts!')


def number_of_exercises(data_frame, start_date, end_date):
    """ Takes a dataframe and two dates and prints the number
        of unique exercises performed during that period.
    """
    date_range = get_date_range(data_frame, start_date, end_date)
    unique_exercises = date_range['Exercise Name'].nunique()
    print(f'During this period, you have performed {unique_exercises} different exercises!')



def one_rep_max_row(row):
    """ Takes a row in a dataframe, and calculates the
    theoretical 1 rep max using the Brzycki formula:
     weight * (36 / (37 - reps)), using the 'Weight' 
     and 'Reps' column.
    """
    weight = row['Weight']
    reps = row['Reps']
    return round(weight * (36/(37 - reps)))


def one_rep_max_exercise(dataframe, exercise):
    """ Applies the one_rep_max_row function to every row in a dataframe
    with the exercise name 'exercise', and then returns a list of the result.
    """ 
    squat_rows = dataframe.loc[df['Exercise Name'] == exercise]
    max =  squat_rows[['Weight', 'Reps']].apply(one_rep_max_row, axis=1)
    return list(max)

def main():
    workouts_between_dates(cleaned, '2022-08-01', '2023-01-15')
    number_of_exercises(cleaned, '2022-078-01', '2023-01-15')
    print(cleaned.head())
    print(one_rep_max_exercise(cleaned, "Squat (Barbell)"))
    
if __name__ == "__main__":
    main()