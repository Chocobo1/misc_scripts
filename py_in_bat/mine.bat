@echo off
rem This is python script embedded in windows batch script. The windows script bootstrap python and then exits
set PY_BOOT="f=open('%~nx0','r');t=f.readlines();f.close();exec ''.join(t[7:]);"
python -c %PY_BOOT%
pause && exit /b

# start of python script
import sys
print (sys.version)
