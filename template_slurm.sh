#!/bin/bash

#SBATCH --job-name=job
#SBATCH --partition=compute
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --input=none
#SBATCH --output=./log/job_%A_%a.out
#SBATCH --error=./log/job_%A_%a.err
#SBATCH --mem=20g
#SBATCH --time=0-04

#--------------------------------------------------------------------------------
# force mode
#--------------------------------------------------------------------------------
FORCE_MODE=false
forceFilepath= #WRITE ME
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
    exit
fi

#--------------------------------------------------------------------------------
# array job expander
#--------------------------------------------------------------------------------
argFilepath=${1}
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
arg1=`echo ${line} | cut -d ',' -f1`

#--------------------------------------------------------------------------------
# submit array jobs
#--------------------------------------------------------------------------------
cmd= #WIRTE ME like examble.sh
argCmd=./arg/${cmd/.sh/.py}
argFilepath=./arg/${cmd/.sh/.list}
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
prevJobId=${jobId}
jobId=`sbatch --parsable --array=1-${numJobs} --dependency=afterok:${prevJobId} ${cmd} ${argFilepath}`
echo "submitted ${numJobs} jobs with job_id=${jobId}, dependency=${prevJobId}"
