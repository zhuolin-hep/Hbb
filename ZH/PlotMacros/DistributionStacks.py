import os
import json
import ROOT
import re
import sys

sys.path.append("./lib")
from Plot import scale_hist, plot_hist, plot_ratio, read_data
from FileIO import open_file, get_primary_name

MCinfo_list = []
factor = 1
sample_kind_list = ['sig', 'st', 'tt', 'dib', 'qcd', 'zjets']
hist_mu_list = ['RecDiMuon', 'RecMuonPlus', 'RecMuonMinus']
selection_list = ['Tight', 'Tight_Trigger', 'Loose', 'Loose_Trigger']
kinematic_list = ['pt', 'eta', 'phi']
kine_hist_dict = {'pt':'50, 0, 500', 'eta':'60, -6, 6', 'phi':'40, -4, 4'} # set the paramameters of TH1
match_dict = {'ZH_HToBB':'sig', 'TTTo':'tt', 'channel':'st', 'ZZ':'dib', 'QCD':'qcd', 'DYJetsToLL':'zjets'} # help categorize samples

# Construct histograms to analyze
for i in sample_kind_list:
    for j in selection_list:
        exec('{0}_RecDiMuon_{1}_M = ROOT.TH1F("{0}_RecDiMuon_{1}_M", "", 60, 75, 105)'.format(i, j))

for i in sample_kind_list:
    for j in hist_mu_list:
        for s in selection_list:
            for k in kinematic_list:
                for key, value in kine_hist_dict.items():
                    if key == k:
                        exec('{0}_{1}_{2}_{3} = ROOT.TH1F("{0}_{1}_{2}_{3}", "", {4})'.format(i, j, s, k, value))

# Load infomation of MC samples
with open('../Database/MCInfo.json') as MCinfo:
    MCinfo_list = json.load(MCinfo)

root_file_open = open_file('./Samples')
data_file_open = open_file('./Data')
data_hist_list = read_data(data_file_open, hist_mu_list, selection_list, kinematic_list, kine_hist_dict)
# Plot invariant mass spectrum and distributions for data
for i in data_hist_list:
    plot_hist(i)
'''
# Check the read_data function is right
with open("entries.txt", 'w') as entries:
    for i in data_hist_list:
        hist_name = i.GetName()
        hist_n = i.GetEntries()
        entries.write("Name: {}, N = {} \n".format(hist_name, hist_n))
'''
# Plot invariant mass spectrum
for fileopenname in root_file_open:
    for s in selection_list:
        exec('h_RecDiMuon_{0}_M = fileopenname.Get("demo/h_RecDiMuon_{0}_M")'.format(s))
    comparename = get_primary_name(root_file_open.index(fileopenname))
    
    # Read scale factor and check the factor for each dataset is right
    for i in MCinfo_list:
        for key, value in i.items():
            if key == 'primary_name':
                if value == comparename:
                    factor = i['factor_2018']
                    print("The primary name: ", value)
                    print("The factor is ", factor)
                    break
    
    # Scale histograms, the scale factor is from MCInfo.json
    for s in selection_list:
        exec("scale_hist(h_RecDiMuon_{0}_M, factor)".format(s))
    # Categorize MC samples
    for s in selection_list:
        for key, value in match_dict.items():
            if re.search(key, comparename):
                exec("{0}_RecDiMuon_{1}_M += h_RecDiMuon_{1}_M".format(value, s))

# Plot invariant mass specturm of MC samples
for i in sample_kind_list:
    for s in selection_list:
        exec('plot_hist({}_RecDiMuon_{}_M)'.format(i, s))

# Plot distributions (pt, eta, phi)
for fileopenname in root_file_open:
    for i in hist_mu_list:
        for s in selection_list:
            for k in kinematic_list:
                exec('h_{0}_{1}_{2} = fileopenname.Get("demo/h_{0}_{1}_{2}")'.format(i, s, k))
    comparename = get_primary_name(root_file_open.index(fileopenname))
    
    # Read scale factor and check the factor for each dataset is right
    for i in MCinfo_list:
        for key, value in i.items():
            if key == 'primary_name':
                if value == comparename:
                    factor = i['factor_2018']
                    print("The primary name: ", value)
                    print("The factor is ", factor)
                    break
    
    # Scale histograms, the scale factor is from MCInfo.json
    for i in hist_mu_list:
        for s in selection_list:
            for k in kinematic_list:
                exec("scale_hist(h_{}_{}_{}, factor)".format(i, s, k))
    # Categorize MC samples
    for i in hist_mu_list:
        for s in selection_list:
            for k in kine_hist_dict:
                for key, value in match_dict.items():
                    if re.search(key, comparename):
                        exec("{0}_{1}_{2}_{3} += h_{1}_{2}_{3}".format(value, i, s, k))

# Plot distributions of MC samples
for i in sample_kind_list:
    for j in hist_mu_list:
        for s in selection_list:
            for k in kinematic_list:
                exec('plot_hist({}_{}_{}_{})'.format(i, j, s, k))

# Plot the stack and Data/MC for invariant mass spectrum
for s in selection_list:
    exec('plot_ratio({1}_RecDiMuon_{0}_M, {2}_RecDiMuon_{0}_M, {3}_RecDiMuon_{0}_M, {4}_RecDiMuon_{0}_M, {5}_RecDiMuon_{0}_M, {6}_RecDiMuon_{0}_M, "RecDiMuon_{0}_M", data_hist_list)'.format(s, sample_kind_list[0], sample_kind_list[1], sample_kind_list[2], sample_kind_list[3], sample_kind_list[4], sample_kind_list[5]))

# Plot the stack and Data/MC for distributions
for h in hist_mu_list:
    for s in selection_list:
        for k in kinematic_list:
            exec('plot_ratio({3}_{0}_{1}_{2}, {4}_{0}_{1}_{2}, {5}_{0}_{1}_{2}, {6}_{0}_{1}_{2}, {7}_{0}_{1}_{2}, {8}_{0}_{1}_{2}, "{0}_{1}_{2}", data_hist_list)'.format(h, s, k, sample_kind_list[0], sample_kind_list[1], sample_kind_list[2], sample_kind_list[3], sample_kind_list[4], sample_kind_list[5]))
