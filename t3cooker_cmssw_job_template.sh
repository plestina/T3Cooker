#!/bin/bash

export SCRAM_ARCH=MY_SCRAM_ARCH
export CMSSW_BASE=MY_CMSSW_BASE

#these variables are setted-up by t3cooker t3cJobManager::makeJobs 
logdir=LOGDIR
logfile=FOUTNAMENOEXT.out
thisjobfileslist=THISJOBFILESLIST
lumimask=LUMIMASK
prefix=PREFIX
pset=PSET
jobid=JOBID

if [! -f $logfile]; then rm $logfile; fi

#Setting up the directory
mkdir -p $logdir/done $logdir/failed

#Setup CMSSW area
voms-proxy-info --all 1>>$logfile 2>&1 ;
cd ${CMSSW_BASE}/src  1>>$logfile 2>&1 ; #directory where current CMSSW release is
source /opt/exp_soft/cms/cmsset_default.sh 1>>$logfile 2>&1 ;
eval `scram runtime -sh`; 1>>$logfile 2>&1 ;
cd - 1>>$logfile 2>&1 ;
echo "Working directory: "$PWD

/usr/bin/time -vo $logfile cmsRun $pset files_load=$thisjobfileslist $lumimask PYCONFIG_PARAMS tag=_$jobid filePrepend=$prefix 1>>$logfile 2>&1 ;

#if the job is done with exit code 0 then print number to file jobs_done
if [ $? = 0 ]; then
  chmod +r ${prefix}/*_${jobid}.root
  touch $logdir/done/$jobid
else
  touch $logdir/failed/$jobid
fi
