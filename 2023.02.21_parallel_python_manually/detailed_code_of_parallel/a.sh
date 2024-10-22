#!/bin/sh
#PBS -N task
#PBS -l nodes=1:ppn=1
#PBS -q bigmem
python a.py
