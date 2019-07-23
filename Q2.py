# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 13:21:23 2018

@author: willi
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Question 2. (c) Plot

data = np.loadtxt('s_price_1yr.dat')

s = data[:,0]
t = data[:,1]

tick_spacing = 0.1

fig, ax = plt.subplots(1,1)
ax.plot(t,s)
ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
plt.xlabel("Time (years)")
plt.ylabel("Stock Price")
plt.title("Daily Share Price for One Year")
plt.xlim(min(t),max(t))
plt.ylim(min(s)-5,max(s)+5)
plt.show()


# Question 2. (d) Plot

data_1yr = np.loadtxt('portfolio_value_1yr.dat')
data_2yr = np.loadtxt('portfolio_value_2yr.dat')
data_5yr = np.loadtxt('portfolio_value_5yr.dat')
data_20yr = np.loadtxt('portfolio_value_20yr.dat')

print(data_1yr)
s = data_1yr[:,0]
t = data_1yr[:,1]

plt.hist(s,30)
plt.title("Histogram of Portfolio Value v(t) of the Portfolio After One Year")
plt.ylabel("Frequency")
plt.xlabel("Portfolio Value")
plt.show()

s = data_2yr[:,0]
t = data_2yr[:,1]

plt.hist(s,50)
plt.title("Histogram of Portfolio Value v(t) of the Portfolio After Two Years")
plt.ylabel("Frequency")
plt.xlabel("Portfolio Value")
plt.show()

s = data_5yr[:,0]
t = data_5yr[:,1]

plt.hist(s,50)
plt.title("Histogram of Portfolio Value v(t) of the Portfolio After Five Years")
plt.ylabel("Frequency")
plt.xlabel("Portfolio Value")
plt.show()

s = data_20yr[:,0]
t = data_20yr[:,1]
plt.hist(s,50)
plt.title("Histogram of Portfolio Value v(t) of the Portfolio After Twenty Years")
plt.ylabel("Frequency")
plt.xlabel("Portfolio Value")
plt.show()


# Question 2. (e)

data_stats = np.loadtxt('statistics.dat')

mean = data_stats[:,0]
variance = data_stats[:,1]
t = data_stats[:,2]

plt.plot(t, mean)
plt.title("The Mean of v(t) as a Function of Time")
plt.ylabel("Mean")
plt.xlabel("Time (years)")
plt.xlim(min(t),max(t))
plt.show()
 
plt.plot(t, variance)
plt.title("The Variance of v(t) as a Function of Time")
plt.ylabel("Variance")
plt.xlabel("Time (years)")
plt.xlim(min(t),max(t))
plt.show()


# Question 2. (f)

data_loss = np.loadtxt('prob_loss.dat')

num_losses = data_loss[:,0]
t = data_loss[:,1]

plt.plot(t, num_losses)
plt.title("Probability of loss as a Function of Time for the Portfolio v(t)")
plt.xlabel("Time (years)")
plt.ylabel("Probability of Loss")
plt.xlim(min(t),max(t))
plt.show()
