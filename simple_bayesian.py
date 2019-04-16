import numpy as np
import math
import csv


data = []

with open('shuffled_data.csv', "rt") as filereader:
    fil = csv.reader(filereader, delimiter= ' ' )
    for rows in fil:
        data.append(rows)

formated_data = []
i = 0
for da in data:
    if(i == 207):
        break
    i+=1
    da = da[0]
    da = da.split(",")
    data_new = []
    j  = 0
    for x in da:
        j+=1
        data_new.append(float(x))
        if( j == 60):
            break
    if(da[-1] == 'M'):
        data_new.append(1)
    else:
        data_new.append(0)
    formated_data.append(data_new)


rows = len(formated_data)
cols = len(formated_data[0])


""" here onward analysis part of the project, data set in list form easy to compute """
rock = 0
metal = 0
for x in formated_data:
    if(x[-1] == 0):
        rock += 1
    else:
        metal += 1


value = []
for x in range(cols - 1):
    value.append(0)

for x in range(rows):
    for y in range(cols - 1):
        value[y] += formated_data[x][y]

distributed , test_sample_labels = [],[0, 0]
for x in range(cols):
    distributed.append([0, 0])

test_rows = 170

for x in range(int(test_rows)):
    for y in range(cols ):
        if(y != cols-1):
            distributed[y][formated_data[x][-1]] += formated_data[x][y]
        else:
            distributed[ y ][formated_data[x] [ -1 ] ]  += 1

matels_in_test = distributed[cols-1][1]
solid_in_test = distributed[cols -1][0]


mean = []
standard_deviation = []

for x in range(cols - 1):
    mean.append([0, 0])
    standard_deviation.append([0, 0])

distributed = distributed[:-1]
index = 0
for x in distributed:
    mean[index][0] = distributed[index][0] / solid_in_test

    mean[index][1 ] = distributed[index]  [1] / matels_in_test

    index += 1


for x in range(int(test_rows)):

    for y in range(cols -1):

        standard_deviation[y][0] += pow(  mean[y][0] - formated_data[x][y], 2.0)

        standard_deviation[y][1] += pow(  mean[y][1] - formated_data[x][y], 2.0)

pi = math.pi
val = math.sqrt(2 * pi)
e  = math.e

def fun(a, b, c):
    return (pow(e, - (a- b)* (a- b) / (2 * c *c)) )/ (val * c)


for x in range(cols -1):
    standard_deviation[y][0] = math.sqrt(standard_deviation[y][0] / (solid_in_test - 1 ))

    standard_deviation[y][1] = math.sqrt(standard_deviation[y][1] / ( matels_in_test -1 ))

aa = ['R', 'M']

tp, fn , fp, tn = 0, 0, 0, 0
output = []
for index in range(170, 207):
    i = 1000000000
    j = 1000000000
    for x in range(cols -1):
        i *= fun(formated_data[index][x], mean[x][0], standard_deviation[x][0])
        j *= fun(formated_data[index][x], mean[x][1], standard_deviation[x][1])
    if i > j:
        if("R" == aa[formated_data[index][-1]] ):
            tn += 1
            output.append(1)
        else:
            fp += 1;output.append(0)

    else:
        if("M" == aa[formated_data[index][-1]]):
            tp += 1
            output.append(1)

        else:
            output.append(0)
            fn += 1
print(output)
print(tp , " ", fn)
print(fp , " ", tn)
print((tp + tn )* 100/ (207- 170) )