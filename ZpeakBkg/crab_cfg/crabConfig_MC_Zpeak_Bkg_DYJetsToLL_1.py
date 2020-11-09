from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'DYJetsToLL_1'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ZpeakBkg_cfg.py'
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '/DYJetsToLL_M-4to50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM'
config.Data.inputDBS = 'global'
config.Data.publication = True
config.Data.outputDatasetTag = 'DYJetsToLL_1'
config.Data.splitting = 'Automatic'

config.Site.storageSite = 'T2_CN_Beijing'