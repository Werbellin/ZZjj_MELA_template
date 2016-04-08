#!/usr/bin/env python

import lheanalyzer

import ROOT


from ME_likelihood import *

print 'Loading Likelihoods' 
# specify the names of the SubProcess directories
ewk = likelihood('ewk_MG_dir/SubProcesses')
qcd = likelihood('qcd_MG_dir/SubProcesses')
print 'Finished loading Likelihoods' 



analysis = lheanalyzer.LHEAnalysis(sys.argv[1])


outfile = ROOT.TFile(sys.argv[2] ,"RECREATE")

ratio_plot = ROOT.TH1F("ME_ratio", "; w_{ewk} / w_{qcd}", 1000, 0, 0.5)

nevents = 0
for event in analysis :
    nevents += 1
    if nevents%100 == 0 :
        print 'Processing event', nevents

    particles = event.particles
    #    print  particles
    
    electrons = filter(lambda particle: particle.pdgId in [11, -11], particles)
    muons = filter(lambda particle: particle.pdgId in [13, -13], particles)

    outgoing_partons = filter(lambda particle: abs(particle.pdgId) in [1, 2, 3, 4, 5, 6, 21] and particle.pt > 0.5, particles)

    if len(electrons) != 2 or len(muons) != 2 or len(outgoing_partons) != 2 :
        print 'Incomplete 2e2mjj final state, skipping event'
        continue

    Z1 = []
    Z1.append(filter(lambda particle: particle.pdgId in [11], electrons)[0].getTLorentzVector())
    Z1.append(filter(lambda particle: particle.pdgId in [-11], electrons)[0].getTLorentzVector())

    Z2 = []
    Z2.append(filter(lambda particle: particle.pdgId in [13], muons)[0].getTLorentzVector())
    Z2.append(filter(lambda particle: particle.pdgId in [-13], muons)[0].getTLorentzVector())


    ME_ewk = ewk.get_likelihood(Z1, Z2, outgoing_partons[0].getTLorentzVector(), outgoing_partons[1].getTLorentzVector())
#    print ME_ewk
    ME_qcd = qcd.get_likelihood(Z1, Z2, outgoing_partons[0].getTLorentzVector(), outgoing_partons[1].getTLorentzVector())
    
    ME_ratio = ME_ewk/ME_qcd

    ratio_plot.Fill(ME_ratio)


ratio_plot.Write()
outfile.Close()

