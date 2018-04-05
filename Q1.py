# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 10:37:33 2018

@author: William
"""

import numpy as np
import pandas as pd
import pylab as plt
from scipy.stats import norm, probplot
from matplotlib.ticker import FuncFormatter
#import matplotlib.dates as dates
#from matplotlib.dates import DateFormatter

#data = np.loadtxt(, delimiter=',', converters={0: dates.strpdate2num('%d-%b-%y')}, skiprows = 1)
headers = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
dtypes = {'Date': 'str', 'Open': 'float', 'High': 'float', 'Low': 'float', 'Close': 'float', 'Adj Close': 'float', 'Volume': 'int'}
parse_dates = ['Date']
df = pd.read_csv('DNL.L.csv', 
                 delimiter=',', 
                 header=0,
                 index_col=None,
                 dtype=dtypes, 
                 parse_dates=parse_dates)
df.info()
date = df.loc[:,"Date"].tolist()
adj_close = df.loc[:,"Adj Close"].tolist()

# Question 1(a)

k = 0
number_of_days = [1,4,9]
increment = [1,5,10]
increment_label = ["Daily Returns", "Five Day Returns", "Ten Day Returns"]
list_label = ["daily_returns", "five_day_returns", "ten_day_returns"]
for j in list_label:
    j = [0]
    for i in np.arange(number_of_days[k],len(adj_close)-1,increment[k]):
        returns = (adj_close[i]-adj_close[i-1]) / adj_close[i-1]
        j.append(returns)
    
    mu, std = norm.fit(j)
    
    fig, axes = plt.subplots(ncols=1, sharey=True)
    fig = plt.hist(j, bins=100, density=True)
    axes.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
    xmin,xmax = plt.xlim()
    plt.xlim(xmin,xmax)
    x = np.linspace(xmin,xmax,100)
    p = norm.pdf(x,mu,std)
    plt.plot(x,p,'k',linewidth=2) # This isn't correct but it's a start
    title = "Fit results: mu = %.5f,  std = %.3f" % (mu, std)
    plt.title(title)
    plt.show()

    probplot(j, plot=plt)
    plt.title("Probability Plot of " + increment_label[k])
    plt.xlim(-4,4)
    plt.ylim(-0.3,0.15)
    plt.show()
    
    k += 1
    
# Investigate change in the probability density function.
    
# Question 1(b)

daily_returns=[0]
for i in np.arange(1,len(adj_close)-1):
    returns = (adj_close[i]-adj_close[i-1])/adj_close[i-1]
    daily_returns.append(returns)

#adj_close = adj_close[-365:]

# variance can be estimated by sigma = s / sqrt(delta_t)
u = [0]
for i in np.arange(1,len(adj_close)-1):
    if adj_close[i] != 0:
        u.append(np.log(adj_close[i])/np.log(adj_close[i-1])) # logarithm of the returns
    else:
        u.append(0)
        
j = 0
sixty_day_rolling_average_u = []
sixty_day_rolling_average_s = []
for i in range(len(daily_returns)-60):
    sixty_day_rolling_average_u.append(np.mean(u[(0+j):(60+j)]))
    sixty_day_rolling_average_s.append(np.mean(adj_close[(0+j):(60+j)]))
    j += 1
    
sixty_day_rolling_average_dates = []
for i in range(len(daily_returns)-60):
    sixty_day_rolling_average_dates.append(date[i+60]) 

s_list = []
delta_t = 1/240 # for 60 day rolling average??? OR howabout you take the average of the first 60 days, and propagate forwards from there, so each increment it's the average of the next 60 bins+1
for i in range(len(daily_returns)-60):
    s_squared = (1/(60-1))*(sum(np.square(np.array(u[i:(i+60)])))-(1/60)*(sum(np.array(u[i:(i+60)]))**2))
    s_list.append(np.sqrt(s_squared))

sigma = (np.array(s_list)/np.sqrt(delta_t)).tolist() 

drift_list = []
for i in range(len(daily_returns)-60):
    drift = np.mean(u[i:(i+60)])/delta_t+sigma[i]**2/2
    drift_list.append(drift)

fig, ax = plt.subplots()
ax.plot(sixty_day_rolling_average_dates,sigma)
plt.title("60 Day Rolling Average of Volatility")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.xlim(sixty_day_rolling_average_dates[0],sixty_day_rolling_average_dates[7566])
plt.ylim(0,0.2)
plt.show()

fig, ax = plt.subplots()
plt.plot(sixty_day_rolling_average_dates,drift_list)
plt.title("60 Day Rolling Average of Drift")
plt.xlabel("Date")
plt.ylabel("Drift")
plt.xlim(sixty_day_rolling_average_dates[0],sixty_day_rolling_average_dates[7566])
plt.show()

# =============================================================================
# sigma = []
# for i in range(len(daily_returns)-60):   
#     MAD = 1.4826*np.median(abs(sixty_day_rolling_average_u[i]-np.median(sixty_day_rolling_average_u)))
#     sigma.append(np.sqrt(MAD))
# 
# plt.plot(sigma)
# plt.show()
# =============================================================================

# =============================================================================
# drift = np.median(sixty_day_rolling_average_u)/delta_t+np.array(sigma)**2/2
# 
# fig, ax = plt.subplots()
# ax.plot(sixty_day_rolling_average_dates,sigma)
# plt.title("60 Day Rolling Average of Volatility")
# plt.xlabel("Date")
# plt.ylabel("Volatility")
# #fig.autofmt_xdate()
# #ax.xaxis.set_ticks(sixty_day_rolling_average_dates)
# #ax.xaxis.set_major_formatter(dates.DateFormatter('\n\n\n%b\n%Y'))
# plt.xlim(sixty_day_rolling_average_dates[0],sixty_day_rolling_average_dates[7566])
# plt.ylim(0,57000)
# plt.show()
# =============================================================================

# =============================================================================
# fig, ax = plt.subplots()
# plt.plot(sixty_day_rolling_average_dates,drift)
# plt.title("60 Day Rolling Average of Drift")
# plt.xlabel("Date")
# plt.ylabel("Drift")
# #fig.autofmt_xdate()
# #ax.xaxis.set_ticks(np.array(sixty_day_rolling_average_dates))
# plt.xlim(sixty_day_rolling_average_dates[0],sixty_day_rolling_average_dates[7566])
# plt.ylim(0,1.6e9)
# plt.show()
# 
# 
# =============================================================================
