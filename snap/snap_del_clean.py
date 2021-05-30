from datetime import datetime
from time import gmtime, strftime
import os
import time
import datetime
import json
import subprocess
import sys
from sys import argv
import numpy as np

# This line takes the supplied argument, which is the .json script of the instances.
# The .json script should never come with .json at the end.
projectn = sys.argv[1]

DATE = time.strftime('%d-%m-%Y')

#Opening the .json supplied file as, and assign it to "instances"
f = open(sys.argv[1])
instances = json.loads(f.read())
f.close()

# Assigning the project to be the .json script name,
#The .json script should never come with .json at the end.
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])
#Getting .json list of snapshot disks and assigning it to snap.json
with open('snap.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'snapshots', 'list', '--format', 'json' ] ,stdout=outfile)

#Other commands that we might use later:
# gcloud compute snapshots list --uri
# gcloud compute snapshots describe

# Assigning the snap.json file to "disks"
f = open('snap.json')
disks = json.loads(f.read())
f.close()

# Creating a snapshosts file
snapshots = open('snapshots', 'w+')



# It SHOULD take all the "name" rows from the instances file, (the one we supplied at the begining)
# IF the name, or part of the name present in the "disks" file, at the "name" row
# It should print the disk name row.

print("Snapshots")
for row in instances:
    iname = row['name']
    for row in disks:
        dname = row['name']
        if iname in dname:
            #py2 way: print >> snapshots, dname
            #py3 way: print(dname, file=snapshots)
            #unified way:
            snapshots.write('{}\n'.format(dname))

snapshots = open('snapshots', 'r')
print(snapshots.read())

#print(snapshots)

#dd = np.loadtxt(snapshots, delimiter='-',usecols=[3])
#dd = np.loadtxt(snapshots, delimiter='-')
dd = np.loadtxt('snapshots', delimiter='-',usecols=str([-1,-2,-3]))
#dd = np.genfromtxt('snapshots', delimiter='-',usecols=[-1],[-4])
print(dd)



#print(DATE)


'''
print("INSTANCES")
for row in instances:
    snapname = row['name']
    print(snapname)


print("DISKS")
for row in disks:
    sname = row['name']
    print(sname)

'''
