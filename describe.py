import numpy as np
import sys
import csv
from math import sqrt, trunc
import pandas as pd


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
                    i = 0
                    for item in row:
                        if not str(item):
                            features[titles[i]].append(np.nan)
                        else:
                            features[titles[i]].append(item)
                        i += 1
                    i = 0
    except FileNotFoundError:
        return -1
    return features


def delete_non_num(features):
    features_to_delete = []
    correct_features = []
    for key in features:
        try:
            for i in range(len(features[key])):
                float_val = float(features[key][i])
                if not np.isnan(float_val):
                    correct_features.append(key)
                    break
                if i == len(features[key]) - 1:
                    features_to_delete.append(key)
        except:
            features_to_delete.append(key)
    for i in features_to_delete:
        features.pop(i)
    return features, correct_features


def count(list):
    sum = 0
    for i in list:
        if not np.isnan(i):
            sum += 1
    sum = round(sum, 6)
    return sum


def collect_count(features):
    count_list = []
    for key in features:
        count_list.append(count(features[key]))
    return count_list


def collect_mean(features, count):
    mean_list = []
    sum = 0
    index = 0
    for key in features:
        _len = len(features[key])
        for item in features[key]:
            if not np.isnan(item):
                sum += item
        mean_list.append(round(sum / count[index], 6))
        index += 1
        sum = 0
    return mean_list


def collect_std(features, _mean, _count):
    std_list = []
    m = 0
    squad_sum = 0
    for key in features:
        for item in features[key]:
            if not np.isnan(item):
                squad_sum += (item - _mean[m]) ** 2
        dispersion = squad_sum / (_count[m] - 1)
        squad_sum = 0
        std_list.append(round(sqrt(dispersion), 6))
        m += 1
    return std_list


def collect_min(features):
    min_list = []
    for key in features:
        _min = float('inf')
        for item in features[key]:
            if not np.isnan(item):
                _min = item if _min > item else _min
        min_list.append(round(float(_min), 6))
    return min_list


def collect_max(features):
    max_list = []
    for key in features:
        _max = float('-inf')
        for item in features[key]:
            if not np.isnan(item):
                _max = item if _max < item else _max
        max_list.append(round(float(_max), 6))
    return max_list


def collect_quartiles(features, percent):
    quartiles_list = []
    for key in features:
        _len = len(features[key])
        quartiles_list.append(round(percent / 100 * (_len + 1), 6))
    return quartiles_list


def create_template(_list, _title):
    template = '{0:' + '' + ".6f"
    return template


def print_info(type_data, type, templates):
    print('\033[41m%-5s\033[0m' % (type), end='')
    m = 0
    for item in type_data:
        print(templates[m].format(item), end='')
        m += 1
    print()


def create_table(features, features_list):
    _count = collect_count(features)
    _mean = collect_mean(features, _count)
    _std = collect_std(features, _mean, _count)
    _min = collect_min(features)
    _max = collect_max(features)
    _q25 = collect_quartiles(features, 25)
    _q50 = collect_quartiles(features, 50)
    _q75 = collect_quartiles(features, 75)
    print('\033[41m%-5s\033[0m' % "", end='')

    max_len = 0
    templates = []
    for count, mean, std, min, q25, q50, q75, max, feature \
        in zip(_count,_mean,_std,_min,_q25,_q50,_q75,_max, features_list):
        max_len = len(str(trunc(count))) + 7 if len(str(trunc(count))) + 7 > max_len else max_len
        max_len = len(str(trunc(mean))) + 7 if len(str(trunc(mean))) + 7 > max_len else max_len
        max_len = len(str(trunc(std))) + 7 if len(str(trunc(std))) + 7 > max_len else max_len
        max_len = len(str(trunc(min))) + 7 if len(str(trunc(min))) + 7 > max_len else max_len
        max_len = len(str(trunc(q25))) + 7 if len(str(trunc(q25))) + 7 > max_len else max_len
        max_len = len(str(trunc(q50))) + 7 if len(str(trunc(q50))) + 7 > max_len else max_len
        max_len = len(str(trunc(q75))) + 7 if len(str(trunc(q75))) + 7 > max_len else max_len
        max_len = len(str(trunc(max))) + 7 if len(str(trunc(max))) + 7 > max_len else max_len
        max_len = len(feature) if len(feature) > max_len else max_len
        max_len += 2
        t = '{0:>' + str(max_len) + "s}"
        print(t.format(feature), end='')
        templates.append('{0:' + str(max_len) + ".6f}")
        max_len = 0
    print()
    print_info(_count, 'count',templates)
    print_info(_mean, 'mean',templates)
    print_info(_std, 'std',templates)
    print_info(_min, 'min',templates)
    print_info(_q25, '25%',templates)
    print_info(_q50, '50%',templates)
    print_info(_q75, '75%',templates)
    print_info(_max, 'max',templates)


def to_float(features):
    float_features = {}
    for key in features:
        float_features[key] = []
        for value in features[key]:
            try:
                float_features[key].append(float(value))
            except:
                float_features[key].append(np.nan)
    return float_features


def main(filePath):
    features = read_csv(filePath)
    numerical_features, list_of_numerical_features = delete_non_num(features)
    numerical_features = to_float(numerical_features)
    create_table(numerical_features, list_of_numerical_features)
    df = pd.read_csv(filePath)
    print(df.describe())


if __name__ == "__main__":
    # if len(sys.argv) == 2:
    #     main(sys.argv[1])
    # else:
    #     print("Wrong number of arguments!")
    main("./dataset_train.csv")
