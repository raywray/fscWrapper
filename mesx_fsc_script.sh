#!/bin/bash -l
#
#PBS -V
#PBS -l nodes=1:ppn=1
#PBS -N samplerun_fsc
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
conda activate fscwrapper_test_env

# Change to the working directory
cd $PBS_O_WORKDIR

# List the Conda environments for debugging
conda info --envs

echo "activating my env"
conda info --envs | grep '^*'

# Define paths to Python script and input file
fsc_wrapper_py=/home/resplin5072/fscWrapper/main.py
user_param_input_file=/home/resplin5072/fscWrapper/user_input_hops_k4.yml

# Run the Python script
echo python3 $fsc_wrapper_py $user_param_input_file
python3 $fsc_wrapper_py $user_param_input_file
