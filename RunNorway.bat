::
::
::	Batch script for running OSeMOSYS Norway Model
::	Kristoffer Lorentsen
::	March 2014
::
ECHO OFF
SET PATH=%PATH%;C:\Program Files (x86)\GnuWin32\bin
glpsol -m OSeMOSYS_2013_05_10/OSeMOSYS_2013_05_10.txt -d norway.dat -o norway_results.txt
