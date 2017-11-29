#--------------------------------------------------------------------------------
# force mode
#--------------------------------------------------------------------------------
FORCE_MODE=false
forceFilepath=hoge
if [ "$FORCE_MODE" = false ] && [ -e ${forceFilepath} ]; then
    echo "PASS: target already distributed"
else
    #WRITE ME
fi

#--------------------------------------------------------------------------------
# array job expander
#--------------------------------------------------------------------------------
argFilepath=hoge
if [ -z ${SLURM_ARRAY_TASK_ID+x} ]; then lineNum=1; else lineNum=${SLURM_ARRAY_TASK_ID} fi;
line=`awk -v lineNum=$linuNum '{if (NR == lineNum) print $0}' ${argFilepath}`
