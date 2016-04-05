#!/usr/bin/env python
from ME_likelihood import *

print 'Loading Likelihoods' 
# specify the names of the SubProcess directories
ewk = likelihood('2e2mujj_QED')
qcd = likelihood('2e2mujj_QCD')
print 'Finished loading Likelihoods' 

ME_ewk = math.log(ewk.get_likelihood(...))
ME_qcd = math.log(qcd.get_likelihood(...))
ME_ratio = ME_ewk  -  ME_qcd
