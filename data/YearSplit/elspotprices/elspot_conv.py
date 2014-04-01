#
#	Convert elspot csv data to a Octave-readable csv - converted to CSV BY KingSoft Spreadsheet
#
import datetime

filename = 'Elspot Prices_2012_Hourly_EUR'


datafile = open(filename + '.csv', 'r')
outputfile = open(filename + '_conv.csv', 'w')
rownum = 1

for row in datafile:
	if rownum == 3:
		row = row.split(',')
		outputfile.write('Time,Oslo,Krs,Bergen,Molde,Trh,Tromso\n')
	if rownum > 3:
		row = row.replace('"','').replace(' ','').split(',')
		if len(row) > 20:
			date = row[0].replace('/','-').split('-')
			time = row[1].replace(' ','').split('-')
			
			thedate = datetime.datetime(int(date[2]), int(date[1]), int(date[0]), int(time[0][:-1]),0,0)
			weekday = str(datetime.datetime.weekday(thedate) + 1)
			
			#print(repr(len(date)))
			#print(date)
			outputfile.write( thedate.strftime('%Y-%m-%d %H:%M:%S') + ',' + row[18] + '.' + row[19] + ',' + row[20] + '.' + row[21] + ',' + row[22] + '.' + row[23] + ',' + row[24] + '.' + row[25] + ',' + row[26] + '.' + row[27] + ',' + row[28] + '.' + row[29]  + '\n')	
	
	rownum=rownum+1
	

outputfile.close()
datafile.close()