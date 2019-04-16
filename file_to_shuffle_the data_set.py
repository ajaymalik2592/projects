import csv
from random import shuffle

da = open('Sonar.csv','rt')

data = open('shuffled_data.csv', 'w+')


da1 = da.readlines()
data1 = csv.writer(data)

listed_data = []

shuffle(da1)
print(da1)
for x in da1:

    data1.writerow(x.split(","))
    print(x)
data.close()
da.close()