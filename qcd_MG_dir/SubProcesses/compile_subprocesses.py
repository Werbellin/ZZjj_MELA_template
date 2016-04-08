import os


files = [f for f in os.listdir('.') if os.path.isdir(f)]

print files

for f in files :
    os.system('cd %s ; pwd; make matrix2py.so; cd ..'%(f))

#for root, dirs, files in os.walk(".", topdown=False):
#    for name in dirs:
#        print(os.path.join(root, name))
