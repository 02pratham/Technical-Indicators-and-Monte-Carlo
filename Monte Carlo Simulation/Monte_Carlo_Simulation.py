#Monte_Carlo_Simulation
import numpy as np
import pandas
import matplotlib
import math
import csv


timesteps = 30
starting_price = 600
volatility = 0.02
max_simulations = 5000


std_dev = volatility


#expected returns of 0%
expected_returns = 0
expected_price = starting_price*(1+expected_returns)

day_price = np.zeros((max_simulations,31))

for i in range(0,max_simulations):
    day_price[i][0]=600
#print(day_price)



#calculating the simulation values
for i in range(0,max_simulations):
    price = starting_price
    for day in range(1,31):
        var = expected_returns*day
        var1 = std_dev*np.random.randn()*math.pow(day,0.5)
        change = price*(var + var1)
        day_price[i][day]= price + change

day_price=day_price.transpose()
#print(day_price)



#creating csv file
df = pandas.DataFrame(day_price)
df.reset_index(drop=True,inplace=True)
df.to_csv('task3main.csv',index_label='day')
#print(df)


#calculating the occurance values
occurance = np.zeros(int(np.amax(day_price))+1,float)
for j in range(0,max_simulations):
    occurance[int(day_price[30][j])]= 1 + occurance[int(day_price[30][j])]


#creating csv file for occurance value
df2= pandas.DataFrame(occurance)
df2.reset_index(drop=True,inplace=True)
df2.to_csv('bell_curve.csv')



