#
#	For analyzing elspot data
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from array import array
import datetime

d13 = pd.read_csv('Elspot Prices_2013_Hourly_EUR_conv.csv',index_col='Time')
d12 = pd.read_csv('Elspot Prices_2012_Hourly_EUR_conv.csv',index_col='Time')

# Get average and timestamp
d12['avg'] = (d12['Oslo'] + d12['Krs'] + d12['Bergen'] + d12['Molde'] + d12['Trh'] + d12['Tromso'])/6
d12.index = pd.to_datetime(d12.index, format='%Y-%m-%d %H:%M:%S')

d13['avg'] = (d13['Oslo'] + d13['Krs'] + d13['Bergen'] + d13['Molde'] + d13['Trh'] + d13['Tromso'])/6
d13.index = pd.to_datetime(d13.index, format='%Y-%m-%d %H:%M:%S')

plt.figure()
plt.grid()

d12.avg.plot(c='blue')
d13.avg.plot(c='red')

plt.grid()

show()

plt.figure()

# Cumulative dist function (load duration)
# http://stackoverflow.com/questions/15408371/cumulative-distribution-plots-python
data12 = d12.avg.values
values12, base12 = np.histogram(data12, bins=100)
cums12 = np.cumsum(values12)
plt.plot(base12[:-1],len(data12)-cums12, c='blue', label='2012')

data13 = d13.avg.values
values13, base13 = np.histogram(data13, bins=100)
cums13 = np.cumsum(values13)
plt.plot(base13[:-1],len(data13)-cums13, c='red', label='2013')
plt.grid()
plt.legend()
show()
# Get timestamp

#d['dt'] =  + ':00:00')
#d.apply(lambda dt:'%s-%s-%s %s:00:00' % (d['Yr'],d['Mnth'],d['Day'],d['Time']),axis=1)
