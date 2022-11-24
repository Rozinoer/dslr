import matplotlib.pyplot as plt
from numpy import isnan
import pandas as pd
from os.path import isfile


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


def display(data):
    figure = plt.figure(figsize=(13,9))
    figure.subplots_adjust(hspace=.5)
    # figure.canvas.set_window_title('Histogram of each course')
    ax = []
    i = 0
    for col in list(data['G'].columns)[1:]:
        ax.append(figure.add_subplot(4,4,i + 1))

        myarray = data['R'].loc[:, col]
        myarray = myarray[~isnan(myarray)]
        ax[i].hist(
            myarray,
            alpha=0.4,
            bins='auto',
            color='#0000FF',
            label='Ravenclaw',
        )

        myarray = data['H'].loc[:, col]
        myarray = myarray[~isnan(myarray)]
        ax[i].hist(
            myarray,
            alpha=0.5,
            bins='auto',
            color='#CCCC00',
            label='Hufflepuff',
        )

        myarray = data['G'].loc[:, col]
        myarray = myarray[~isnan(myarray)]
        ax[i].hist(
            myarray,
            alpha=0.4,
            bins='auto',
            color='#FF0000',
            label='Gryffindor',
        )

        myarray = data['S'].loc[:, col]
        myarray = myarray[~isnan(myarray)]
        ax[i].hist(
            myarray,
            alpha=0.4,
            bins='auto',
            color='#00FF00',
            label='Slytherin',
        )

        ax[i].set_title(col)
        i+=1
    plt.legend(
        bbox_to_anchor=(1.5,1),
        loc='upper left',
        borderaxespad=0
    )

    # plt.show()



def histogram(filename):
    data = get_df_houses(filename)
    display(data)


if __name__ == '__main__':
    filename = 'dslr/dataset_train.csv'
    histogram(filename)
