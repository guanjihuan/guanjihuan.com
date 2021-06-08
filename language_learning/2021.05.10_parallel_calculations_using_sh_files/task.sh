#!/bin/sh

for job_index in 0 1 2 3 4 5 6
do

cp a.py a${job_index}.py
sed -i "s/job_index = -1/job_index = ${job_index}/" a${job_index}.py


cp a.sh a${job_index}.sh
sed -i "s/python a.py/python a${job_index}.py/" a${job_index}.sh
qsub a${job_index}.sh

done
