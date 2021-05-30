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
#automate_snapshot

DATE = time.strftime('%Y-%m-%d')

#data=subprocess.check_output("gcloud compute snapshots list --format json > snapshotlist.json", shell=True)
f = open(sys.argv[1])
instances = json.loads(f.read())
f.close()

subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])
#data_full = subprocess.check_output(['gcloud', 'compute', 'snapshots', 'list', '--format', 'json' ])
with open('snap.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'snapshots', 'list', '--format', 'json' ] ,stdout=outfile)

#data_full=subprocess.check_output("gcloud compute snapshots list --format json > snapshotlist.json", shell=True)

# gcloud compute snapshots list --uri
# gcloud compute snapshots describe
f = open('snap.json')
disks = json.loads(f.read())
f.close()
'''
for row in instances:
    snapname = row['name']
    print(snapname)
    if snapname in disks:
        #snapname = row['name']
        print(snapname)
'''
print("INSTANCES")
for row in instances:
    iname = row['name']
    for row in disks:
        dname = row['name']
        for iname in disks:
            print(iname)


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

    ##subprocess.check_output("gcloud compute snapshots list --format json > snapshotlist.json", shell=True)
    ##snap_date = subprocess.check_call(['gcloud', 'compute', 'snapshots', 'describe', snapname])
    #snap_date=subprocess.check_call(['/usr/bin/gcloud', 'compute', 'snapshots', 'describe', snapname, '|', 'grep', "creationTimestamp", '|', 'cut -d', '" "', '-f 2', | tr -d \' | cut -f 1 -d T)"
    #snap_list=
    ##snap_list=subprocess.check_call(['gcloud', 'compute', 'snapshots', 'list' ])
    ##print(snap_list.split('"')[0])
    #snap_date=subprocess.check_call(['/usr/bin/gcloud', 'compute', 'snapshots', 'list', '|', 'grep' snapname ])
    ##print(snap_date)
    #delsnap=row['creationTimestamp']
    #crtime=delsnap[:10]
#if crtime <= DATE :
#    print "true"
#    print row['name']
    #os.system("echo Y | gcloud compute snapshots delete"+ " " +snapname)
#else:
#    print "false"
