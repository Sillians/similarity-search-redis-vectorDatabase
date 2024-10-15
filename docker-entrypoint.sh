#!/bin/sh
set -e

# Set the code directory path
CODE_DIR="/app/src"

# file name to run
MY_FILE=${1:-main.py}

echo "Starting similarity search application: $MY_FILE"

# Run the script
python3 "$CODE_DIR/$MY_FILE"