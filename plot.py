#
#	For plotting
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
from array import array

d = pd.read_csv('SelectedResults.csv', index_col='y')

# YEAR = ID 1
years = d[d.ID == 1].index.values
nyears = len(years)

# TECHNOLOGY = ID 2
#techs = d[d.ID == 2]['t'].values
techs = ['tElCo', 'tElHy', 'tElPu', 'tElDi', 'tElNu']
ntechs = len(techs)


for i in range(0,ntechs):
		d[(d.ID == 92) & (d.r == 'NO') & (d.t == techs[i])]['value'].plot(label=techs[i])
		
plt.legend()
show()
	