#Evaluation Day XX - DD.MM.YYYY - Time: HH:MM
#Conditions: Ambient or nitrogen Atmosphere
#Chemicals: Solution X / Redox Probe Y with Concentration Z
#Working Electrode: GCE, Flat ITO, Porous ITO or Ultra-Micro-Electrode

#Import packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pylab
import os
import math

################ settings ################
# filename without ending
filename = 'GCE_1Vs-0.01Vs_compensation-900Ohm'
# startposition of datapoints
a = 0
# endposition of datapoints to determine linear regression function
n = 80
# sweep rate patterns (srp):
srp = ([1000, 900, 800, 700, 600, 500, 400, 300, 200, 100], 
       [1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50, 30, 20, 10],
       [1000, 900, 800, 700, 600, 500, 400, 300, 200, 150, 100, 80, 60, 50, 30, 20, 10, 5, 3, 2, 1],
       [1000], 
       [#insert here your own scan rate pattern
       ]
      )
#select scan rate line 1, 2, 3, 4, etc.
srl = 2
# significant digits of result
significant_digits = 5
##########################################


# load data from file
data = np.loadtxt(filename + '.txt', delimiter='\t', skiprows=1, dtype = np.double)

#use datapoints for baseline
regressiondata = data[a:n,:]

# determine number of colums
l = len(data[1,:]) - 1

# some directory stuff
dirname = os.path.dirname('____file______')
evaldir = os.path.join(dirname, filename + '_evaluation')
if not os.path.exists(evaldir):
    os.makedirs(evaldir)
    
    
#index for sweep rate
r= srp[srl-1]
print("i,p in Ampere from Sweep rates "+str(r[0])+ "mV/s to " + str(r[-1])+"mV/s:")

p=0
for i in range(1,l+1):
    # find regression function parameters
    m,b = pylab.polyfit(regressiondata[:,0], regressiondata[:,i], 1)
    x_a = m
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
    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.plot(x, data[:,i], x, m*x+b, ':', regressiondata[:,0], regressiondata[:,i], x_max, y_lin, 'ro',x_max, y_max, 'ro', regressiondata[0,0], regressiondata[0,i],'gx',regressiondata[-1,0], regressiondata[-1,i], 'gx')
    left, right = plt.xlim()
    bottom, top = plt.ylim()
    rounded_number =  round(diff, significant_digits - int(math.floor(math.log10(abs(diff)))) - 1)
    plt.text(left + (0.01 * (right - left)), bottom + (0.95 * (top-bottom)), "\u0394i (" + str(significant_digits) + " sf): " + str(rounded_number) + " A")
    plt.title(filename + ".txt: measurement " + str(r[p]) + " mV/s", y=1.07)
    plt.xlabel('E in [V]')
    plt.ylabel('i in [A]')
    plt.subplots_adjust(left=0.15)
    ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
    plt.savefig(os.path.join(evaldir, filename + "_meas" + str(r[p]) + '.png'))
    plt.clf()
    
    #Output delta i,p
    #print(str(r[p]) + "=" + str(rounded_number))
    print(str(rounded_number))
    
    #Output delta i,p/v^(0.5)
    #print(str(rounded_number/(r[p]*0.001)**(0.5)))
    p+=1

