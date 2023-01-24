

""" Program for visualizing training data from Strong using Streamlit"""

import pandas as pd
#import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as plt_date


df = pd.read_csv("strong.csv")

cleaned = df[["Date", "Workout Name", "Duration", "Exercise Name", "Set Order", "Weight", "Reps"]]
cleaned['Date'] = pd.to_datetime(cleaned['Date']).dt.strftime('%Y-%m-%d')
 # Remove time

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
    date = row['Date']
    return (round(weight * (36/(37 - reps))), date)


def one_rep_max_exercise(dataframe, exercise):
    """ Applies the one_rep_max_row function to every row in a dataframe
        with the exercise name 'exercise', and then returns a list of the result.
    """ 
    squat_rows = dataframe.loc[df['Exercise Name'] == exercise]
    max =  squat_rows[['Weight', 'Reps', 'Date']].apply(one_rep_max_row, axis=1)
    return list(max)


def plot_max(date_weight_tuples, exercise):
    """Creates a scatter plot of the calculated one rep max
        vs the dates.
    """
    dates = plt_date.date2num(np.array([date[1] for date in date_weight_tuples]))
    maxes = np.array([max[0] for max in date_weight_tuples])
    coefficients = np.polyfit(dates, maxes, 1)
    polynomial = np.poly1d(coefficients)
    ys = polynomial(dates)
    plt.plot_date(dates, maxes)
    plt.plot(dates, ys)
    plt.title(f'Calculated 1-RM for {exercise}')
    plt.xlabel('Date')
    plt.ylabel('Weight [kg]')
    plt.gcf().autofmt_xdate()
    plt.show()


def exercise_format(dataframe):
    """ Formats the available exercises and prints it for selection"""
    exercise_list = list(dataframe['Exercise Name'].unique())
    print(f"---------- The full list of available exercises: -------")
    for i in range(len(exercise_list)):
        print(f"{exercise_list[i]}")
    #print(exercise_list)


def main():
    workouts_between_dates(cleaned, '2022-08-01', '2023-01-15')
    number_of_exercises(cleaned, '2022-08-01', '2023-01-15')
    exercise_format(cleaned)
    exercise = input("Choose an exercise to view: ")
    max_list = (one_rep_max_exercise(cleaned, exercise))
    plot_max(max_list, exercise)
    


if __name__ == "__main__":
    main()