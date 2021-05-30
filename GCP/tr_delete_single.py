# The Script was written by Maxim Bardin from Cloudnow
# This script deletes a single google cloud platform instance using gcloud,
# It checks if the instance does NOT have the tags 'do-not-stop' or 'do-not-delete' before deleting it


import os
import sys
import subprocess
import json

print("Syntax: tr_delete_single.py instance-name zone")

instance = sys.argv[1]
zone = sys.argv[2]
#zone = "us-east1-b"
region = zone[:-2]

stop_tag = 'do-not-stop'
del_tag = 'do-not-delete'

print("\nSetting project to be TR-RND")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'tr-rnd'])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

print("Checking if instance exists...")
with open('instances_list.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)

with open('instances_list.json') as f: instances_list = json.load(f)

found = False
for inst in instances_list:
    found = instance in inst['name']
    if found:
        print("Instance found")
        break
if not found:
    print("Instance NOT found!")
    sys.exit()


print("Checking Tags...")
with open('instance.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'describe', instance, '--format', 'json' ] ,stdout=outfile)


with open('instance.json') as f: instance_json = json.load(f)

for i in instance_json:
    iname = instance_json['name']
    tags = instance_json['tags'].get('items', [])


if (stop_tag not in tags) and (del_tag not in tags):
    print("Deleting Instance " + instance + "...")
    subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', instance]) #Deletes the instance!!!
else:
    print("Cannot Delete Instance, Tags " + str(tags) + " Found!"  )

'''
if stop_tag not in tags:
    if del_tag not in tags:
        print("Deleting Instance " + instance + "...")
        subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', instance])
else:
    print("Cannot Delete Instance, Tags " + str(tags) + " Found!"  )
'''
