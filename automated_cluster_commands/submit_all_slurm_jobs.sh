#!/bin/bash

output_file="submit_jobs_output.txt"
> "$output_file" # clear if it already exists

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
FAILED_COUNTER=0

# Loop over each SLURM script name in the list and submit the job
while IFS= read -r SLURM_SCRIPT; do
    if [ -f "$SLURM_SCRIPT" ]; then
        sbatch_output=$(sbatch "$SLURM_SCRIPT" 2>&1)
        if [[ $? -eq 0 ]]; then
            echo "Submitted: $SLURM_SCRIPT"
            echo "Submitted: $SLURM_SCRIPT" >> "$output_file"
            COUNTER=$((COUNTER + 1))
        else
            echo "Failed to submit: $SLURM_SCRIPT"
            echo "Failed to submit: $SLURM_SCRIPT" >> "$output_file"
            echo "Error: $sbatch_output" >> "$output_file"
            FAILED_COUNTER=$((FAILED_COUNTER + 1))
        fi
    else
        echo "Script not found: $SLURM_SCRIPT"
        echo "Script not found: $SLURM_SCRIPT" >> "$output_file"
    fi
done < "$SLURM_SCRIPT_LIST_PATH"

echo "Total scripts submitted: $COUNTER"
echo "Total scripts submitted: $COUNTER" >> "$output_file"
echo "Total scripts failed: $FAILED_COUNTER"
echo "Total scripts failed: $FAILED_COUNTER" >> "$output_file"
