A simple toolkit to run MELA analysis from MadGraph code

Manual:

1) generate a process, e.g. 'generate p p > z z jj QCD=0, z > e+ e-, z > mu+ mu-'
2) create FORTRAN code via 'output standalone foo_bar'
3) Compile the FOTRAN code using the compile_subprocesses.py scipt
4) Implement custom copy of 'get_likelihood' of 'ME_likelihood.py'
    -the momenta of the final state particles need to be passed and the relevant permutations need to be considered
5) See mela_example.py on how to produce likelihoods 
 

