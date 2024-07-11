#!/bin/bash

output_file="submission_output.txt"
> "$output_file" # clear if it already exists

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
        JOB_ID=$(qsub "$PBS_SCRIPT" 2>&1)
        if [[ "$JOB_ID" == *"PBS job id"* ]]; then
            echo "Successfully submitted: $PBS_SCRIPT with job ID: $JOB_ID"
            echo "Submitted: $PBS_SCRIPT with job ID: $JOB_ID" >> "$output_file"
            COUNTER=$((COUNTER + 1))
        else
            echo "Failed to submit: $PBS_SCRIPT"
            echo "Failed to submit: $PBS_SCRIPT with error: $JOB_ID" >> "$output_file"
        fi
    else
        echo "Script not found: $PBS_SCRIPT"
        echo "Script not found: $PBS_SCRIPT" >> "$output_file"
    fi
done < "$PBS_SCRIPT_LIST_PATH"

echo "Total scripts submitted: $COUNTER"
