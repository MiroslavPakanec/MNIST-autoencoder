@echo off

REM Navigate to the mlflow directory and run the batch script
cd service_mlflow
call restart_windows.bat
cd ..

REM Navigate to the service directory and run the batch script
cd service_backend
call restart_windows.bat
cd ..


REM Navigate to the client directory and run the batch script
cd client
call restart_windows.bat
cd ..