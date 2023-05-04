@echo off
set INTERVAL=300
:Again
python run.py
::pause::
timeout %INTERVAL%
goto Again
