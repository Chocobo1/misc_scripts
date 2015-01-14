1>2# : ^
''' This is also a valid python script
@echo off
python "%~f0" && pause && exit /b
rem ^ '''

# start of python script
import sys
print (sys.version)
