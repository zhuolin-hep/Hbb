import FWCore.ParameterSet.Config as cms

process = cms.Process("ZHTest")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False),
SkipEvent = cms.untracked.vstring('ProductNotFound'))

process.source = cms.Source("PoolSource", fileNames =
        cms.untracked.vstring('root://cmsxrootd.fnal.gov//store/mc/RunIIAutumn18MiniAOD/ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/100000/072DBADE-6D59-2241-8E5A-EADFB942C666.root'))

process.demo = cms.EDAnalyzer("ZHTest",
                                       muonTag = cms.InputTag("slimmedMuons"),
                                       vertexTag = cms.InputTag("offlineSlimmedPrimaryVertices"),
                                       triggerTag = cms.InputTag("TriggerResults", "", "HLT"),
                                       HLTPath = cms.string("HLT_IsoMu20_v*"),
                                       jetTag = cms.InputTag("slimmedJets"),
                                       bTag = cms.string("pfDeepCSVJetTags"),
                                       #GenPartTag  = cms.InputTag("prunedGenParticles"),
                                       UseRochCorr = cms.untracked.bool(False),
                                       RndmSeed    = cms.untracked.uint32(2345)
)

process.TFileService = cms.Service("TFileService",
          fileName = cms.string('ZHTree.root')
)

process.p = cms.Path(process.demo)