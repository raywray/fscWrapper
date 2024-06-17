#!/bin/bash -l

#PBS -V
#PBS -l NODES
#PBS -N JOBNAME
#PBS -joe
#PBS -q batch

cd $PBS_O_WORKDIR
NCORES=`wc -w < $PBS_NODEFILE`
DATE=`date`
HOST=`hostname`

echo " "
echo "running on host: $HOSTNAME"
echo "$NCORES cores requested"
echo "job submitted: $DATE"
echo "job STDOUT follows:"
echo " "

# Activate the Conda environment
conda init bash
source /home/resplin5072/bashrc-miniconda3
conda activate fsc_wrapper_env

# Change to the working directory
cd $PBS_O_WORKDIR

# List the Conda environments for debugging
conda info --envs

echo "activating my env"
conda info --envs | grep '^*'

# Define paths to Python script and input file
project_path=PROJECT_PATH
fsc_wrapper_py="${project_path}/cluster_main.py"
output_dir=OUTPUT_DIR
prefix=PREFIX
num_first_sim=NUM_FIRST_SIM
num_last_sim=NUM_LAST_SIM

for i in $(seq $num_first_sim $num_last_sim); do
    # Run the Python script
    echo python3 $fsc_wrapper_py $output_dir $project_path $prefix $i
    python3 $fsc_wrapper_py $output_dir $project_path $prefix $i &
done

# Wait for all background jobs to finish
wait

echo "All instances of the Python script have completed"

