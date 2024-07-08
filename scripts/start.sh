#!/bin/bash

# Set environment variables
export POX_DIR=~/workspace/pox
export CONFIG_FILE=src/config/config.json

# Define log files
MAIN_LOG=logs/main.log
SDN_CONTROLLER_LOG=logs/sdn_controller.log
RESOURCE_ALLOCATION_LOG=logs/resource_allocation.log
STABILITY_ANALYSIS_LOG=logs/stability_analysis.log
NETWORK_MANAGER_LOG=logs/network_manager.log
NETWORK_MONITOR_LOG=logs/network_monitor.log

# Create log directory if it doesn't exist
mkdir -p logs

# Clear old log files
> $MAIN_LOG
> $SDN_CONTROLLER_LOG
> $RESOURCE_ALLOCATION_LOG
> $STABILITY_ANALYSIS_LOG
> $NETWORK_MANAGER_LOG
> $NETWORK_MONITOR_LOG

echo "Starting IoT Resource Optimizer system..." | tee -a $MAIN_LOG

# Start POX controller
echo "Starting POX controller..." | tee -a $MAIN_LOG
$POX_DIR/pox.py forwarding.l2_learning openflow.discovery ext.rest_api &>> $SDN_CONTROLLER_LOG &
POX_PID=$!
echo "POX controller started with PID $POX_PID" | tee -a $MAIN_LOG

# Start Mininet
echo "Starting Mininet..." | tee -a $MAIN_LOG
sudo mn --controller=remote,ip=127.0.0.1,port=6633 --switch ovsk,protocols=OpenFlow10 --topo=single,3 &>> $MAIN_LOG &
MININET_PID=$!
echo "Mininet started with PID $MININET_PID" | tee -a $MAIN_LOG

# Start main application
echo "Starting main application..." | tee -a $MAIN_LOG
python3 src/main.py $CONFIG_FILE &>> $MAIN_LOG &
MAIN_APP_PID=$!
echo "Main application started with PID $MAIN_APP_PID" | tee -a $MAIN_LOG

# Wait for all processes to finish
wait $POX_PID $MININET_PID $MAIN_APP_PID

echo "IoT Resource Optimizer system stopped." | tee -a $MAIN_LOG
