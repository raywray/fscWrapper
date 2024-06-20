#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1     # This will be the number of CPUs per individual array job
#SBATCH --mem=300M     # This will be the memory per individual array job
#SBATCH --time=0-12:00:00     # 12 hrs per job
#SBATCH --array=1-ARRAY_MAX
#SBATCH --job-name=JOB_NAME
#SBATCH --partition=PARTITION

DATE=$(date)
HOST=$(hostname)
NCORES=$(nproc)

echo " "
echo "running on host: $HOST"
echo "$NCORES cores requested"
echo "job submitted: $DATE"
echo "job STDOUT follows:"
echo " "

# Activate the Conda environment
conda init bash
source /opt/linux/rocky/8.x/x86_64/pkgs/miniconda3/py39_4.12.0/bin/conda
conda activate fsc_wrapper_env

# List the Conda environments for debugging
conda info --envs

echo "activating my env"
conda info --envs | grep '^*'

# Calculate the parameters based on the array index
INDEX=$SLURM_ARRAY_TASK_ID
PARAMS=$(sed -n "${INDEX}p" PARAM_FILE)

# Extract individual parameters
output_dir=$(echo $PARAMS | cut -d ' ' -f 1)
project_path=$(echo $PARAMS | cut -d ' ' -f 2)
prefix=$(echo $PARAMS | cut -d ' ' -f 3)
i=$(echo $PARAMS | cut -d ' ' -f 4)

fsc_wrapper_py="${project_path}/cluster_main.py"

# Run your Python script with the parameters
python3 $fsc_wrapper_py $output_dir $project_path $prefix $i
