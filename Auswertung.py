import numpy as np
import matplotlib.pyplot as plt
import pylab
import os
import math

################ settings ################
# filename without ending
filename = 'GCE_1Vs-0.01Vs_2-11-21'
# amount of datapoints to determine linear regression function
n = 85
# significant digits of result
significant_digits = 3
##########################################


# load data from file
data = np.loadtxt(filename + '.txt', delimiter='\t', skiprows=1, dtype = np.double)

# take n number of data from the beginning
n = 85
regressiondata = data[0:n,:]

# determine number of colums
l = len(data[1,:]) - 1

# some directory stuff
dirname = os.path.dirname(__file__)
evaldir = os.path.join(dirname, filename + '_evaluation')
if not os.path.exists(evaldir):
    os.makedirs(evaldir)

for i in range(1,l+1):
    # find regression function parameters
    m,b = pylab.polyfit(regressiondata[:,0], regressiondata[:,i], 1)
    # find maximum value
    y_max = np.max(data[:,i])
    x_max = data[data[:,i]==y_max, 0]
    if len(x_max) > 1:
        x_max = x_max[0]
    # find corresponding x value of linear function
    y_lin = m*x_max + b
    # compute difference
    diff = float(y_max - y_lin)
    x = data[:,0]
    plt.figure
    plt.plot(x, data[:,i], x, m*x+b, ':', regressiondata[:,0], regressiondata[:,i], x_max, y_lin, 'ro', x_max, y_max, 'ro')
    left, right = plt.xlim()
    bottom, top = plt.ylim()
    plt.text(left + (0.01 * (right - left)), bottom + (0.95 * (top-bottom)), "\u0394 y: " + str(diff))
    rounded_number =  round(diff, significant_digits - int(math.floor(math.log10(abs(diff)))) - 1)
    plt.text(left + (0.01 * (right - left)), bottom + (0.9 * (top-bottom)), "\u0394 y (" + str(significant_digits) + " sf): " + str(rounded_number))
    plt.title(filename + ".txt measurement " + str(i), y=1.07)
    plt.savefig(os.path.join(evaldir, filename + "_meas" + str(i) + '.png'))
    plt.clf()
