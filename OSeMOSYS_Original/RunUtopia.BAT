ECHO OFF
ECHO If this fails, edit the batch file to make GLPSOL.EXE accesible via the PATH variable.
SET PATH=%PATH%;C:\Program Files (x86)\GnuWin32\bin
glpsol -m OSeMOSYS_2013_05_10_short.txt -d UTOPIA_2013_05_10.dat -o UtopiaResults.txt
Pause