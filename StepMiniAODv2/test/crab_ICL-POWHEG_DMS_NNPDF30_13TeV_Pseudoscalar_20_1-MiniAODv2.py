from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName     = 'NNPDF30_13TeV_Pseudoscalar_20_1_v1'
config.General.workArea        = 'ICL-POWHEG_DMS'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.JobType.pluginName = 'ANALYSIS'
config.JobType.psetName   = 'MiniAODv2_cfg.py'
config.JobType.outputFiles = ['MiniAODv2.root']

config.Data.inputDataset         = '/NNPDF30_13TeV_Pseudoscalar_20_1/pela-ICL-POWHEG_DMS_NNPDF30_13TeV_Pseudoscalar_20_1_v1-2015_25ns_Startup_PoissonOOTPU-AODSIM-32cf84fa/USER'
config.Data.inputDBS             = 'phys03'
config.Data.splitting            = 'EventAwareLumiBased'
config.Data.unitsPerJob          = 500
config.Data.totalUnits           = -1
config.Data.outLFNDirBase        = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication          = True
config.Data.outputDatasetTag     = 'ICL-POWHEG_DMS_NNPDF30_13TeV_Pseudoscalar_20_1_v1-2015_25ns_Startup_PoissonOOTPU-MiniAODv2'

config.Site.whitelist   = ["T2_UK_London_IC"]
config.Site.storageSite = 'T2_UK_London_IC'