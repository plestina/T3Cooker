#import FWCore.ParameterSet.VarParsing as VarParsing
#options = VarParsing.VarParsing('standard')


##----------------------------------------------------------------------
## Setup 'analysis'  options
##----------------------------------------------------------------------
#from ZZAnalysis.Tools.ZZAnalysisOptions import getSkimStepOptions
## you can add as much options in this file and make cfg highly flexible
## and avoid making many cfg files with just few different parameters
##-----------------------------------------------------------------------------------------------------
##EXAMPLE; cmsRun zzPATSkim.py maxEvents=10 isMC=0 applySkim=1 dataset=Jan16ReReco globaltag=FT_R_42_V24
##------------------------------------------------------------------------------------------------------
#options=getSkimStepOptions()  #already parsed in this function

#print "cmsRun with options: "
#print "===================="
#print options


#DON'T TOUCH
### suffix: 


# setup default options
#options.output = "output.root"
#options.files = "file1.root"
#options.maxEvents = 10

# get and parse the command line arguments
#options.parseArguments()

execfile("PSET")
process.source.fileNames = cms.untracked.vstring(options.files)
process.TFileService.fileName=cms.string('PREFIXZZAnalysis4l_SUFIX.root')
process.ZZ4muAnalysis.TreeFile=cms.untracked.string('PREFIXZZ4muAnalysisTree_SUFIX.root')
process.ZZ4eAnalysis.TreeFile=cms.untracked.string('PREFIXZZ4eAnalysisTree_SUFIX.root')
process.ZZ2mu2eAnalysis.TreeFile=cms.untracked.string('PREFIXZZ2mu2eAnalysisTree_SUFIX.root')
