

""" Module with useful function for analysis of strong data"""

import pandas as pd
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


def one_rep_max_exercise(dataframe, exercise, start_date, end_date):
    """ Applies the one_rep_max_row function to every row in a dataframe
        with the exercise name 'exercise', and then returns a list of the result.
    """ 
    df_exercise = get_date_range(dataframe, start_date, end_date)
    df_exercise = df_exercise[df_exercise['Exercise Name'] == exercise]
    
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


def get_weekly_workouts(dataframe, start_date, end_date):
    new_df = get_date_range(dataframe, start_date, end_date)
    new_df['Date'] = pd.to_datetime(new_df['Date'])
    new_df['week_start'] = new_df['Date'].dt.to_period('W').dt.start_time
    new_df = new_df.drop_duplicates(subset = 'Date') # Drops the duplicate dates
    new_df['week_start'] = new_df['week_start'].dt.strftime('%Y-%m-%d')
    #new_df.set_index('week_start')
    series = new_df['week_start'].value_counts().sort_index() # Sorts by the dates
    return series

print(cleaned)