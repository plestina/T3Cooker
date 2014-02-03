#!/bin/bash

##Job settings                                                         
#PBS -o LOGDIR/cmssw_JOBID.stdout                          
#PBS -e LOGDIR/cmssw_JOBID.stderr                                       
#PBS -W group_list=avery                                           
#PBS -M roko.plestina@cern.ch
             
##Job Configuration                                         
##Job Resources                                                     
#PBS -l walltime=10:00:00 
#PBS -l nodes=1:ppn=1                                                  
#PBS -l pmem=4gb 

##Create Work Area
CMSSWVER=MY_CMSSW_VERSION
#CMSSWVER=CMSSW_5_2_5_patch3
export SCRAM_ARCH=MY_SCRAM_ARCH
export OSG_APP=/osg/app                                         
export VO_CMS_SW_DIR=${OSG_APP}/cmssoft/cms                               
export CMS_PATH=${VO_CMS_SW_DIR}                                                                                
. ${CMS_PATH}/cmsset_default.sh
cd $TMPDIR
eval `scramv1 project CMSSW ${CMSSWVER}`
cd ${CMSSWVER}/
#rm -rf lib/ src/ config/ python/
rm -rf ./*
cp -r -d /scratch/hpc/plestina/HZZ_Legacy/SandBox/${CMSSWVER}/* ./
pwd
ls -altrh
cd src
eval `scramv1 runtime -sh`
#eval `scramv1 setup mcfm >& tmp.out`
edmPluginRefresh -p ../lib/$SCRAM_ARCH
#similar thing could be done with targz and copy to Worker node, than scram b ProjectRename and cmsenv and maybe edmPluginRefresh -p ../lib/$SCRAM_ARCH

#fix mcfm issue
rm -rf Pdfdata
cp -r ${CMSSW_BASE}/src/ZZMatrixElement/MELA/data/Pdfdata ./
# pwd
# ls -altrh



# these variables are setted-up by t3cooker t3cJobManager::makeJobs 
logdir=LOGDIR
# logfile=cmssw_JOBID.out
thisjobfileslist=THISJOBFILESLIST
lumimask=LUMIMASK
prefix=PREFIX
pset=PSET
jobid=JOBID

cd ${CMSSW_BASE}/src
echo "Node TMPDIR: "$TMPDIR
echo "Working directory: "$PWD
echo "Job running on `hostname` at `date`"
echo "cmsRun $pset files_load=$thisjobfileslist $lumimask PYCONFIG_PARAMS tag=_$jobid filePrepend=$prefix"
echo 
cmsRun $pset files_load=$thisjobfileslist $lumimask PYCONFIG_PARAMS tag=_$jobid filePrepend=$prefix
cmsRun_status=$?
echo "Job ended at `date` with exit code ${cmsRun_status}"
# ls -l ./*




#Setting up the directory for T#Cooker status
mkdir -p $logdir/done $logdir/failed
#if the job is done with exit code 0 then print number to file jobs_done
if [ $cmsRun_status = 0 ]; then
#   chmod +r ${prefix}/*_${jobid}.root
  touch $logdir/done/$jobid
else
  touch $logdir/failed/$jobid
fi







