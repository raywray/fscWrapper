#!/bin/bash
# TO CALL: qsub script_name.sh

# this example batch script requests 1 node, 20 cores (the max)
# per node.. requesting ALL available cores can be seen as a way
# of requesting sole access to the node that gets allocated (other
# users cannot request cores on the allocated node); we "hog" all
# the resources of a node while our job is running there.
#
# ON THE OTHER HAND... the user here only runs a single instance of a
# single-threaded application -- namely the "hostname" command, which
# is propogated to the allocated node by way of mpirun (see below).
#
# GOLDEN RULE -- the batch system only does this: runs this batch
#        script on one of the requested nodes. that is ALL
#        it does. in which case when multiple processes (perhaps
#        on multiple nodes) are wanted it's the user's responsibility
#        to enter the appropriate commands to propogate the processes.
#        here, the user uses "mpirun" to propogate 2 processes on
#        the single nodes. NOTE: the "hostname" command as a built-in
#        system command is _obviously_ not linked w/ any openmpi mpi
#        libraries -- yet mpirun is happy to propogate instances
#        of that commmand.
#
# request 2 processes on a single generic node (of type "mpi").
# for more info on requesting specific nodes see
# "man pbs_resources"
#
# comments beginning w/ "PBS" serve as pbs batch directives...
#PBS -V
# request node via node property "mpi" -- the generic node property
#PBS -l nodes=1:ppn=1
#PBS -N samplerun_fsc
#PBS -joe
#PBS -q batch
cd $PBS_O_WORKDIR

python3 main.py