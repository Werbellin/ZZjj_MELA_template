A simple toolkit to run MELA analysis from MadGraph code

Requirements:

For the ME code:
- LHAPDF and its python interface
- numpy (needed by the FORTRAN to Python library tool)

Tor run the example tree loop:
- ROOT
- pyROOT
- ?


How to run the example:

1) compile ME python libraries by calling "python compile_subprocesses.py" in [ewk, qcd]_MG_dir/SubProcesses respectively
2) run "python run_example.py" 


General workflow:


1) generate a process, e.g. 'generate p p > z z jj QCD=0, z > e+ e-, z > mu+ mu-'

2) create FORTRAN code via 'output standalone foo_bar'

3) Compile the FOTRAN code using the compile_subprocesses.py scipt

4) Implement custom copy of 'get_likelihood' of 'ME_likelihood.py'
    -the momenta of the final state particles need to be passed and the relevant permutations need to be considered

5) See mela_example.py on how to produce likelihoods 
 

