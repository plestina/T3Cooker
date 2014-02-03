#!/bin/bash

#export SCRAM_ARCH=MY_SCRAM_ARCH
#export CMSSW_BASE=MY_CMSSW_BASE
#export PBS_O_MAIL=roko.plestina@gmail.com

#these variables are setted-up by t3cooker t3cJobManager::makeJobs 
logdir=LOGDIR
logfile=FOUTNAMENOEXT.out
thisjobfileslist=THISJOBFILESLIST
lumimask=LUMIMASK
prefix=PREFIX
jobid=JOBID
executable=EXECUTABLE

#Setting up the directory
mkdir -p $logdir/done $logdir/failed

# cd /home/llr/cms/plestina/cmssw/CMG_5_2_X/CMGTools/CMSSW_5_2_5/src
# cd /home/llr/cms/plestina/cmssw/L1/CMSSW_5_3_4/src
cd /grid_mnt/vol__vol1__u/llr/cms/plestina/cmssw/HzzProduction/TreesLLR/2013/V5_15_0/CMGTools/CMSSW_4_4_5/src
export SCRAM_ARCH=slc5_amd64_gcc462
source /opt/exp_soft/cms/cmsset_default.sh
eval `scram runtime -sh`
cd -

# source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.27.06/x86_64-slc5-gcc43-opt/root/bin/thisroot.sh
# source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.32.00/x86_64-slc5-gcc46-opt/root/bin/thisroot.sh
# source /afs/cern.ch/sw/lcg/app/releases/ROOT/5.28.00/slc4_amd64_gcc34/root/bin/thisroot.sh


#Setup CMSSW area
voms-proxy-info --all 1>>$logfile 2>&1 ;
echo "Working directory: "$PWD


#change this part to cover your needs
export PATH=$PATH:EXE_DIR 
${executable} -filelist ${thisjobfileslist} ${lumimask} OPTIONS -out ${prefix}output_${jobid}.root 1>>$logfile 2>&1 ;
# /usr/bin/time -vo $logfile  ${executable} -filelist ${thisjobfileslist} ${lumimask} OPTIONS -out ${prefix}output_${jobid}.root 1>>$logfile 2>&1 ;


#if the job is done with exit code 0 then print number to file jobs_done
if [ $? = 0 ]; then
  chmod +r ${prefix}output_${jobid}.root 1>>$logfile 2>&1 
  touch $logdir/done/$jobid
else
  touch $logdir/failed/$jobid
fi
