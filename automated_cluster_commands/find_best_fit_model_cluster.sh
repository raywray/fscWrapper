#!/bin/bash -l
#
#PBS -V
#PBS -l nodes=1:ppn=1
#PBS -N raya_find_best_lhoods
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

echo python3 /home/resplin5072/fscWrapper/automated_cluster_commands/find_best_fit_model_cluster.py 
python3 /home/resplin5072/fscWrapper/automated_cluster_commands/find_best_fit_model_cluster.py 