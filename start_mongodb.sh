#!/bin/bash
# Script to start MongoDB for development

DATA_DIR="/tmp/mongodb_data"
SOCK_DIR="$HOME/mongodb_sock"
LOG_FILE="/tmp/mongodb.log"

# Create directories if they don't exist
mkdir -p "$DATA_DIR"
mkdir -p "$SOCK_DIR"

# Check if MongoDB is already running
if pgrep -x mongod > /dev/null; then
    echo "MongoDB is already running"
    exit 0
fi

# Start MongoDB
echo "Starting MongoDB..."
mongod --dbpath "$DATA_DIR" \
       --port 27017 \
       --bind_ip 127.0.0.1 \
       --unixSocketPrefix "$SOCK_DIR" \
       --fork \
       --logpath "$LOG_FILE"

if [ $? -eq 0 ]; then
    echo "MongoDB started successfully"
    echo "Data directory: $DATA_DIR"
    echo "Log file: $LOG_FILE"
else
    echo "Failed to start MongoDB. Check logs at: $LOG_FILE"
    exit 1
fi
