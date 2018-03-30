#!/bin/bash

#!/bin/bash
#$ -S /bin/bash
#$ -N pre
#$ -q standard.q
#$ -cwd
#$ -v PATH
#$ -o /dev/null
#$ -e /dev/null
#$ -l mem_free=5G

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
if [ -z ${SGE_TASK_ID+x} ] ; then lineNum=1; else lineNum=${SGE_TASK_ID}; fi;
line=`awk -v lineNum=$lineNum '{if (NR == lineNum) print $0}' ${argFilepath}`
arg1=`echo ${line} | cut -d ',' -f1`
OUT=./log/pre_${JOB_ID}_${SGE_TASK_ID}.out
ERR=./log/pre_${JOB_ID}_${SGE_TASK_ID}.err

#--------------------------------------------------------------------------------
# submit array jobs
#--------------------------------------------------------------------------------
cmd= #WRITE ME like example.sh
argCmd=./arg/${cmd%.*}.py
argFilepath=${argCmd%.*}.lst
eval ${argCmd} > ${argFilepath}
numJobs=`grep -c '' ${argFilepath}`
prvJobid=${jobid}
jobid_r=`qsub -terse -t 1-${numJobs} -hold_jid ${prvJobid} ${cmd} ${argFilepath}`
jobid=`echo ${jobid_r} | cut -d '.' -f1`
echo "submitted ${numJobs} jobs with job_id=${jobid}, dependency=${prvJobid}"
