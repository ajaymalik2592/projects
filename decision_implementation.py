import numpy as np
import math
import csv
import random

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


""" here onward analysis part on decision tree of the project, data set in list form easy to compute """
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


distributed, min_max, gain = [], [], []
for x in range(cols ):
    distributed.append([0, 0])
    min_max.append([100, 0])
    if(cols-1 == x):
        break
    gain.append([1, 0, 0])

test_rows = 170

for x in range(int(test_rows)):
    for y in range(cols ):
        if(y != cols-1):
            distributed[y][formated_data[x][-1]] += formated_data[x][y]

            min_max[y][0] = min(min_max[y][0], formated_data[x][y])

            min_max[y][1] = max(min_max[y][1], formated_data[x][y])

        else:
            distributed[ y ][formated_data[x] [ -1 ] ]  += 1

matels_in_test = distributed[cols-1][1]
solid_in_test = distributed[cols -1][0]

def gain_ratio(di):
    r = 0


    if(di[0][0] == 0 or di[0][1] == 0):
        pass
    else:
        r -= di[0][0] * math.log( di[0][0]/ (di[0][0] + di[0][1]) , 2)  + di[0][1] * math.log(di[0][1]/ (di[0][0] + di[0][1]) , 2)

    if(di[1][0] ==0 or di[1][1] == 0):
        pass
    else:
        r -= di[1][0] * math.log( di[1][0]/ (di[1][0] + di[1][1]) , 2)  + di[0][1] * math.log(di[1][1]/ (di[1][0] + di[1][1]) , 2)

    p1 = sum(di[0])
    p2 = sum(di[1])
    print(p1 , " " , p2)
    total = p1 + p2
    p = 0
    if(p1 != 0):
        p -= p1 * math.log(p1 / total , 2)
    if(p2 != 0):
        p -=p2 * math.log(p2 / total,2 )
    if(p == 0):
        return r * pow(10,100)
    return (r / test_rows) / p

for x in range(cols -1):
    l = min_max[x][0]
    r = min_max[x][1]
    i = l * 10000
    temp = []

    while(i <= 10000 * r):

        mid = i / 10000
        i += 1
        divided = [[0, 0], [0, 0]]
        for y in range(test_rows):
            if(formated_data[y][x] >= mid):
                divided[1][formated_data[y][-1]] += 1
            else:
                divided[0][formated_data[y][-1]] += 1
        temp.append( [gain_ratio(divided), mid] )
    i = 100000
    index = 0
    for xx in temp:
        if(xx[0] < i):
            i = xx[0]
            index = xx[1]
    gain[x][0], gain[x][1], gain[x][2] = i, x,  index


i = 0

equalize = 0
for x in gain:
    equalize = max(equalize, x[0])


final_weighted_for_decisiontree = []

for x in range(cols - 1 ):
    final_weighted_for_decisiontree.append([ equalize / gain[x][0] ,gain[x][2] ] )

print(final_weighted_for_decisiontree)
i = 0



aa = ['R', 'M']
tr = 0
tp , fn , fp , tn = 0 ,0, 0, 0
output = []
for index in range(170, 207):
    i = 1
    j = 1
    for x in range(cols -1):
        if(formated_data[index][x] >= final_weighted_for_decisiontree[x][1]):
            i *= final_weighted_for_decisiontree[x][0]
        else:
            j *= final_weighted_for_decisiontree[x][0]
    if i < j :
        if("R" == aa[formated_data[index][-1]] ):
            tn += 1
            tr += 1
            output.append(1)
        else : fp += 1; output.append(0)
    else:
        if("M" == aa[formated_data[index][-1]]):
            tr += 1
            tp += 1
            output.append(1)
        else : fn += 1; output.append(0)

print(output)
print(tp, fn)
print(fp, tn)
print(tr  * 100/ (207 - 171))