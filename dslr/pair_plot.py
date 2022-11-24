import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys

class   bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def     pair_plot():
    # Read dataframe from the CSV file
    df = pd.read_csv(
        'dataset_train.csv',
        # Columns to include
        usecols=[1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    )
    # Houses color palette
    houses_palette = {
        'Gryffindor':'#FF0000',
        'Ravenclaw':'#0000FF',
        'Hufflepuff':'#CCCC00',
        'Slytherin':'#00FF00',
    }
    # Set the theme of the subplots
    sns.set_theme(font_scale=0.52)
    # Pair Plot using 'Seaborn'
    sns.pairplot(
        data= df,
        #diag_kind="hist",
        hue= "Hogwarts House",
        palette= houses_palette,
        plot_kws= {
            'alpha':0.4,
            's': 5
        },
        height= 1.1,
    )
    # Show
    plt.show()


# Launch program
pair_plot()