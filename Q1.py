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
adj_close = df.loc[:,"Adj Close"]
adj_close = adj_close.values.tolist()

# =============================================================================
# daily_returns=[0]
# for i in np.arange(1,len(adj_close)-1):
#     returns = (adj_close[i]-adj_close[i-1])/adj_close[i-1]
#     daily_returns.append(returns)
# #plt.hist(adj_close, bins=30)
# #plt.show()
# 
# mu, std = norm.fit(daily_returns)
# 
# #print(norm.fit(daily_returns))
# #print(mu)
# fig, axes = plt.subplots(ncols=1, sharey=True)
# fig = plt.hist(daily_returns, bins=100, density=True)
# axes.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
# xmin,xmax = plt.xlim()
# plt.xlim(xmin,xmax)
# x = np.linspace(xmin,xmax,100)
# p = norm.pdf(x,mu,std)
# plt.plot(x,p,'k',linewidth=2) # This isn't correct but it's a start
# title = "Fit results: mu = %.5f,  std = %.3f" % (mu, std)
# plt.title(title)
# plt.show()
# 
# probplot(daily_returns, plot=plt)
# plt.xlim(-4,4)
# plt.ylim(-0.3,0.15)
# plt.show()
# 
# five_day_returns = [0]
# for i in np.arange(4,len(adj_close)-1,5):
#     returns = (adj_close[i]-adj_close[i-1]) / adj_close[i-1]
#     five_day_returns.append(returns)
#     
# fig, axes = plt.subplots(ncols=1, sharey=True)
# fig = plt.hist(five_day_returns, bins=100, density=True)
# axes.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
# xmin,xmax = plt.xlim()
# plt.xlim(xmin,xmax)
# x = np.linspace(xmin,xmax,100)
# p = norm.pdf(x,mu,std)
# plt.plot(x,p,'k',linewidth=2) # This isn't correct but it's a start
# title = "Fit results: mu = %.5f,  std = %.3f" % (mu, std)
# plt.title(title)
# plt.show()
# 
# probplot(five_day_returns, plot=plt)
# plt.xlim(-4,4)
# plt.ylim(-0.3,0.15)
# plt.show()
# 
# ten_day_returns = [0]
# for i in np.arange(9,len(adj_close)-1,10):
#     returns = (adj_close[i]-adj_close[i-1]) / adj_close[i-1]
#     ten_day_returns.append(returns)
#     
# fig, axes = plt.subplots(ncols=1, sharey=True)
# fig = plt.hist(ten_day_returns, bins=100, density=True)
# axes.xaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.0%}'.format(x)))
# xmin,xmax = plt.xlim()
# plt.xlim(xmin,xmax)
# x = np.linspace(xmin,xmax,100)
# p = norm.pdf(x,mu,std)
# plt.plot(x,p,'k',linewidth=2) # This isn't correct but it's a start
# title = "Fit results: mu = %.5f,  std = %.3f" % (mu, std)
# plt.title(title)
# plt.show()
# 
# probplot(ten_day_returns, plot=plt)
# plt.xlim(-4,4)
# plt.ylim(-0.3,0.15)
# plt.show()
# 
# =============================================================================
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