from datetime import datetime
from time import gmtime, strftime
import os
import time
import datetime
import json
import subprocess
import sys
from sys import argv


projectn = sys.argv[1]

zone = "europe-west1-b"
region = "europe-west1"
DATE = time.strftime('%d-%m-%Y')
sym = "-"

#data=subprocess.check_output("gcloud compute disks list --format json > diskslist.json", shell=True)
# script should be a .json script inside, but named after the project
print("Setting the project to be " + projectn)
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

f = open(sys.argv[1]);
data = json.loads(f.read())
f.close()

for row in data:
    #print row['name']
    #print row['zone']
    DISK_NAME=row['name']
    snappname = DISK_NAME + sym + DATE
    #print DISK_NAME
    zname=row['zone']
    os.system("gcloud compute disks snapshot"+ " " +DISK_NAME + " " +"--snapshot-names"+ " " +snappname+ " "  +"--zone"+" " +zname)

#Rotation_of_Disk
'''
DATE = time.strftime('%Y-%m-%d')

#data=subprocess.check_output("gcloud compute snapshots list --format json > snapshotlist.json", shell=True)
f = open(sys.argv[1]);
data = json.loads(f.read())
f.close()

subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

for row in data:
    snapname=row['name']
    #snap_date=subprocess.check_call(['gcloud', 'compute', 'snapshots', 'describe', snapname, '|', 'grep', "creationTimestamp", '|', 'cut -d', '" "', '-f 2', | tr -d \' | cut -f 1 -d T)"
    snap_date=subprocess.check_call(['gcloud', 'compute', 'snapshots', 'list', '|', 'grep' snapname ])
    #delsnap=row['creationTimestamp']
    #crtime=delsnap[:10]
#if crtime <= DATE :
#    print "true"
#    print row['name']
    #os.system("echo Y | gcloud compute snapshots delete"+ " " +snapname)
else:
    print "false"


else:
   print "please enter a valid choice 1 or 2"
'''
