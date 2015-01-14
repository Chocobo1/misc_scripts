@echo off
more +3 "%~f0" | python && pause && exit /b

# start of python script
import sys
print (sys.version)
