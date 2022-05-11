import sys
import csv
from math import sqrt


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


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
                    for item in row:
                        features[titles[row.index(item)]].append(item)
    except FileNotFoundError:
        return -1
    return features


def delete_non_num(features):
    features_to_delete = []
    correct_features = []
    for key in features:
        try:
            float(features[key][0])
            correct_features.append(key)
        except:
            features_to_delete.append(key)
    for i in features_to_delete:
        features.pop(i)
    return features, correct_features


def count(list):
    sum = 0.0
    for i in list:
        if not str(i):
            sum += 0
        else:
            sum += float(i)
    sum = round(sum, 6)
    return sum


def collect_count(features):
    count_list = []
    for key in features:
        count_list.append(count(features[key]))
    return count_list
    # print('{:^10}'.format(""), end='')
    # for i in features_list:
    #     width = len(i) if len(i) > len(count_list[features_list.index(i)]) else len(count_list[features_list.index(i)])
    #     width += 2
    #     print(i.center(width), end='')
    #     width_list.append(width)
    # print()
    # print('{:^10}'.format("Count"), end='')
    # for i in count_list:
    #     print(i.center(width_list[count_list.index(i)]), end='')
    # print()


def collect_mean(features, _count):
    mean_list = []
    m = 0
    for key in features:
        _len = len(features[key])
        mean_list.append(round(_count[m] / _len, 6))
        m += 1
    return mean_list


def collect_std(features, _mean):
    std_list = []
    m = 0
    squad_sum = 0
    for key in features:
        for item in features[key]:
            if not str(item):
                squad_sum += (0.0 - _mean[0]) ** 2
            else:
                squad_sum += (float(item) - _mean[0]) ** 2
        std_list.append(round(sqrt(squad_sum / _mean[0]), 6))
        m += 1
    return std_list


def collect_min(features):
    min_list = []
    for key in features:
        _min = features[key][0]
        for item in features[key]:
            _min = item if _min > item else _min
        if not str(_min):
            min_list.append(0.0)
        else:
            min_list.append(round(float(_min), 6))
    return min_list


def collect_max(features):
    max_list = []
    for key in features:
        _max = features[key][0]
        for item in features[key]:
            _max = item if _max < item else _max
        if not str(_max):
            max_list.append(0.0)
        else:
            max_list.append(round(float(_max), 6))
    return max_list


def collect_quartiles(features, percent):
    quartiles_list = []
    for key in features:
        _len = len(features[key])
        quartiles_list.append(round(percent / 100 * (_len + 1), 6))
    return quartiles_list


def create_table(features, features_list):
    _count = collect_count(features)
    _mean = collect_mean(features, _count)
    _std = collect_std(features, _mean)
    _min = collect_min(features)
    _max = collect_max(features)
    _q25 = collect_quartiles(features, 25)
    _q50 = collect_quartiles(features, 50)
    _q75 = collect_quartiles(features, 75)


# def empty_to_zero(numerical_features):
#     _features = []
#     for key in numerical_features:
#         print(numerical_features[key])
#         for i in numerical_features[key]:
#             if not str(i):
#                 numerical_features[key][i] = '0'
#                 print(numerical_features[key][i])
#     return _features


def main(filePath):
    features = read_csv(filePath)
    numerical_features, list_of_numerical_features = delete_non_num(features)
    # empty_to_zero(numerical_features)
    create_table(numerical_features, list_of_numerical_features)


if __name__ == "__main__":
    # if len(sys.argv) == 2:
    #     main(sys.argv[1])
    # else:
    #     print("Wrong number of arguments!")
    main("./dataset_train.csv")
