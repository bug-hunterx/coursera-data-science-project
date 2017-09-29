import csv
import numpy as np
import os
from sklearn import datasets, linear_model


def read_production():
    file = open('south-korea-stats.csv')
    reader = csv.reader(file, delimiter=',')
    result = {}
    for row in reader:
        if "Rice (Paddy Equivalent)" in row[3]:
            result[int(row[5])] = float(row[7])
    return result


def get_vhi_mean(csv_result, index, year):
    total = 0
    week_count = 0
    for file in csv_result:
        if year in file:
            value = csv_result[file][index]
            if value > 0:
                week_count = week_count + 1
                total = total + value
    return total / week_count


def load_csv(file_path):
    file = open(file_path, 'r')
    reader = csv.reader(file)
    result = []
    for row in reader:
        value = float(row[2])
        if value < 0:
            value = -1
        result.append(value)
    return result


def load_all_csv():
    result = {}
    dir = 'data'
    files = os.listdir(dir)
    for file in files:
        if '.csv' in file:
            result[file] = load_csv(os.path.join(dir, file))
    return result


all_csv_result = load_all_csv()


def read_vhi(year_start=1982, year_end=2013):
    result = {}
    for i in range(year_start, year_end):
        result[i] = {}
        result[i]['vhi'] = []
        year_str = str(i)
        for j in range(0, 8273):
            mean = get_vhi_mean(all_csv_result, j, year_str)
            result[i]['vhi'].append(mean)
    return result


def merge_vhi_production(vhi, production):
    for year in vhi:
        if year in production:
            vhi[year]['production'] = production[year]
    return vhi


def get_lr_train(result):
    y = []
    x = []
    years = result.keys()
    years = sorted(years)
    for year in years:
        y.append(np.asarray([result[year]['production']]))
        x.append(np.asarray(result[year]['vhi']))
    return np.asarray(x), np.asarray(y)


production = read_production()
vhi = read_vhi()
result = merge_vhi_production(vhi, production)
x, y = get_lr_train(result)
lr = linear_model.LinearRegression()
lr.fit(x,y)
coeff=lr.coef_[0]
np.savez('coeff.npz',coeff=coeff)
print(result)
