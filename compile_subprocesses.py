import os
"""
run this script from the SubProcesses directory to compile the FORTRAN code
(produces lots of stdout output)
"""

files = [f for f in os.listdir('.') if os.path.isdir(f)]

print files

for f in files :
    os.system('cd %s ; pwd; make matrix2py.so; cd ..'%(f))
