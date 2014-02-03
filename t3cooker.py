
#TODO
#include hadd
#include all dataset functions
#setup install
#add for case of no user_remote_dir
#

# _____ _____  ____            _                _       _    ____                  _          
#|_   _|___ / / ___|___   ___ | | _____ _ __   | | ___ | |__/ ___|  ___ _ ____   _(_) ___ ___ 
#  | |   |_ \| |   / _ \ / _ \| |/ / _ \ '__|  | |/ _ \| '_ \___ \ / _ \ '__\ \ / / |/ __/ _ \
#  | |  ___) | |__| (_) | (_) |   <  __/ | | |_| | (_) | |_) |__) |  __/ |   \ V /| | (_|  __/
#  |_| |____/ \____\___/ \___/|_|\_\___|_|  \___/ \___/|_.__/____/ \___|_|    \_/ |_|\___\___|
#
#########################################################
class T3CookerService(object):
        """This class is an entry point for T3Cooker,
        it checks options set by user and calls the executing 
        classes T3CookerJobCreator or T3CookerJobManager.
        """
        ############################################
        def __init__(self):
	  import os, sys, fnmatch
	  verbose=True
	  from optparse import OptionParser, OptionGroup
	  #import optparse
	  self.parser = OptionParser()  #there is also possibiblity to group options...Look into documentation.
	###Config options

	  self.configOps = OptionGroup(self.parser, "Configuration Options",
			  "With these options you choose file or directory which "
			  "will be used to perform something from \"Action options\".")
	  
	  self.configOps.add_option("--cfg", dest="ConfigFile", type="string", 
			help="specify path of your t3cooker configuration for creating jobs", metavar="T3COOKER_CFG", default="NO_CFG")
	  self.configOps.add_option("-c", dest="JobDir", type="string", 
			help="set your t3cooker directory to perform an action on it.", metavar="T3COOKER_DATA_DIR")
	  self.parser.add_option_group(self.configOps)		


	###Action options		
	  self.actionsOps = OptionGroup(self.parser, "Action Options",
			  "These options will perform something on cfg file "
			  "or dataset you choose with \"Config options\" .")
			  
	  self.actionsOps.add_option("--init", dest="SetupT3", action="store_true",
			help="set this once per session, grid and T3 initalization", default=False)
			
	  self.actionsOps.add_option("--create", dest="CreateJobs", action="store_true", 
			help="set this for creating jobs", default=False)
			
	  self.actionsOps.add_option("--status", dest="GetStatus", action="store_true", 
			help="set this to check job status", default=False)
			
	  self.actionsOps.add_option("--submit", dest="SubmitRange", type="string",
			help="submit jobs in range. Should specify range [\'all\' or list of numbers].", 
			metavar="<JOB_RANGE>", default="RANGE_NOT_SET")
			
	  self.actionsOps.add_option("--kill", dest="KillRange", type="string", 
			help="kill jobs in range. MUST specify range [\'all\' or list of numbers]", 
			metavar="<JOB_RANGE>", default="RANGE_NOT_SET")
	
	  self.actionsOps.add_option("--hadd", dest="HaddRange", type="string", 
			help="Hadd output files (.root) in range. MUST specify range [\'all\' or list of numbers]", 
			metavar="<JOB_RANGE>", default="RANGE_NOT_SET")		  
			
			
	  self.parser.add_option_group(self.actionsOps)

	###Parse all options
	  (self.options, self.args) = self.parser.parse_args()
        
        #########################################################  
        def cook(self):
	  self.userOpts = self.getOptionsSetByUser(self.parser) #this is dictionary
	  if self.checkOptions(self.userOpts) :
	    self.executeRequest(self.userOpts)
	  else:
	    self.parser.print_help()
	    self.parser.error("\n***Error: Bad choice of arguements. Read help and think.")
	  return
	  
	  
		
		
        #########################################################  
        def checkOptions(self, options):
	  """Cheking which options can go together
	    Cheking number of options
	    Checking format of options
	    
	    Possible combinations:
	    --cfg goes with [create and or submit] 
	    --c goes with [submit || kill || status]
	    --status can go alone 
	  """

	  #now let's check if combination of options can be executed
	  nopts=len(options)
	  if nopts == 0 :
	      return False
	    
	  keys = options.keys()
	  if "ConfigFile" in  keys:
	      #checkFile(options['ConfigFile'])
	      if nopts >3 :
		return False
	      if "CreateJobs" in keys and "SubmitRange" in keys:
		return True
	      if "CreateJobs" in keys and nopts==2 :
		return True  
	      else:
		return False
	      
	  elif "JobDir" in keys :
	      if nopts > 2 :
		return False
	      if "SubmitRange" in keys or "KillRange" in keys or "GetStatus" in keys :  
		return True
	      else :
		return False  
	    
	  elif nopts==1 and "GetStatus" in keys :
	      return True
	  elif "SetupT3" in keys :
	      return True
	  else:
	      return False

        #########################################################  
        def executeRequest(self,options):
	  """This method calls methods that according to options 
	    execute request. Now the options should be ok, i.e safe
	    after checking with checkOptions()
	  """
	  #print "Executing request: ",
	  #print options
	  keys = options.keys()
	  if "SetupT3" in keys:
	      self.t3setup()
	  if "ConfigFile" in  keys:
	      if "CreateJobs" in keys:
		if "SubmitRange" in keys :
		    ##if options['SubmitRange'] not in ['all','RANGE_NOT_SET' ] :
		    #if options['SubmitRange'] :	  
		        #print "T3Cooker: Usage ERROR ***"
		        #print "T3Cooker can not submit range for all datasets in config file."
		        #print "You should either provide range as \'all\' or leave the range empty! Exiting."
		        #return
		    #else:
		        creator = T3CookerJobCreator(options['ConfigFile'])
		        creator.create()
		        allDirs = creator.getJobDirs()
		        for jobDir in allDirs:
			  manager = T3CookerJobManager(jobDir)
			  manager.submit(options['SubmitRange'])
		else :
		    print "T3Cooker is creating jobs from config file :" + options['ConfigFile']
		    creator = T3CookerJobCreator(options['ConfigFile'])
		    creator.create()
	      
	  elif "JobDir" in keys :
	      manager = T3CookerJobManager(options['JobDir'])
	      if "SubmitRange" in keys or "KillRange" in keys or "GetStatus" in keys or "HaddRange" in keys:  
		if "SubmitRange" in keys :
		    manager.submit( options['SubmitRange'] )
		elif "KillRange" in keys :
		    manager.kill(options['KillRange'])
		elif "GetStatus" in keys:
		    manager.status()      
		elif "HaddRange" in keys:
		    manager.hadd(options['HaddRange'])      
	        
	  #print "Request executed!\n"
	  return 

        #########################################################  
        def getOptionsSetByUser(self, parser):
	  """Method checks which options where set by user.
	  """
	  #print "[getOptionsSetByUser]"
	  #defaultOpts   = parser.defaults
	  optKeys       = parser.defaults.keys()
	  optDefaultVals= parser.defaults.values()
	  optDefault_dict=dict(zip(optKeys,optDefaultVals))
	  
	  
	  
	  (options, args) = parser.parse_args()
	  #print options
	  optParsed_dict = vars(options)
	  optParsedVals = vars(options).values()
	  
	  userOptions={} # create empty dictionary
	  for k, v in optParsed_dict.iteritems():
	      if not v == optDefault_dict[k] :
		userOptions.update({k:v})
	  #print optDefaultVals
	  #print optParsedVals
	  #print userOptions
	  #print optKeys
	  #print defaults
	  return userOptions
	
        #########################################################  
        def t3setup(self):
	  import subprocess, shlex  
	  t3setup_args = shlex.split("bash /opt/exp_soft/cms/t3/t3setup")
	  t3setup = subprocess.Popen(t3setup_args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	  out, err = t3setup.communicate()
	  print out
	  print err
	  return





# _____ _____  ____            _                _       _      ____                _             
#|_   _|___ / / ___|___   ___ | | _____ _ __   | | ___ | |__  / ___|_ __ ___  __ _| |_ ___  _ __ 
#  | |   |_ \| |   / _ \ / _ \| |/ / _ \ '__|  | |/ _ \| '_ \| |   | '__/ _ \/ _` | __/ _ \| '__|
#  | |  ___) | |__| (_) | (_) |   <  __/ | | |_| | (_) | |_) | |___| | |  __/ (_| | || (_) | |   
#  |_| |____/ \____\___/ \___/|_|\_\___|_|  \___/ \___/|_.__/ \____|_|  \___|\__,_|\__\___/|_|   
#
#########################################################
class T3CookerJobCreator(object):
        """Create jobs for given datasets which means it has
	to create first file lists and than pass them to 
	the python script that launches cmssw code.
	TODO in the future: include option for any kind of 
	job on data i.e. simple root or something like that.
	I the job output directory is not set in config, then 
	all results shoud go to {job}/res subdirectory.
        """
        
        """The configuration will be copied to share directory
	of every dataset. Or maybe just the config for this 
	dataset. We'll see.
        """
        ############################################
        def __init__(self, configName):
#########################################################
	  print """

=================================================================

  _________________________              ______                
  ___  __/__|__  /__  ____/______ ______ ___  /_______ ________
  __  /   ___/_ < _  /     _  __ \_  __ \__  //_/_  _ \__  ___/
  _  /    ____/ / / /___   / /_/ // /_/ /_  ,<   /  __/_  /    
  /_/     /____/  \____/   \____/ \____/ /_/|_|  \___/ /_/     

	  
=================================================================
				        
	  """
	
	  print """Creating all jobs from """ + configName  	
	  import ConfigParser
	  #self._reserved_sections = ['T3COOKER','COMMON','CMSSW','USER']
	  self._reserved_sections = ['USER','T3COOKER','COMMON','CMSSW','EXE']
	  self.checkFile(configName)
	  try:
	      self._config = ConfigParser.SafeConfigParser()
	      #self._config.read([configName, 't3cooker_defaults.cfg'])
	      self._config.read([configName])
	  except ConfigParser.ParsingError, err:
	      print 'Could not parse:', err
	  self._stdParams = self.setStandardValuesFromConfig()
	  self._jobDirs = []   #the list gets filled during Create
	  #self._datasets = self.getDatasetsFromConfig()
	  #self._ui_working_dir = self._config.get('USER','ui_working_dir')
	  #print "INIT: params",
	  #print self._stdParams
        
        ############################################
        def getJobDirs(self):
	  return self._jobDirs

        ############################################
        def create(self):
	  """Here we take parameters for dataset and override _stdParams.
	    Then, for each dataset we apply parameters to create working
	    area and jobs.
	  """
	  
	  import os, copy
	  import rfio, fnmatch, string
	  import ConfigParser
	  
	  opts_in_dataset_sections = self.getValidDatasetsSectionsFromConfig()
	    
	  
	  #first remove file with duplicates if it existes
	  if os.path.exists('remove_us_from_storage.sh') :
	      os.remove('remove_us_from_storage.sh')
	  
	  for dataset, params in opts_in_dataset_sections.iteritems():
	      _thisDatasetParams = copy.deepcopy(self._stdParams)
	      _thisDatasetParams.update(opts_in_dataset_sections[dataset])
	      
	      print "-----------------------------------------------------------------"
	      print "%(dataset)s parameters: " %locals()
	      print "-----------------------------------------------------------------"
	      ### now create dataset directory tree
	      _thisDatasetDir = _thisDatasetParams['ui_working_dir'] + '/'+ dataset
	      self._jobDirs.append(_thisDatasetDir)
	      self.createDirs(_thisDatasetDir)
	      #create remote directory
	      _user_remote_dir=''
	      if _thisDatasetParams['user_remote_subdir'] != '' :
		_user_remote_dir = _thisDatasetParams['user_remote_dir'] +"/"+ _thisDatasetParams['user_remote_subdir']
	      elif _thisDatasetParams['user_remote_dir'] == '' :
		_user_remote_dir = _thisDatasetDir + '/res' 
	      else : 
		_user_remote_dir = _thisDatasetParams['user_remote_dir'] + '/' + dataset 
		
	      #_user_remote_dir = _thisDatasetParams['user_remote_dir'] + '/' + dataset 	
	      _thisDatasetParams.update({'user_remote_dir':str(_user_remote_dir)})
	      try:
		os.makedirs(_thisDatasetParams['user_remote_dir'])
	      except OSError, e:
		print str(e)
	      #now make file list splited using input_files_per_job
	      #first check for duplicated files: possible if used crab before
		  
	      inputFilesDirPrefix = _thisDatasetParams['input_files_se_prefix']+ "/"
	      inputFilesDirSufix  = _thisDatasetParams['datasetpath'] + "/"
	      inputFilesDirPrefix_2 = inputFilesDirPrefix
	      if _thisDatasetParams['type_of_executable']=='cmssw' :
		inputFilesDirPrefix_2 = ""
	      try:
		inputFilesAll = os.listdir(inputFilesDirPrefix + inputFilesDirSufix )  #os.system('rfdir ' + dpmPrefix + dpmDir + ' | awk \'{print $NF}\'')  #list of subdirectories 
		
	      except:
		inputFilesAll = rfio.listdir(inputFilesDirPrefix + inputFilesDirSufix )  #os.system('rfdir ' + dpmPrefix + dpmDir + ' | awk \'{print $NF}\'')  #list of subdirectories 
	        
	      if _thisDatasetParams['input_file_name_pattern'] != '':
		input_file_name_pattern = _thisDatasetParams['input_file_name_pattern']
		inputFiles = fnmatch.filter(inputFilesAll, input_file_name_pattern)
	      else :
		inputFiles = inputFilesAll
	      #print inputFiles
	      #now we should look for duplicates and skip them in the list	
	      inputFilesNoDupl = []
	      #inputFiles
	      duplicates = []
	      prefix_root_access_dpm = _thisDatasetParams['prefix_root_access_dpm']
	      for onefile in inputFiles :
		if onefile not in duplicates:
		    pattern= string.join(onefile.split('_')[:2],"_") +"_?_*.root"
		    onefilelist=fnmatch.filter(inputFiles, pattern)
		    duplicates.extend(onefilelist)
		    #if len(duplicates) < 10 :
		      #print "Duplicates:" + str(duplicates)
		    if len(onefilelist)>0:
		        latestfile=onefilelist.pop()
		        #duplicates.extend(onefilelist)
		        #if len(onefilelist) > 0 :
			  #print "consider removing:" + str(onefilelist)
		inputFilesNoDupl.append(prefix_root_access_dpm + inputFilesDirPrefix_2 + inputFilesDirSufix + onefile) #take the latest file produced			  
		#inputFilesNoDupl.append(inputFilesDirSufix + latestfile) #take the latest file produced
		#if len(inputFilesNoDupl) < 5 :
		  #print "Input files:" + str(inputFilesNoDupl)
		        
	      #first remove file with duplicates if it existes
	      
	      #findDuplCommand = 'findDuplicate.csh %(inputFilesDirPrefix)s%(inputFilesDirSufix)s >> remove_us_from_storage.sh' %locals()
	      #os.system(findDuplCommand)


	      #Continue creating job with the list
	      self.makeJobs(dataset, _thisDatasetParams, inputFilesNoDupl)
	      _thisDatasetParams.update({'njobs':str(self.njobs),'dataset':str(dataset)})
	      #print _thisDatasetParams
	      #import pprint 
	      #pp = pprint.PrettyPrinter(indent=4)
	      #pp.pprint(_thisDatasetParams)
	      
	      #finaly write configuration to files in share subdirectory
	      fcfg = open(_thisDatasetDir+'/share/t3cooker_all_datasets.cfg','w')
	      self._config.write(fcfg)
	      fcfg.close()
	      
	      _thisDatasetConf = ConfigParser.RawConfigParser(_thisDatasetParams)
	      fthiscfg = open(_thisDatasetDir+'/share/t3cooker.cfg','w')
	      _thisDatasetConf.write(fthiscfg)
	      fthiscfg.close()
	      
	      fdict = open(_thisDatasetDir+'/share/t3cooker.dict','w')
	      fdict.write(str(_thisDatasetParams))
	      fdict.close()
	      
	      statusdict=statusDict(_thisDatasetDir)
	      for job in range(1,self.njobs+1):
		      statusdict.dict[job]={"status" : "Created", "ID" : None} 
	      statusdict.save()
	    
	  pass
	  return 
        ############################################  
        def makeJobs(self, dataset, params, inputFiles, ):
	  """Here we print a job file and a py configuration that the job runs
	    Again we read configuration file and do the job spliting.
	    Output files should have some additional string in the name
	    in case job is run multiple times.
	  """
	  import os
	  #prepare input files chunks
	  inputFileChunks = self.chunks(inputFiles,params['input_files_per_job'])
	  #print str(inputFileChunks) 
	  print "Number of jobs generated = " + str(len(inputFileChunks))
	  self.njobs = len(inputFileChunks)
	  
	  for jobid in range(1,self.njobs+1):
	  
		  ##set echo
	        #set listfile = $1
	        #set samplename=`basename $listfile .list`
	        #set pythonfile=$samplename.py
	        
	        datasetAbsPath = str(os.path.abspath(params['ui_working_dir']+ '/'+ dataset))
	        cmssw_base_dir='~'  #just as initialization
	        cmssw_version=''  #just as initialization
	        my_scram_arch = os.environ['SCRAM_ARCH']
	        ##set analyzer="ZZ4lAnalyzer_cfg.py"
	        if params['type_of_executable']=='cmssw' :
		  fpyNameNoExt="cmssw_%(jobid)d" %locals()
		  fpyName = datasetAbsPath + '/job/cmssw_%(jobid)d.py' %locals()
		  foutNameNoExt = datasetAbsPath + '/res/cmssw_%(jobid)d' %locals()
		  try:
		      cmssw_base_dir = os.environ['CMSSW_BASE']
		      cmssw_version=os.environ['CMSSW_VERSION']
		  except KeyError, err:
		      print str(err)
		      print "You must configure your CMSSW environment first!"
		      raise
		    
	        else :
		  fpyNameNoExt="exec_%(jobid)d" %locals()
		  fpyName = datasetAbsPath + '/job/exec_%(jobid)d.py' %locals()
		  foutNameNoExt = datasetAbsPath + '/res/exec_%(jobid)d' %locals()
	        #writing python file that will be called by the job
	        #we could in principle avoid this by including var parsing to the 
	        #pset directly
	        pset=''
	        executable=''
	        exe_dir=''
	        if params['type_of_executable']=='cmssw' or params['type_of_executable']=='cmsRun' :
		  pset=params['pset']
	        else :		
		  import string
		  exe_full_path_list = params['executable'].split('/')
		  exe_dir = string.join(exe_full_path_list[:(len(exe_full_path_list)-1)],'/')
		  executable = exe_full_path_list[len(exe_full_path_list)-1]
		  
	        #prefix=params['user_remote_dir']+ '/'+ dataset+ '/'
	        prefix=params['user_remote_dir']+ '/'
	        sufix=str(jobid)
	        #read from template
	        templDir = os.environ['T3COOKER_BASE_DIR']
	        #fpytemplate = open(templDir+"/t3cooker_cmssw_py_template.py","r")
	        #t3cooker_py_template = fpytemplate.read()
	      
	        #py_replace_dic = {'PSET':str(pset),'PREFIX':str(prefix),'SUFIX':str(sufix)}
	        #this_t3cooker_py = self.replace_words(t3cooker_py_template, py_replace_dic)
	        #fpytemplate .close()
	        #fpy = open(fpyName,"w")
	        #fpy.write(this_t3cooker_py )
	        #fpy.close()
	        
	        if params['corrupted_files_list']!='': 	     
		  try:
		      fcorrupted_files_list = open(params['corrupted_files_list'],'r')
		  except IOError, e:
		      print 'Opening list with corrupted file paths.'
		      if e.errno == errno.EACCES :
			return "Cannot read"
			# Not a permission error.
			raise
		      else:
			os.strerror(errno.errorcode[e.errno])
			return  
		  corrupted_files_list = fcorrupted_files_list.readlines()
		  #print corrupted_files_list
		  fcorrupted_files_list.close()
		  
		  for file_entry in inputFileChunks[jobid-1]:
		      file_path=file_entry + '\n'
		      #print file_entry;
		      if file_path in corrupted_files_list:
			print 'Skipping corrupted file: ' + file_path
			inputFileChunks[jobid-1].pop(inputFileChunks[jobid-1].index(file_entry))
	        
	        
	        
	        logDir=str(os.path.abspath(params['ui_working_dir']+ '/'+ dataset+'/log/'))
	        thisJobFilesList = datasetAbsPath + '/job/lists/'+fpyNameNoExt+'.list' 
	        thisJobFiles=open(thisJobFilesList,"w")
	        thisJobFiles.write("\n".join(inputFileChunks[jobid-1]))
	        #print "thisJobFilesList: "+thisJobFilesList
	        thisJobFiles.close()
	        
	        
	        lumi_mask=params['lumi_mask']
	        if lumi_mask!='':
		  lumi_mask='goodlumi='+lumi_mask
	        pycfg_params = ''
	        options = ''
	        if params['type_of_executable']=='cmssw' :
		  #other python parameters CMSSW_BASE
		  pycfg_params = params['pycfg_params']
		  #print "parameters to pass : "+	str(pycfg_params)       
	        else:
		  options = params['options']
	        job_template = params['job_template']
	        #now create job to be ran on CE
	        fjobName = "job_%(jobid)d.sh" %locals()
	        fjob=open(datasetAbsPath + '/job/'+fjobName,"w")
	        if job_template=='':
		  fjobtemplate = open(templDir+"/t3cooker_cmssw_job_template.sh","r")
	        else :
		  fjobtemplate = open(params['job_template'],"r")
	        
	        t3cooker_job_template = fjobtemplate.read()
	        
	        job_replace_dic={}
	        if params['type_of_executable']=='cmssw' :
		  job_replace_dic={'MY_SCRAM_ARCH':my_scram_arch,'MY_CMSSW_BASE':str(cmssw_base_dir),'MY_CMSSW_VERSION':str(cmssw_version),
			     'FPYNAME':str(fpyName),'THISJOBFILESLIST':str(thisJobFilesList), 
			     'FOUTNAMENOEXT':str(foutNameNoExt) ,'JOBID':str(jobid),'LOGDIR':str(logDir),
			     'PYCONFIG_PARAMS':str(pycfg_params),'PREFIX':str(prefix),'PSET':str(pset),
			     'LUMIMASK':str(lumi_mask)
			     }
	        else :		
		  job_replace_dic={'THISJOBFILESLIST':str(thisJobFilesList), 
			     'FOUTNAMENOEXT':str(foutNameNoExt) ,'JOBID':str(jobid),'LOGDIR':str(logDir),
			     'OPTIONS':str(options),'PREFIX':str(prefix),'EXECUTABLE':str(executable),
			     'EXE_DIR':str(exe_dir),'LUMIMASK':str(lumi_mask)
			     }
	        
	        this_t3cooker_job = self.replace_words(t3cooker_job_template, job_replace_dic)
	        fjobtemplate .close()
	        fjob.write(this_t3cooker_job )
	        fjob.close()

	        #make job executable
	        os.chmod(datasetAbsPath + '/job/'+fjobName,0755)
	  return
	  
	  
        
        
        def replace_words(self,text, word_dic):
	  """
	  take a text and replace words that match a key in a dictionary with
	  the associated value, return the changed text
	  """
	  import re
	  rc = re.compile('|'.join(map(re.escape, word_dic)))
	  def translate(match):
	      return word_dic[match.group(0)]
	  return rc.sub(translate, text)
	
        ############################################  
        def chunks(self,l, n):
	  n=int(n)
	  return [l[i:i+n] for i in range(0, len(l), n)]
        ############################################  
        def getValidDatasetsSectionsFromConfig(self):
	  """Reads configuration and creates a list of datasets
	    to be used with jobs. 
	  """
	  _validDatasetSectionsDict={}
	  
	  ####get list of sections
	  print self._config.sections()
	  #_datasets=[] # here we will put datasets 
	  for sec in self._config.sections() :
	    if sec not in self._reserved_sections :
	      if self._config.has_option(sec,'datasetpath') :
		_validDatasetSectionsDict.update({sec : dict(self._config.items(sec))})
	      else:
		print "[WARNING] Dataset section %(sec)s is missing \'datasetpath\' option. It WILL NOT be created!" %locals()
	      #_datasets.append(section)
	  pass
	  return _validDatasetSectionsDict
	
        ############################################  
        def setStandardValuesFromConfig(self):
	  import ConfigParser
	  _stdParams={'pset':'','input_files_per_job':0, 'ui_working_dir':'', 'user_remote_dir':'',
		    'pycfg_params':'','job_submiter':'/opt/exp_soft/cms/t3/t3submit', 'batch_queue':'llr',
		    'type_of_executable':'cmssw','input_files_se_prefix':'', 'job_template':'', 'lumi_mask':'',
		    'executable':'','options':'', 'input_file_name_pattern':'','corrupted_files_list':'',
		    'prefix_root_access_dpm':'', 'user_remote_subdir':''
		    }
		    
	  #print "Before DEFAULT:" 
	  #print _stdParams
	  _stdParams.update(dict(self._config.items('DEFAULT')))  #first read from default
	  #print "After DEFAULT:"
	  #print _stdParams
	  #check if MUST_HAVE sections are there - there is no default for these sections
	  #must_have_sect_opts = ['T3COOKER','CMSSW']
	  #must_have_options = ['pset','input_files_per_job']
	  #must_have_opts = {'T3COOKER':[], 'CMSSW':['pset','input_files_per_job']}  #Fill here empty sections if you want to set something as MUST_HAVE
	  must_have_opts = {'T3COOKER':[]}  #Fill here empty sections if you want to set something as MUST_HAVE
	  must_have_opts_int = ['input_files_per_job']
	  for sec,opts in must_have_opts.iteritems() :
	    ##if mustsect not in 
	    for opt in opts:
	      try: 
		if opt in must_have_opts_int:
		    _stdParams[opt] = self._config.getint(sec,opt)
		else:  
		    _stdParams[opt] = self._config.get(sec,opt)
	      #except ConfigParser.NoSectionError, ConfigParser.NoOptionError, err:
	      except ConfigParser.NoOptionError, err:	
		print str(err)
		raise
	  #print "After MUST_HAVE:"
	  #print _stdParams
	  #other_opts_cfg_default = dict(self._config.items('DEFAULT')) #
	  #other_opts_cfg = {}
	  import pprint 
	  pp = pprint.PrettyPrinter(indent=4)
	  for sec in self._reserved_sections:
	      if self._config.has_section(sec):
		print "Updating from section " + sec
		#print dict(self._config.items(sec))
		pp.pprint(dict(self._config.items(sec)))
		
		#print self._config.items(sec)
		_stdParams.update(dict(self._config.items(sec)))
	  #print "After REST:"
	  #print _stdParams

	  return _stdParams
	
        ############################################  
        def createDirs(self, datasetpath):
	  import os
	  for leafDir in ['job','log','res','share','job/lists'] :
	    finalDir = "%(datasetpath)s/%(leafDir)s" % locals()
	    #print finalDir
	    if not os.path.exists(finalDir) :
	        os.makedirs(finalDir)
	    else :
	        print """Dir already exists!!! ---> %(finalDir)s """ %locals()
	        return
	    #if verbose :
	    #print "Creating directory: " + finalDir
	  return
        ############################################
        ###Check if file is readable - raise error if not
        def checkFile(self,filename) :  
	  import errno
	  print "checking file"
	  try:
	      fp = open(filename)
	  except IOError, e:
	      if e.errno == errno.EACCES:
		return "Cannot read"
	      # Not a permission error.
	      raise
	  else:
	      return
	
	
# _____ _____  ____            _                _       _     __  __                                   
#|_   _|___ / / ___|___   ___ | | _____ _ __   | | ___ | |__ |  \/  | __ _ _ __   __ _  __ _  ___ _ __ 
#  | |   |_ \| |   / _ \ / _ \| |/ / _ \ '__|  | |/ _ \| '_ \| |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '__|
#  | |  ___) | |__| (_) | (_) |   <  __/ | | |_| | (_) | |_) | |  | | (_| | | | | (_| | (_| |  __/ |   
#  |_| |____/ \____\___/ \___/|_|\_\___|_|  \___/ \___/|_.__/|_|  |_|\__,_|_| |_|\__,_|\__, |\___|_|   
#                                                                                      |___/         	
#########################################################
class T3CookerJobManager(object):
        """This class is called when submitting, asking status
	 or killing jobs. To work it needs to know about your
	 path of production i.e. '-c [ui_working_dir]/[dataset]'
	 option has to be used. It should be given the range, 
	 and if no range is provided it takes 'all' as argument
	 in case of submit and 'None' in case of killing.
	 Status is always returned for all the jobs. 
	 
	 To get the information about the jobs, status is looking 
	 in the log subdir containing list of failed and done jobs.
	 If the job is not found, it looks if it is running with qstat 
	 command,
        """
        
        ############################################
        def __init__(self, datasetDir):
	  import os
	  try:
	      self._datasetDir  = os.path.abspath(datasetDir)
	  except IOError, e:
	      if e.errno == errno.EACCES:
	        return "No directory!"
	      raise
	  self._datasetDir  = os.path.abspath(datasetDir)
	  import ConfigParser
	  try:
	      self._config = ConfigParser.SafeConfigParser()
	      self._config.read([self._datasetDir+'/share/t3cooker.cfg'])
	  except ConfigParser.ParsingError, err:
	      print 'Could not parse:', err
	  self.configDict=dict(self._config.items('DEFAULT'))

	  



        
        ############################################
        def submit(self, jobsInRange):
	  self.checkDirTree(self._datasetDir)
	  _jobsRange = self.getJobList(jobsInRange)
	  import os
	  import re
	  import subprocess, shlex
	  import progressbar #new ROKO
	  
	  njobs=len(_jobsRange)
	  progress = progressbar.AnimatedProgressBar(end=njobs, width=100)
	  
	  datasetDir = self._datasetDir
	  submiter_tool = str(self.configDict['job_submiter'])
	  batch_queue = str(self.configDict['batch_queue'])
	  job_nice_name = str(self.configDict['dataset'])
	  nsuccess=0
	  
	  print
	  print "-----------------------------------------------------------------"
	  print "Dataset:  " + job_nice_name 
	  print "-----------------------------------------------------------------"
	  if njobs>0 :
	      if njobs==1:
		what='job'
	      else:
		what='jobs'
	      print "Launching %(njobs)d %(what)s to T3 ... can take some time ..."%locals()
	  else:
	      print "Size of job range is 0, so nothing is submited. Try providing range."


	  statusdict=statusDict(datasetDir)
	  

	  #jobidre=re.compile("^\s*\d+\.llrt3\.in2p3\.fr\s*$")
	  jobidre=re.compile("^\s*\d+\.torx\.ufhpc\s*$")

	  submitted_jobs=[]
	  for job in _jobsRange :
	      if statusdict.dict[job]["status"] == "Created" or statusdict.dict[job]["status"] == "Killed" :
		      #print "Submitting Job %s" % job 
		      #t3submit_args = shlex.split("%(submiter_tool)s -m a -k eo -N %(job_nice_name)s_%(job)s -q %(batch_queue)s %(datasetDir)s/job/job_%(job)s.sh"%locals())
		      t3submit_args = shlex.split("%(submiter_tool)s -N %(job_nice_name)s_%(job)s -q %(batch_queue)s %(datasetDir)s/job/job_%(job)s.sh"%locals())
		      t3submit = subprocess.Popen(t3submit_args,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		      jobid=t3submit.stdout.readline()
		      if jobidre.match(jobid) :
			      nsuccess+=1
			      progress + 1 #new ROKO
			      #print progress
			      progress.show_progress() #new ROKO
			      statusdict.dict[job]["status"]="Submitted"
			      statusdict.dict[job]["ID"]=jobid
			      #print "Job %s succesfully submitted" % job
			      submitted_jobs.append(job)
		      else:
			      print "Job %s submission failed" % job
	      else:
		      print "Job %s cannot submitted being in state %s" % (job,statusdict.dict[job]["status"])



	      
	  submitted_jobs_str=self.printCrabLike(submitted_jobs)
	  print '\nSubmitted %(nsuccess)d/%(njobs)d : %(submitted_jobs_str)s' %locals(),
	  

	  statusdict.save()
	  
	  return
	
        ############################################
        def kill(self, jobsInRange):
	  self.checkDirTree(self._datasetDir)
	  import os, subprocess, shlex

	  statusdict=statusDict(self._datasetDir)
	  nsuccess=0

	  job_nice_name = str(self.configDict['dataset'])
	  print
	  print "-----------------------------------------------------------------"
	  print "Dataset:  " + job_nice_name 
	  print "-----------------------------------------------------------------"


	  _jobsRange = self.getJobList(jobsInRange)
	  njobs=len(_jobsRange)	  
	  killed_jobs=[]
	  for job in _jobsRange:
		  if statusdict.dict[job]["status"]=="Done" or statusdict.dict[job]["status"]=="Failed" or statusdict.dict[job]["status"]=="Aborted":
			  print "Job %s is in a final status %s. Putting it in Killed state" % (job,statusdict.dict[job]["status"])
			  killed_jobs.append(job)
			  nsuccess+=1
			  statusdict.dict[job]["status"]="Killed"
		  elif statusdict.dict[job]["status"]=="Created":
			  print "job %s is in Created status, it cannot be killed" % job
		  else :
			  qdel=subprocess.Popen( shlex.split("/usr/bin/qdel %s 1>/dev/null 2>&1;echo 'EXIT='$?" % statusdict.dict[job]["ID"]),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
			  #print "Killing job %s. Run status to verify" % job
			  killed_jobs.append(job)
			  nsuccess+=1
			  statusdict.dict[job]["status"]="Killing" 
			  #statusdict.dict[job]["status"]="Killed"
			  
	  killed_jobs_str=self.printCrabLike(killed_jobs)
	  print 'Killed %(nsuccess)d/%(njobs)d : %(killed_jobs_str)s' %locals()
	  print "Run --status to verify killing."

	  statusdict.save()
	  pass
	  return 
	
	
        ############################################
        def status(self):
	  import os
	  import string,re
	  import subprocess,shlex

	  
	  statusdict=statusDict(self._datasetDir)

          #Title
	  job_nice_name = str(self.configDict['dataset'])
	    
	  print
	  print "-----------------------------------------------------------------"
	  print "Dataset:  " + job_nice_name 
	  print "-----------------------------------------------------------------"

	  
	  #Checking Done and Failed jobs
	  self.checkDirTree(self._datasetDir)

	  #qstat informations
	  qstat_list={}
	  #qstat=subprocess.Popen( shlex.split("/usr/bin/qstat @llrt3"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	  #qstatre=re.compile("^\d+\.llrt3")
	  qstat=subprocess.Popen( shlex.split("/usr/bin/qstat @torx"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	  qstatre=re.compile("^\d+\.torx")
	  
	  for line in qstat.stdout.readlines():
		  #print "**** Before matching: "+line
		  if qstatre.match(line):
			#print line
			qstat_list[line.rsplit()[0].split('.')[0]]=line.rsplit()[4]  
			#print line.rsplit()[4]
			#print "Check number : "+line.rsplit()[0].split('.')[0]


	  for job in  statusdict.dict:
		  
		  #print job
		  if os.path.exists(self._datasetDir+"/log/done/"+str(job)):
			  statusdict.dict[job]["status"]="Done"
			  subprocess.Popen( shlex.split("rm "+self._datasetDir+"/log/done/"+str(job)),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		  elif os.path.exists(self._datasetDir+"/log/failed/"+str(job)):
			  statusdict.dict[job]["status"]="Failed"
			  subprocess.Popen( shlex.split("rm "+self._datasetDir+"/log/failed/"+str(job)),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		  elif statusdict.dict[job]["status"] in ["Created","Aborted","Killed","Done","Failed"]:
			  continue
		  elif str(statusdict.dict[job]["ID"]).split('.')[0] in qstat_list:
			  statusdict.dict[job]["status"]=qstat_list[str(statusdict.dict[job]["ID"]).split('.')[0]]
		  elif statusdict.dict[job]["status"] == "Killing":
			  statusdict.dict[job]["status"] = "Killed"
		  else:
			  statusdict.dict[job]["status"]="Aborted"
		
	  created_jobs=[]
	  done_jobs=[]
	  failed_jobs=[]
	  aborted_jobs=[]
	  killed_jobs=[]
	  running_jobs=[]
	  queued_jobs=[]
	  #printing job list
	  for job in statusdict.dict:
	        job_status = statusdict.dict[job]["status"]
	        if job_status=="R": job_status="Running"
	        if job_status=="Q": job_status="Queued"
	        #print "%s     %s" % (job,statusdict.dict[job]["status"])
	        if int(job)>1 and (int(job)-1)%10==0 : print "-------------------------------"
	        #print '{0:10d} {1:20}'.format(job, job_status )
	        print '%-5d      %s' % (job,job_status )
	        #print "%s     %s     " % (job,job_status )
	        #print "%s     %s" % (job,job_status )
	        if job_status=="Created" :
		  created_jobs.append(str(job))
	        elif job_status=="Aborted" :
		  aborted_jobs.append(str(job))
	        elif job_status=="Killed" :
		  killed_jobs.append(str(job))
	        elif job_status=="Done" :
		  done_jobs.append(str(job))
	        elif job_status=="Failed" :
		  failed_jobs.append(str(job))
	        elif job_status=="Running" :
		  running_jobs.append(str(job)) 
	        elif job_status=="Queued" :
		  queued_jobs.append(str(job)) 
			  
	  print "-----------------------------------------------------------------"
	  
	  
	  bold = "\033[1m"
	  reset = "\033[0;0m"
	  #print "I want " + bold + "this" + reset + " text to be bold."
	  import math
	  fdict=open(self._datasetDir+'/share/t3cooker.dict','r')
	  theDict = eval(fdict.read())
	  #print theDict
	  njobs = int(theDict['njobs'])
	  width = int(math.log10(njobs))+1
	  #print "width = "+ str(width)
	  print 			   "*** Job Summary ***"
	  print 			   "Dataset  %*s  : %s%s%s" % (width,"",bold,job_nice_name,reset)
	  if len(done_jobs)   >0 : print 'Done    [%*d] : %s' % (width,len(done_jobs),self.printCrabLike(done_jobs))
	  if len(running_jobs)>0 : print 'Running [%*d] : %s' % (width,len(running_jobs),self.printCrabLike(running_jobs))
	  if len(queued_jobs) >0 : print 'Queued  [%*d] : %s' % (width,len(queued_jobs),self.printCrabLike(queued_jobs))
	  if len(aborted_jobs)>0 : print 'Aborted [%*d] : %s' % (width,len(aborted_jobs),self.printCrabLike(aborted_jobs))
	  if len(created_jobs)>0 : print 'Created [%*d] : %s' % (width,len(created_jobs),self.printCrabLike(created_jobs))
	  if len(failed_jobs) >0 : print 'Failed  [%*d] : %s' % (width,len(failed_jobs),self.printCrabLike(failed_jobs))
	  if len(killed_jobs) >0 : print 'Killed  [%*d] : %s' % (width,len(killed_jobs),self.printCrabLike(killed_jobs))
	  	    
	  remote_dir = str(self.configDict['user_remote_dir'])
	  
	  print 			   "Storage  %*s  : %s" % (width,"",remote_dir)

	  if (len(failed_jobs)+len(aborted_jobs)+len(killed_jobs)+len(created_jobs)) > 0 :
	        print "[T3Cooker] *** You might want to submit jobs in Aborted/Created/Failed/Killed state with --submit <range> option."

	  statusdict.save()

	  
        ############################################
        def hadd(self, jobsInRange):
	  self.checkDirTree(self._datasetDir)
	  print "Hadd not yet implemented!"
	  _jobsRange = self.getJobList(jobsInRange)
	  pass
	  return 
		  
	
        ############################################
        def getJobList(self,rawJobRange):
	  """Here we create a list from the input string.
	    For the moment we only parse comma separated values 
	    and not ranges like XXX-YYY (TODO).
	    We also need to include the check if the rawJobRange
	    has only integers and commas
	    
	  """
	  import string  

	  
	  
	  fdict=open(self._datasetDir+'/share/t3cooker.dict','r')
	  theDict = eval(fdict.read())
	  #print theDict
	  njobs = int(theDict['njobs'])
	  fullListofJobs=range(1,njobs+1)
	  if rawJobRange=='RANGE_NOT_SET' or  string.lower(rawJobRange)=='all':
	      return fullListofJobs

	  #remove all job numbers that dont exist by intersecting with full range
	  commaSepList=list(set(fullListofJobs).intersection( self.convert(rawJobRange) ) )
	  #remove all job nubers that dont exist
	  #print commaSepList 
	  return commaSepList
	  
        ############################################	  
        #convert range expression to list of numbers
        def convert(self, x):
	    
	  result = []
	  for part in x.split(','):
	      if '-' in part:
		a, b = part.split('-')
		try :
		    a, b = int(a), int(b)
		except ValueError,e :
		    print "---> Not a valid number (or range) for job." %locals()
		    raise
		result.extend(range(a, b + 1))
	      else:
		a = int(part)
		result.append(a)
	  return sorted(set(result))
        ############################################
        #check if get list of jobs from arguments  
        def checkDirTree(self, dataset):
	  #print """Checking existence of dataset directory: """ + dataset
	  import errno, os
	  #print "checking file"
	  try:
	      os.stat(dataset)
	  except:
	      print "Cannot read directory for %(dataset)s"%locals()
	      raise
	  return
        ############################################
        def printCrabLike(self, num_list) :
	
	  import itertools
	  def ranges(self, i):
	      for a, b in itertools.groupby(enumerate(i), lambda (x, y): y - x):
		b = list(b)
		yield b[0][1], b[-1][1]
	    
	  jobList=[]
	  for i in num_list:
	      try:
		jobList.append(int(i))
	      except:
		pass
	      
	  jobRanges=list(ranges(self,sorted(jobList)))
	  
	  jobsStr = ""
	  nranges=len(jobRanges)
	  rindex=0
	  for r in jobRanges :
	      #one_range = ""
	      if (r[1]-r[0]) > 1 :
		one_range = str(r[0])+"-"+str(r[1])
	      elif (r[1]-r[0]) == 1 :
		one_range = str(r[0])+","+str(r[1])
	      elif r[0]==r[1] :
		one_range = str(r[0])
	      if rindex < (nranges-1) :
		one_range+=','
	      rindex+=1	
	      
	      jobsStr+=one_range
	  return jobsStr
	  
	  
#########################################################
class statusDict(object):
	"""
	A class holding information about the status of particular jobs.
	"""
	def __init__(self,dir):
		import pickle, os
		self.file=dir+"/share/status.dict"
		if os.path.exists(self.file):
			fh=open(self.file,'r');		
			self.dict=pickle.load(fh)
			fh.close()
		else:
			self.dict={}
	def save(self):
		import pickle
		fh=open(self.file,'w');
		pickle.dump(self.dict,fh)
		fh.close()

		
