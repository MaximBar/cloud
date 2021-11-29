# The Script was written by Maxim Bardin
# This script deletes a single or several google cloud platform instances using gcloud,
# It looks inside a list of instances for part of the name,
# If found It checks if the instance does NOT have the tags 'do-not-stop' or 'do-not-delete' before deleting it


import os
import sys
import subprocess
import json



print("Syntax: python script.py instance-name without '-node-x'/'-manager-x' suffix + zone")
print("Example: python tr_delete_cluster.py   cluster-min-maximb-grc-predix-new us-east1-b")
inst = sys.argv[1]
zone = sys.argv[2]
#zone = "us-east1-b"
region = zone[:-2]

stop_tag = 'do-not-stop'
del_tag = 'do-not-delete'


print("\nSetting project to be XXX...")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'xxx'])

print("Setting region to be " + region + "...")
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone + "...")
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

print("Checking if instances exist...")
with open('instances_list.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)

with open('instances_list.json') as f: instances_list = json.load(f)

print("Checking Tags...")
for instance in instances_list:
    iname = instance['name']
    tags = instance['tags'].get('items', [])
    if inst in iname:
        if (stop_tag not in tags) and (del_tag not in tags):
            print("Deleting instance " + iname)
            subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', iname]) #Deletes the instance!!!
        else:
            print("Cannot Delete Instance " + iname + " Tags " + str(tags) + " Found!")

'''


print("Checking Tags...")
for instance in instances_list:
    iname = instance['name']
    tags = instance['tags'].get('items', [])
    if inst in iname:
        #if (stop_tag not in tags) or (del_tag not in tags):
        if stop_tag not in tags:
            if del_tag not in tags:
                print("Deleting instance " + iname)
                #subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', iname])
        else:
            print("Cannot Delete Instance " + iname + " Tags " + str(tags) + " Found!"  )



'''
