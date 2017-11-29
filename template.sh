#--------------------------------------------------------------------------------
# force mode
#--------------------------------------------------------------------------------
FORCE_MODE=false
forceFilepath=hoge
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target file already exists"
else
    #WRITE ME
fi

#--------------------------------------------------------------------------------
# array job expander
#--------------------------------------------------------------------------------
argFilepath=hoge
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID}; fi;
line=`awk -v lineNum=$linuNum '{if (NR == lineNum) print $0}' ${argFilepath}`


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
echo "submitted "${numJobs}" jobs with job_id="${jobId}", dependency="${prevJobId}
