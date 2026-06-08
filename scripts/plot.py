# !/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt


# parameters to modify 
filename="/home/ubuntu/CWM-project/assignment2/time_py.txt"
label='c'
xlabel = 'time(ns)'
ylabel = '% entries under'
title='CDF of One Million Repeat of rdtime with c on single core'
fig_name='trash.png'
bins=100 #adjust the number of bins to your plot
max_examples = 10000

## load data from input file
t = np.loadtxt(filename, delimiter=" ", dtype="float")[1:max_examples]
t = [x for x in t if x <= 500]
print(np.average(t))

## if your data is "X Y" (2 cols), use the following line
#plt.plot(t[:,0], t[:,1], label=label)  # Plot some data on the (implicit) axes.

## if your data is "X" (1 col), use the following line
#plt.plot(t, label=label)  # Plot some data on the (implicit) axes.

## comment the lines above and uncomment the line below to plot a simple CDF
plt.hist(t[:], bins, density=True, histtype='step', cumulative=True, label=label)

## comment the lines above and uncomment the 4 lines below for a nicer CDF
#n = np.arange(1,len(t)+1) / float(len(t))
#ts = np.sort(t)
#fig, ax = plt.subplots()
#ax.step(ts,n)

plt.xlabel(xlabel)
plt.ylabel(ylabel)
plt.title(title)
plt.legend()
plt.savefig(fig_name)
plt.show()
