#!/bin/bash

# Navigate to the mlflow service directory and run the shell script
cd client
./restart_linux.sh
cd ..

# Navigate to the backend service directory and run the shell script
cd service
./restart_linux.sh
cd ..

# Navigate to the client directory and run the batch script
cd client
./restart_linux.sh
cd ..