@echo off

REM Switch to D: drive and project directory
cd /D "D:\Nihal\Codes\Automatic Notebook Run"

:: This batch script activates a conda env and runs the notebook
call "C:\Users\Musanna\anaconda3\condabin\conda.bat" activate pytorch_env

:: Execute the notebook using Jupyter
jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=-1 --output "%~1" "%~2"
exit
