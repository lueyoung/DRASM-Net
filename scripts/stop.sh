#!/bin/bash

# Set environment variables
export MAIN_LOG=logs/main.log

echo "Stopping IoT Resource Optimizer system..." | tee -a $MAIN_LOG

# Function to check and kill a process by its name
kill_process() {
    local process_name=$1
    local pids=$(pgrep -f $process_name)

    if [ -z "$pids" ]; then
        echo "No $process_name process found." | tee -a $MAIN_LOG
    else
        echo "Stopping $process_name process(es)..." | tee -a $MAIN_LOG
        echo $pids | xargs kill -9
        echo "$process_name process(es) stopped." | tee -a $MAIN_LOG
    fi
}

# Stop POX controller
kill_process "pox.py"

# Stop Mininet
echo "Stopping Mininet..." | tee -a $MAIN_LOG
sudo mn -c &>> $MAIN_LOG
echo "Mininet stopped." | tee -a $MAIN_LOG

# Stop main application
kill_process "main.py"

echo "IoT Resource Optimizer system stopped." | tee -a $MAIN_LOG
