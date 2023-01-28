

""" Program for visualizing training data from Strong using Streamlit"""

import pandas as pd
#import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as plt_date


df = pd.read_csv("strong.csv")

cleaned = df[["Date", "Workout Name", "Duration", "Exercise Name", "Set Order", "Weight", "Reps"]]
cleaned['Date'] = pd.to_datetime(cleaned['Date']).dt.strftime('%Y-%m-%d') # Fixes time format
cleaned['category'] = cleaned['Exercise Name'].str.extract(r'\((.*)\)', expand=False).fillna("Other")  # Creates exercise categories
cleaned['category'] = cleaned['category'].replace(
    {'machine': 'Machine',
    'Smith Machine': 'Barbell',
    'Cable - Straight Bar': 'Cable'})


def get_date_range(data_frame, start_date, end_date):
    """ Slices a dataframe between a start date and end date"""
    return data_frame[(data_frame["Date"] > start_date) & (data_frame["Date"] < end_date)]


def workouts_between_dates(data_frame, start_date, end_date):
    """ Takes a dataframe and two dates and prints the number
        of workouts between the dates.
    """
    date_range = get_date_range(data_frame, start_date, end_date)
    unique_dates = date_range['Date'].nunique()
    return unique_dates

def number_of_exercises(data_frame, start_date, end_date):
    """ Takes a dataframe and two dates and prints the number
        of unique exercises performed during that period.
    """
    date_range = get_date_range(data_frame, start_date, end_date)
    unique_exercises = date_range['Exercise Name'].nunique()
    return unique_exercises


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
    df_exercise = dataframe[dataframe['Exercise Name'] == exercise]
    print(df_exercise)
    max =  df_exercise[['Weight', 'Reps', 'Date']].apply(one_rep_max_row, axis=1)
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


def get_exercises(dataframe):
    """ Formats the available exercises and prints it for selection"""
    exercise_list = list(dataframe['Exercise Name'].unique())
    return exercise_list


def get_volume(row):
    """ Returns the product of weight, reps, sets, and exercises for a 
        time frame
    """
    weight = row['Weight']
    reps = row['Reps']
    return weight * reps


def total_volume(dataframe):
    """Returns the total volume for all exercises in a dataframe"""
    product =  dataframe[['Weight', 'Reps']].apply(get_volume, axis=1)
    return product


def workouts_per_week(dataframe):
    unique_dates = dataframe["Date"].drop_duplicates()
    unique_dates = pd.to_datetime(unique_dates)
    unique_dates = unique_dates.dt.week
    week_counts = unique_dates.value_counts()
    return week_counts

first_set = cleaned[cleaned['Set Order'] == 1]
second_set = cleaned[cleaned['Set Order'] == 2]



def main():
    workouts_between_dates(cleaned, '2022-08-01', '2023-01-15')
    number_of_exercises(cleaned, '2022-08-01', '2023-01-15')
    #print(cleaned.head())
    #print(total_volume(cleaned))
    #volume = total_volume(cleaned)
    #total_vol = sum(volume)
    #print(f'Total volume: {total_vol/1000:.1f}')
    #print(cleaned)
    #print(one_rep_max_exercise(cleaned, "Squat (Barbell)"))

    #print(cleaned)
    print(workouts_per_week(cleaned))
if __name__ == "__main__":
    main()