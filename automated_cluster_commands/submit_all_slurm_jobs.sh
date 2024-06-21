#!/bin/bash

# Check if the list of SLURM script names is provided as an argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <slurm_script_list_file>"
    exit 1
fi

# Read the list of SLURM script names from the provided file
SLURM_SCRIPT_LIST_PATH=$1

if [ ! -f "$SLURM_SCRIPT_LIST_PATH" ]; then
    echo "File not found: $SLURM_SCRIPT_LIST_PATH"
    exit 1
fi

# Initialize the counter
COUNTER=0

# Loop over each SLURM script name in the list and submit the job
while IFS= read -r SLURM_SCRIPT; do
    if [ -f "$SLURM_SCRIPT" ]; then
        sbatch "$SLURM_SCRIPT"
        echo "Submitted: $SLURM_SCRIPT"
        COUNTER=$((COUNTER + 1))
    else
        echo "Script not found: $SLURM_SCRIPT"
    fi
done < "$SLURM_SCRIPT_LIST_PATH"

echo "Total scripts submitted: $COUNTER"

