import ROOT

ROOT.gROOT.SetBatch(1)
fGen = ROOT.TFile("./higgsPt.root")
fReco = ROOT.TFile("./ZH_HToBB_ZToLL_M125_13TeV_powheg_pythia8.root")

hGen = fGen.Get("higgsPt")
hGen.GetYaxis().SetTitle("Nevents / 10 [GeV]")
hGen.SetStats(0)
hGen.SetMarkerStyle(32)
hGen.SetLineColor(ROOT.kRed)
hGen.SetMarkerColor(ROOT.kRed)
zhtree = fReco.Get("demo/ZHCollection")
zhtree.Draw("HiggsPt >> hReco(50, 0, 500)")
hReco = ROOT.gROOT.FindObject("hReco")
hReco.GetYaxis().SetTitle("Nevents / 10 [GeV]")
hReco.SetStats(0)
hReco.SetMarkerStyle(24)
hReco.SetMarkerColor(ROOT.kAzure + 4)
hReco.SetLineColor(ROOT.kAzure + 4)

# Scale histograms to 0.271416347 fb^-1
hGen.Scale(0.271416347 / ((10000 / 0.07618) / 1000))
hReco.Scale(4.467044268740913e-06)

c = ROOT.TCanvas()
upperPad = ROOT.TPad("upperPad", "upperPad", 0., 0.3, 1., 1.)
lowerPad = ROOT.TPad("lowerPad","lowerPad", 0., 0., 1., 0.3)
upperPad.Draw()
lowerPad.Draw()
upperPad.SetTicks(1, 1)
upperPad.SetLogy()
upperPad.SetBottomMargin(0.)
#hGen.SetMinimum(3e-9)
hGen.SetMaximum(1)
upperPad.cd()
cmsTag = ROOT.TLatex(0.13, 0.917, "#scale[1.1]{CMS}")
cmsTag.SetNDC()
cmsTag.SetTextAlign(11)
cmsTag2 = ROOT.TLatex(0.2, 0.917, "#scale[0.825]{#bf{#it{Private}}}")
cmsTag2.SetNDC()
cmsTag2.SetTextAlign(11)
cmsTag3 = ROOT.TLatex(
	0.90, 0.917, "#scale[0.9]{#bf{0.271 fb^{-1} (13 TeV, 2018)}}")
cmsTag3.SetNDC()
cmsTag3.SetTextAlign(31)
hGen.Draw()
hReco.Draw("same")
cmsTag.Draw("same")
cmsTag2.Draw("same")
cmsTag3.Draw("same")
lowerPad.cd()
lowerPad.SetTicks(1, 1)
lowerPad.SetGridy()
lowerPad.SetTopMargin(0.)
lowerPad.SetBottomMargin(0.3)
hRatio = ROOT.TGraphAsymmErrors()
hRatio.Divide(hReco, hGen, 'pois')
hRatio.GetXaxis().SetTitleSize(0.1)
hRatio.GetXaxis().SetLabelSize(0.08)
hRatio.GetXaxis().SetTitleOffset(1)
hRatio.GetXaxis().SetLimits(0, 500)
hRatio.GetXaxis().SetTitle("p_{T}^{dijet} [GeV]")
hRatio.GetYaxis().SetNdivisions(505)
hRatio.GetYaxis().SetRangeUser(0, 1)
hRatio.GetYaxis().SetTitle("Signal Strength")
hRatio.GetYaxis().SetTitleSize(0.08)
hRatio.GetYaxis().SetLabelSize(0.08)
hRatio.GetYaxis().SetTitleOffset(0.4)
hRatio.SetMarkerStyle(21)
hRatio.Draw("AP")

upperPad.cd()
leg = ROOT.TLegend(0.63, 0.70, 0.86, 0.87)
leg.AddEntry(hGen, "MadGraph5@NLO", "PE")
leg.AddEntry(hReco, "Powheg", "PE")
leg.AddEntry(hRatio, "Ratio", "PE")
leg.Draw("same")

c.SaveAs("./ratio.pdf")