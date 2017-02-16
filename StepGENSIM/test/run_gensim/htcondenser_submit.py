#!/usr/bin/env python
"""
This is the equivalent of running:
cmsRun config.py
htcondenser_setup.sh runs some shell commands to setup a CMSSW release.
We use the setup_script arg in JobSet() to define a setup script to run before
executing commands.
Then cmsRun is called as a simple example.
You must have a valid grid certificate, check with voms-proxy-info
"""
import os
import datetime
import tarfile
import argparse
import sys
import fnmatch
import logging
import htcondenser as ht

##__________________________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument('--exe', action='store', dest='exe', help='executable file for batch submission')
parser.add_argument('-i', '--file_dir', default='', help='Path to .root files')
parser.add_argument('-f', '--filename', dest='filename', default='*.root', help='LHE filename')
parser.add_argument('--dry_run', action='store_true', dest='dryRun', help='Dry run only')
parser.add_argument('--logging-level', default = 'INFO', choices = ['DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL'], help = "level for logging")
args   = parser.parse_args()

# Logging details
log_level = logging.getLevelName(args.logging_level)
log_handler = logging.StreamHandler()
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("ModifyLHEs")
logger.setLevel(log_level)
logger.handlers[:] = [ ]
logger.addHandler(log_handler)

##__________________________________________________________________||
hdfs_top         = os.path.join(os.path.sep, 'hdfs', 'user', os.environ['LOGNAME'], 'gensim_jobs')
jobdir_top       = os.getcwd()

print 'HDFS top: ', hdfs_top
logger.info("HDFS top: {0}".format(hdfs_top))
print 'Job dir top: ', jobdir_top
logger.info("Job dir top: {0}".format(jobdir_top))

##__________________________________________________________________||
jobdir_base_pre = os.path.join('job_{:%Y%m%d}'.format(datetime.datetime.now()) )
i = 0
while True:
    i += 1
    jobdir_base = '{}_{:03d}'.format(jobdir_base_pre, i)
    jobdir = os.path.join(jobdir_top, 'gensim_jobs', jobdir_base)
    if os.path.exists(jobdir): continue
    hdfs_store = os.path.join(hdfs_top, jobdir_base)
    if os.path.exists(hdfs_store): continue
    break

print 'Job dir base:', jobdir_base
if args.dryRun:
    print 'Job dir: ', jobdir

os.makedirs(jobdir)

##__________________________________________________________________||
log_store = os.path.join(jobdir, 'logs')
log_stem  = 'simple.$(cluster).$(process)'

filePath = args.file_dir
filename = args.filename
setup_script = os.path.join(jobdir_top,'htcondenser_setup.sh')
if filePath: filePath = os.path.abspath(filePath)
path, job_dirs, files = os.walk(filePath).next()
try:
    compfiles = [os.path.join(dirpath, f)
                 for dirpath, dirnames, files in os.walk(filePath)
                 for f in fnmatch.filter(files, filename)]
    
    if not compfiles:
        print "No file directories found"        
except ValueError:
    print "Could not form file list"    

cmssw_base = os.path.abspath(os.path.join(os.environ['CMSSW_BASE'], os.pardir))
input_tar_path = os.path.join(cmssw_base, 'cmssw.tar.gz')    
tar            = tarfile.open(input_tar_path, 'w:gz')

# Tar CMSSW and send to worker node
os.chdir(cmssw_base)
import subprocess
print 'Tarring ', subprocess.check_output(['du', '-cksh',cmssw_base]).split()[0].decode('utf-8') , 'in ', cmssw_base
tar.add(os.environ['CMSSW_BASE'].split('/')[-1])
tar.close()
os.chdir(jobdir_top)
sys.exit(1)

##__________________________________________________________________||
job_set = ht.JobSet(exe='cmsDriver.py',
                    copy_exe=False,
                    setup_script='setup_cmssw.sh',
                    filename=os.path.join(log_store, 'simple_cmssw_job.condor'),
                    out_dir=log_store, out_file=log_stem + '.out',
                    err_dir=log_store, err_file=log_stem + '.err',
                    log_dir=log_store, log_file=log_stem + '.log',
                    cpus=1, memory='50MB', disk='1',
                    certificate=True,  # !!! important for passing Grid certificate to jobs
                    hdfs_store=hdfs_store)

# Now add a Job
# Note that in this scenario, we are accessing the file over XRootD,
# and thus we don't need to add it to the input_files argument.
for file_path in compfiles:
    file_in  = file_path
    file_out = file_path.split('/')[-1]
    
job = ht.Job(name='cmssw_job',
             args=[configPath],
             input_files=[input_tar_path],
             output_files=[file_out],
             )

job_set.add_job(job)

# Now submit jobs
job_set.submit()
