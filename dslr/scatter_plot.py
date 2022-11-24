import matplotlib.pyplot as plt
from numpy import isnan
import pandas as pd
from os.path import isfile
import numpy as np

def read_csv(csvFile):
    df = pd.read_csv(
            csvFile,
            usecols=[1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        )
    return df


def     get_df_houses(filename):
    if not isfile(filename):
        print('ERROR: File not Found!')
        exit(1)
    df = read_csv(filename)
    df_houses = {}
    df_houses['G'] = df[df['Hogwarts House'] == 'Gryffindor']
    df_houses['H'] = df[df['Hogwarts House'] == 'Hufflepuff']
    df_houses['S'] = df[df['Hogwarts House'] == 'Slytherin']
    df_houses['R'] = df[df['Hogwarts House'] == 'Ravenclaw']
    return df_houses


def     get_house_courses(df_houses, house, course1, course2):
    col1 = df_houses[house].loc[:, course1]
    col2 = df_houses[house].loc[:, course2]
    indexs = [(~isnan(x) and ~isnan(y)) for x, y in zip(col1, col2)]
    courses = {
        course1: list(col1[indexs]),
        course2: list(col2[indexs]),
    }
    return courses



def display(df_houses, f1=3, f2=4):
    course1 = df_houses['R'].columns[f1]
    course2 = df_houses['R'].columns[f2]
    figure = plt.figure(figsize=(10,8))
    figure.canvas.set_window_title(f'Scatter of the courses  " {course1} " and " {course2} "')
    courses = get_house_courses(df_houses, 'R', course1, course2)
    plt.scatter(
        courses[course1],
        courses[course2],
        alpha=0.4,
        color='#0000FF',
        label='Ravenclaw',
    )
    courses = get_house_courses(df_houses, 'H', course1, course2)
    plt.scatter(
        courses[course1],
        courses[course2],
        alpha=0.5,
        color='#CCCC00',
        label='Hufflepuff',
    )
    courses = get_house_courses(df_houses, 'G', course1, course2)
    plt.scatter(
        courses[course1],
        courses[course2],
        alpha=0.4,
        color='#FF0000',
        label='Gryffindor',
    )
    courses = get_house_courses(df_houses, 'S', course1, course2)
    plt.scatter(
        courses[course1],
        courses[course2],
        alpha=0.4,
        color='#00FF00',
        label='Slytherin',
    )
    plt.title(f'Scatter "{course1}" with "{course2}"')
    plt.legend(loc='upper right')
    plt.ylabel(course2)
    plt.xlabel(course1)
    plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
    plt.show()


def scatter(f1=2, f2=3):
    data = get_df_houses('./dataset_train.csv')
    display(data, f1, f2)


if __name__ == '__main__':
    scatter()



