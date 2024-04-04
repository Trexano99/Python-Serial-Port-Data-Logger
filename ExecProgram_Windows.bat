@echo off

echo Checking if Python is installed...

python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install it from https://www.python.org/downloads/
) else (

    echo Python is installed. Proceeding.

    echo Checking necessary Python packages...
    python -m pip install --upgrade pip
    python -m pip install pyserial

    echo Done.    

    echo Starting execution of SerialPortDataLogger

    cls
    python SerialPortDataLogger.py
)

echo Press any key to exit...
pause >nul