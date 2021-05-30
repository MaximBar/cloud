from datetime import datetime
from time import gmtime, strftime
import os
import time
import datetime
import json
import subprocess
import sys
from sys import argv


choice=sys.argv[1]
#automate_snapshot

if choice == '1':

                DATE = time.strftime('%d-%m-%Y')
                sym = "-"
                data=subprocess.check_output("gcloud compute disks list --format json > diskslist.json", shell=True)
                f = open('diskslist.json')
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

if choice == '2':


                DATE = time.strftime('%Y-%m-%d')

                data=subprocess.check_output("gcloud compute snapshots list --format json > snapshotlist.json", shell=True)
                f = open('snapshotlist.json');
                data = json.loads(f.read())
                f.close()
                for row in data:
                            snapname=row['name']
                            delsnap=row['creationTimestamp']
                            crtime=delsnap[:10]
                            if crtime <= DATE :
                                     print "true"
                                     print row['name']
                                     os.system("echo Y | gcloud compute snapshots delete"+ " " +snapname)
                            else:
                                    print "false"

else:
   print "please enter a valid choice 1 or 2"
