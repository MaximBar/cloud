# The Script was written by Maxim Bardin from Cloudnow
# This script creates a google cloud platform instance using gcloud
import os
import sys
import subprocess
import json
import random
import string


print("Syntax is: python tr_create_cluster.py suffix image zone machine-size subnetwork 'do not stop(yes/no)' 'do not delete(yes/no)'")
print("Example: python tr_create_cluster.py min-maxim.bar-test-node-1 thetaray-image-ubuntu-17-3-0-java us-east1-b n1-standard-2 rnd-subnet yes no")
# Example2: python tr_create_cluster.py min-namesuffix-manager-1 grc-new2 us-east1-b n1-standard-2 rnd-subnet yes no

suffix_dot = sys.argv[1]
suffix = suffix_dot.replace('.','-')
image = sys.argv[2]
zone = sys.argv[3]
machine_size = sys.argv[4]
subnetwork = sys.argv[5]
do_not_stop_tag = sys.argv[6]
do_not_delete_tag = sys.argv[7]
region = zone[:-2]

if do_not_stop_tag != 'yes':
    if do_not_stop_tag != 'no':
        print("You must only type 'yes' or 'no' at the 'do_not_stop_tag' field!")
        sys.exit()

if do_not_delete_tag != 'yes':
    if do_not_delete_tag != 'no':
        print("You must only type 'yes' or 'no' at the 'do_not_delete_tag' field!")
        sys.exit()


print("You selected: " + "\nSuffix: " + suffix + "\nImage: " + image + "\nZone: " + zone + "\nMachine Size: " + machine_size
 + "\nSubnetwork: " + subnetwork
 + "\nDo Not Stop: " +  do_not_stop_tag + "\nDo Not Delete: " + do_not_delete_tag)

print("\nSetting project to be TR-RND...")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'tr-rnd'])

print("Setting region to be " + region + "...")
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone + "...")
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

s = "abcdefghijklmnopqrstuvwxyz0123456789"
rand = ''.join(random.choice(s) for i in range(8))
instance_name = "tr-cluster-" + str(suffix)
snap = str(image) + "-disk1"
disk = str(instance_name) + "-disk1-" + rand

print("Checking if machine already exists")
with open('instances_list.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)

with open('instances_list.json') as f: instances_list = json.load(f)

for instance in instances_list:
    iname = instance['name']
    if instance_name in iname:
        print("Machine Already Exists!")
        sys.exit()
    else:
        continue

print("Check passed successfully!")

print("Creating Instance from image...")
subprocess.check_call(['gcloud', 'compute', 'instances', 'create', instance_name, '--image', image, '--machine-type', machine_size, '--subnet', subnetwork])

print("Creating disk from snapshot...")
subprocess.check_call(['gcloud', 'compute', 'disks', 'create', disk, '--source-snapshot', snap])

print("Attaching disk to instance...")
subprocess.check_call(['gcloud', 'compute', 'instances', 'attach-disk', instance_name, '--disk', disk])

print("Setting disk to auto-delete...")
subprocess.check_call(['gcloud', 'compute', 'instances', 'set-disk-auto-delete', instance_name, '--disk', disk])


print("Adding Tags To Instance (if set)...")


if do_not_stop_tag == "yes":
    do_not_stop = "do-not-stop"
    print("Adding Do Not Stop Tag...")
    subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance_name, '--tags', do_not_stop])


if do_not_delete_tag == "yes":
    do_not_delete = "do-not-delete"
    print("Adding Do Not Delete Tag...")
    subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance_name, '--tags', do_not_delete])


with open('new_instance.txt', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'describe', instance_name ] ,stdout=outfile)
#IP = subprocess.check_output("grep 'natIP' new_instance.txt", shell=True)
IP = subprocess.check_output("grep 'networkIP' new_instance.txt", shell=True)
print("\nThe full name of the new instance is: " + instance_name  )
#print("The External IP of the new instance is: ")
print("The Internal IP of the new instance is: ")
#print((IP).strip()[7:])
print((IP).strip()[11:])
#IP = ((IP).strip()[7:])
IP = ((IP).strip()[11:])

with open('ip.txt', 'wb') as ipfile: ipfile.write(IP)

print("Instance created, script finished")
