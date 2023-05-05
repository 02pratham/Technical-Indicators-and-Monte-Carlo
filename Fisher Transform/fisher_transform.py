#fisher transform indicator
import numpy as np
import pandas
import matplotlib as mt
import csv
import math

'''all the values are calculated through formulaes given in investopedia site'''


#storing the useful data into lists from stock_prices.csv
with open('stock_prices.csv','r') as file:
    csvfile = csv.reader(file)
    csvfile = list(csvfile)
    closing=[]
    j=0
    for i in csvfile:
        if j==0:
            j=1
            continue
        else:            
            closing.append(i[4])

#converting the list into the float type array
closing = np.array(closing, float)

#claculating the maximum and the minimum  in 9 days period
days = closing.size
max_9=[]
min_9=[]

for i in range(0,days-9,9):
    maximum=closing[i]
    minimum=closing[i]
    for j in range(0,9):
        if closing[i+j]<minimum:
            minimum = closing[i+j]
        if closing[i+j]>maximum:
            maximum = closing[i+j]
    max_9.append(maximum)
    min_9.append(minimum)
# print(max_9)
# print(min_9)


#converitng all the values into range of -1 to 1
#formula for converting all values in range of -1 to 1
# OldRange = (OldMax - OldMin)  
# NewRange = (NewMax - NewMin)  
# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

fisher=[]
itr = 0
for i in range(0,days-9,9):
    for j in range(0,9):
        new_value = (((closing[i+j]-min_9[itr])*2)/(max_9[itr]-min_9[itr]))-1
        fisher.append(new_value)
    itr = itr+1
#print(fisher)

final_fisher = []
for X in fisher:
    value = (1+X)/(1-X)
    if value:
        final_fisher.append(math.log(value))
    else: 
        final_fisher.append(100000)


#claculation of fisher transform values
fisher_transform = []
j=0
for i in final_fisher:
    if j==0:
       fisher_transform.append(i)
       j = j+1
    elif final_fisher[j] == 100000:
        fisher_transform.append(100000)
        j=j+1
    elif math.isinf(final_fisher[j]):
       final_fisher[j]=100000
       fisher_transform.append(100000)
       j = j+1
    elif final_fisher[j-1] == 100000:
        k=j
        while k:
            if final_fisher[k] == 100000:
                k=k-1
                continue
            else:
                break
        fisher_transform.append(final_fisher[j]+final_fisher[k])
        j=j+1
    else:
        fisher_transform.append(final_fisher[j]+final_fisher[j-1])
        j=j+1
fisher_transform.append(100000)      
j=0
for i in fisher_transform:
    if i == 100000 and j!=0:
        fisher_transform[j]=fisher_transform[j-1]
        j=j+1
    else:
        j=j+1
#print(fisher_transform,len(fisher_transform))

#moving average(calculation of trigger values) 
mv_avg=[]
for i in range(0,days-3,3):
    avg_sum=0
    for j in range(0,3):
        avg_sum=avg_sum+fisher_transform[i+j]
    for j in range(0,3):
        mv_avg.append(avg_sum/3)
mv_avg.append(avg_sum/3)





#sending the data to the csv file along with stock price data
df = pandas.read_csv('stock_prices.csv')
df.insert(7,column='Fisher_Transform',value=fisher_transform)
df.insert(8,column='Trigger',value=mv_avg)
df.to_csv('task1.csv', index = False)
df.Close

