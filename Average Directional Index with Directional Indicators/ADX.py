#Average Directional Index
import numpy as np
import pandas 
import matplotlib as mp
import csv
import math

'''all the values are calculated through formula given in investopedia site'''

#storing the values of data to be used in lists
with open('stock_prices.csv') as file:
    csvfile = list(csv.reader(file))
    #print(csvfile)
    high=[]
    low=[]
    closing=[]
    j=0
    for i in csvfile:
        if j==0:
            j=j+1
        else:
            closing.append(i[4])
            high.append(i[2])
            low.append(i[3])

closing = np.array(closing,float)
high = np.array(high,float)
low = np.array(low,float)
# print(high,len(high))
# print(low,len(low))


#calculating vlues for +DM and -DM
dm_plus=[]
dm_minus=[]
tr=[0]
j=0
for i in range(0,len(high)-1):
    upmove = high[j+1]-high[j]
    downmove = low[j]-low[j+1]
    if upmove>0 and upmove>downmove:
        dm_plus.append(upmove)
    else:
        dm_plus.append(0)
    if downmove>0 and downmove>upmove:
        dm_minus.append(downmove)
    else:
        dm_minus.append(0)
    j=j+1

#print(dm_minus,len(dm_minus))
#print(dm_plus,len(dm_plus))
j=1
for i in range(1,len(high)):
    var1 = high[j]-low[j]
    var2= high[j]-closing[j-1]
    var3= low[j]-closing[j-1]
    if var1>var2:
        if var1>var3:
            tr.append(var1)
        else:
            tr.append(var3)
    else:
        if var2>var3:
            tr.append(var2)
        else:
            tr.append(var3)
    j=j+1

#(tr,len(tr))

#smoothing the values for +DM,-DM and true range
#period for smoothing 14 days
smoothdm_plus=[]
smoothdm_minus=[]
smooth_tr=[]

sum1=0
sum2=0
sum3=0
for j in range(0,14):
    sum1=sum1+dm_minus[j]
    sum2=sum2+dm_plus[j]
    sum3=sum3+tr[j]
for i in range(0,14):
    smoothdm_minus.append(sum1/14)
    smoothdm_plus.append(sum2/14)
    smooth_tr.append(sum3/14)

# print(smoothdm_minus,len(smoothdm_minus))
# print(smoothdm_plus,len(smoothdm_plus))
# print(smooth_tr,len(smooth_tr))

for i in range(14,len(high)-1):
    var =(13*smoothdm_minus[i-1] + dm_minus[i])/14
    smoothdm_minus.append(var)
    var =(13*smoothdm_plus[i-1] + dm_plus[i])/14
    smoothdm_plus.append(var)

# print(smoothdm_minus,len(smoothdm_minus))
# print(smoothdm_plus,len(smoothdm_plus))



#calculting the average true range
#avg true range
avg_tr=0
for i in tr:
    avg_tr=avg_tr+i

avg_tr = avg_tr/len(tr)
#print(avg_tr)


#calculating the +/-directional index
#directional index 
plus_DI=[]
minus_DI=[]
Dx=[]
for i in range(0,len(smoothdm_minus)):
    plus_DI.append((smoothdm_plus[i]/avg_tr)*100)
    minus_DI.append((smoothdm_minus[i]/avg_tr)*100)
    
#print(plus_DI,len(plus_DI))
#print(minus_DI,len(minus_DI))

for i in range(0,len(smoothdm_minus)):
    if plus_DI>minus_DI:
        Dx.append((abs(plus_DI[i]-minus_DI[i])/abs(plus_DI[i]+minus_DI[i]))*100)
    else:
        Dx.append((abs(minus_DI[i]-plus_DI[i])/abs(plus_DI[i]+minus_DI[i]))*100)

#print(Dx,len(Dx))


#calculatin final #ADX VALUES
#average directional index
avg_Dx=[]
var=0
for i in range(0,14):
    var=var+Dx[i]
avg_Dx.append(var/14)
for i in range(1,len(Dx)):
    avg_Dx.append(((13*avg_Dx[i-1])+Dx[i])/14)

# print(avg_Dx,len(avg_Dx))
avg_Dx.append(np.NaN)
plus_DI.append(np.NaN)
minus_DI.append(np.NaN)

df=pandas.read_csv('stock_prices.csv')
df.insert(7,column='ADX',value=avg_Dx)
df.insert(8,column='Plus_DI',value=plus_DI)
df.insert(9,column='Minus_DI',value=minus_DI)
df.to_csv('task2.csv',index=False)
df.Close