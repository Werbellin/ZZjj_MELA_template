import os
#import multiprocessing
import time

def runLHEAnalysis((inputFile, outputFile, logFile)) :
#    os.system('python mela_example.py %s %s > %s' % (inputFile, outputFile, logFile))
    os.system('python mela_example.py %s %s' % (inputFile, outputFile))




inputList = [
'ZZjj_2e_2mu_qcd_v1_test', 
'ZZjj_2e2mu_ewk_v1_test'
]

jobs = []

for i in inputList :
    jobs.append((i + '.lhe', i + '.root', i + '.log'))


print time.strftime('%X %x %Z')
for j in jobs :
    runLHEAnalysis(j)


# use this to run several jobs 
#
#pool = multiprocessing.Pool(4)
#pool.map(runLHEAnalysis, jobs)
#print time.strftime('%X %x %Z')
#os.system("python new_analyze.py  ~/data/Samples_Nicola/gen2je-e-e-e_S+B+I_mjjJets_13TeV.LHE/gen100.lhe blubbbbb3.root > blubb3.log")
