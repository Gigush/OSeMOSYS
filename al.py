#
#	Code for analyzing OSeMOSYS results - it simply initializes the workspace
#	Kristoffer Lorentsen - 2014
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import *

d = pd.read_csv('SelectedResults.csv')#, index_col='y')

#
##	Generate dictionaries for mapping between ID and NAME
#
dName = {} # Input id, get name
dID = {} # Input name, get id
dict = './OSeMOSYS_Print/OSeMOSYS_2013_05_10_desc.txt'
dictf = open( dict , 'r' )

for row in dictf:
	row = row.split(',')
	dName[int(row[0])] = row[1]
	dID[row[1]] = int(row[0])

#strg = d[(d.ID == 68) & (d.ls == 2) & (d.s == 'DAM')].value
