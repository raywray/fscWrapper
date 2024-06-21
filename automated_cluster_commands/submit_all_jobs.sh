#!/bin/bash

# Check if the list of PBS script names is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <pbs_script_list_file>"
    exit 1
fi

# Read the list of PBS script names from the provided file
PBS_SCRIPT_LIST_PATH=$1

if [ ! -f "$PBS_SCRIPT_LIST_PATH" ]; then
    echo "File not found: $PBS_SCRIPT_LIST_PATH"
    exit 1
fi

# Initialize the counter
COUNTER=0

# Loop over each PBS script name in the list and submit the job
while IFS= read -r PBS_SCRIPT; do
    if [ -f "$PBS_SCRIPT" ]; then
        qsub "$PBS_SCRIPT"
        echo "Submitted: $PBS_SCRIPT"
        COUNTER=$((COUNTER + 1))
    else
        echo "Script not found: $PBS_SCRIPT"
    fi
done < "$PBS_SCRIPT_LIST_PATH"
