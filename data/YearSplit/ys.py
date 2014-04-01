#
#	For splitting years into splits based on seasons, daytypes and timebrackets
#

#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt
#from pylab import *
from array import array
import datetime
import csv
#import numpy.lib.recfunctions as rfn

#
#	YearSplit class
#
class YearSplit(object):
	def __init__(self, month = 0, daytype = [], dtb = []):
		
		seasStr = { 1 : 'Jan', 2 : 'Feb', 3 : 'Mar', 4 : 'Apr', 5 : 'May', 6 : 'Jun', 7 : 'Jul', 8 : 'Aug', 9 : 'Sep', 10 : 'Oct', 11 : 'Nov', 12 : 'Dec' }
		dtStr = { 0 : 'Wd', 5 : 'We' }
		dtbStr = { 0 : '1', 6 : '2', 11 : '3', 17 : '4', 22 : '5' }
	
		self.month = month
		self.daytype = daytype
		self.dtb = dtb
		self.name = seasStr[month] + dtStr[daytype[0]] + dtbStr[dtb[0]]
		
	def getAccumHourly(self, time, values):
		
		accumValue = 0
		
	    # If time and values are not the same
		if len(time) != len(values):
			print 'Time and values does not have the same amount of indexes'
			return 0
		for i in range(0,len(values)):
		    if time[i].month == self.month and time[i].weekday() in self.daytype and time[i].hour in self.dtb:
				accumValue = accumValue + values[i]
		return accumValue
		
	def getAverageHourly(self,time, values):
	
		accumValue = 0
		numValues = 0
		
	    # If time and values are not the same
		if len(time) != len(values):
			print 'Time and values does not have the same amount of indexes'
			return 0
		for i in range(0,len(values)):
		    if time[i].month == self.month and time[i].weekday() in self.daytype and time[i].hour in self.dtb:
				accumValue = accumValue + values[i]
				numValues = numValues + 1
		return accumValue / numValues
		
	def getYearSplit(self,time):
	
		numValues = 0
		
	    # If time and values are not the same
		for i in range(0,len(time)):
		    if time[i].month == self.month and time[i].weekday() in self.daytype and time[i].hour in self.dtb:
				numValues = numValues + 1

		return numValues / float(len(time))

	def getValueProfile(self,time,values):
	
		accumValue = 0
		
	    # If time and values are not the same
		if len(time) != len(values):
			print 'Time and values does not have the same amount of indexes'
			return 0
		for i in range(0,len(values)):
		    if time[i].month == self.month and time[i].weekday() in self.daytype and time[i].hour in self.dtb:
				accumValue = accumValue + values[i]
		return accumValue / sum(values)
		
		
#	def daytypes(self, dt)
#		
#       return daytypes(dt)




# DayTypes
# 1 = weekday, 2 = weekend (sat/sun)
daytypes = { 1 : [0,1,2,3,4], 2: [5,6] }

# DailyTimeBrackets
dtbs = {1 : range(0,6), 2 : range(6,11), 3 : range(11,17), 4 : range(17,22), 5 : range(22,24)}

seasons = { 1 : 1, 2 : 2, 3 : 3, 4 : 4, 5 : 5,6:6,7:7,8:8,9:9,10:10,11:11,12:12 }

# Total number
nYs = len(daytypes) * len(dtbs) * len(seasons)
print 'Number of slices: ' + repr(nYs)

ys = []
# Register/generate all yearsplits
for s in seasons.keys():
	for dt in daytypes.keys():
		for dtb in dtbs.keys():
			ys.append(YearSplit(s,daytypes[dt],dtbs[dtb]))

#			
## Read price data
#

