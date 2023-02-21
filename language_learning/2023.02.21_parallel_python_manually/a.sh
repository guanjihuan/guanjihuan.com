#!/bin/sh
#PBS -N task
#PBS -l nodes=1:ppn=1
#PBS -q bigmem
cd $PBS_O_WORKDIR
export OMP_NUM_THREADS=1
python a.py
