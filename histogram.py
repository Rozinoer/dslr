import matplotlib.pyplot as plt
import numpy as np
import csv
from datetime import datetime


def read_csv(filePath):
    features = {}
    flag = 1
    titles = []
    try:
        with open(filePath, 'r', newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in data:
                if flag:
                    flag = 0
                    titles = row
                    for item in row:
                        features[item] = []
                else:
                    i = 0
                    for item in row:
                        if not str(item):
                            features[titles[i]].append(np.nan)
                        else:
                            features[titles[i]].append(item)
                        i += 1
    except FileNotFoundError:
        return -1
    return features


def get_datarow_by_index(data, index, titles):
    row = {}
    for i in titles:
        row[i] = data[i][index]
    return row


def data_by_house(course_data):
    houses = {
        "Ravenclaw": 0,
        "Slytherin": 0,
        "Gryffindor": 0,
        "Hufflepuff": 0
    }
    for item in course_data:
        score = 0
        for key in item:
            if key != "Hogwarts House" and key != "Birthday":
                if not np.isnan(float(item[key])):
                    value = float(item[key])
                    score += value
        houses[item["Hogwarts House"]] += score
    for key in houses:
        houses[key] = round(houses[key], 2)
    return houses


def data_by_course(data):
    titles = []
    courses = {
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
    }
    for key in data:
        titles.append(key)
    titles.remove("Index")
    titles.remove("First Name")
    titles.remove("Last Name")
    titles.remove("Best Hand")
    for i in range(0, 1600):
        row = get_datarow_by_index(data, i, titles)
        birthday_year = datetime.strptime(row['Birthday'], "%Y-%m-%d").year
        courses[2001 - birthday_year + 1].append(row)
    houses_score = []
    houses_score.append(data_by_house(courses[1]))
    houses_score.append(data_by_house(courses[2]))
    houses_score.append(data_by_house(courses[3]))
    houses_score.append(data_by_house(courses[4]))
    houses_score.append(data_by_house(courses[5]))
    houses_score.append(data_by_house(courses[6]))
    for i in houses_score:
        print(i)
    # n, bins, patches = plt.hist(data)
    #
    # plt.xlabel('Smarts')
    # plt.ylabel('Probability')
    # plt.title('Histogram of IQ')
    # plt.xlim(0, 10)
    # plt.ylim(0, 10)
    # plt.grid(True)
    # plt.show()


def histogram():
    data = read_csv('./dataset_train.csv')
    data_by_course(data)


if __name__ == '__main__':
    histogram()