priceTime = []
price = []
with open('elspotprices/Elspot Prices_2013_Hourly_EUR_conv.csv', 'rb') as f:
	reader = csv.reader(f)
	reader.next()
	for row in reader:
		# Append datetime
		priceTime.append( datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S') )
		
		# Append price to array
		price.append( (float(row[1]) + float(row[2]) + float(row[3]) + float(row[4]) + float(row[5]) + float(row[6]) ) / 6 )

		

#
## Read demand data
#
demandTime = []
demand = []		
with open('statnetcons/ProductionConsumption-2013.csv', 'rb') as f:
	reader = csv.reader(f)
	reader.next()
	for row in reader:
		# Append datetime
		demandTime.append( datetime.datetime.strptime(row[0][:19], '%d.%m.%Y %H:%M:%S' ) )
		
		# Append demand to array
		demand.append( float(row[2]) )		

# Calculate average price  and accumulated demand for each timeslice		
averagePrice = [0]*len(ys)
accumDemand = [0]*len(ys)
yearSplit = [0]*len(ys)
demandProfile = [0]*len(ys)

for i in range(0, len(ys)):
  averagePrice[i] = ys[i].getAverageHourly(priceTime,price)
  accumDemand[i] = ys[i].getAccumHourly(demandTime,demand)
  yearSplit[i] = ys[i].getYearSplit(demandTime)
  demandProfile[i] = ys[i].getValueProfile(demandTime,demand)
 
 
# Output to file
startY = 2014
endY = 2034

# Yearsplit

opf = open('yearSplit.txt', 'w')
opf.write('param YearSplit\t:\t')

for i in range(startY,endY+1):
	opf.write( '{0:d}\t\t'.format(i) )

opf.write('\t:=')

for i in range(0, len(ys)):
	opf.write( '\n' + ys[i].name + '\t\t\t\t')
	for j in range(startY,endY+1):
		opf.write( '{0:.6f}\t'.format(yearSplit[i]))
		
opf.write(';\n\n\n')

# Specified demandprofile

opf.write('param\tSpecifiedDemandProfile\tdefault 0\t:=\n\t[NO,fELC,*,*]\t:\t')
for i in range(startY,endY+1):
	opf.write( '{0:d}\t\t'.format(i) )
	
for i in range(0, len(ys)):
	opf.write( '\n' + ys[i].name + '\t\t\t\t')
	for j in range(startY,endY+1):
		opf.write( '{0:.6f}\t'.format(demandProfile[i]))
opf.write(';\n\n\n')

# Conversion ls
opf.write('param Conversionls default 0 :=\n[*,*]:\t\t')
for i in range(1,13):
	opf.write( '{0:d}\t'.format(i) )
for i in range(0, len(ys)):
	opf.write( '\n' + ys[i].name + '\t\t')
	for j in range(1,13):
		if ys[i].month == j:
			opf.write( '{0:d}\t'.format(1) )
		else:
			opf.write( '{0:d}\t'.format(0) )
			
opf.write(';\n\n\n')			

# Conversion ld
opf.write('param Conversionld default 0 :=\n[*,*]:\t\t')
for i in range(1,3):
	opf.write( '{0:d}\t'.format(i) )
for i in range(0, len(ys)):
	opf.write( '\n' + ys[i].name + '\t\t')
	for j in range(1,3):
		if ys[i].daytype == daytypes[j]:
			opf.write( '{0:d}\t'.format(1) )
		else:
			opf.write( '{0:d}\t'.format(0) )
			
opf.write(';\n\n\n')	

# Conversion lh
opf.write('param Conversionlh default 0 :=\n[*,*]:\t\t')
for i in range(1,6):
	opf.write( '{0:d}\t'.format(i) )
for i in range(0, len(ys)):
	opf.write( '\n' + ys[i].name + '\t\t')
	for j in range(1,6):
		if ys[i].dtb == dtbs[j]:
			opf.write( '{0:d}\t'.format(1) )
		else:
			opf.write( '{0:d}\t'.format(0) )
			
opf.write(';\n\n\n')	

for i in range(0, len(ys)):
	opf.write('\t' + ys[i].name)


opf.close()

print 'Total consumption: ' + str(sum(demand)) + 'MWh' + ' = ' + str(sum(demand)*3.6*pow(10,-6)) + 'PJ'
