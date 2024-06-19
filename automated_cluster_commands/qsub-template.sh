#!/bin/bash -l

#PBS -V
#PBS -l nodes=1:ppn=1
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
cur_run=CUR_RUN

# Run the Python script
echo python3 $fsc_wrapper_py $output_dir $project_path $prefix $cur_run
python3 $fsc_wrapper_py $output_dir $project_path $prefix $cur_run