import os
import sys
import subprocess
import random

# The script accepts 5 vars, run:
# python instances.py image-name tag-name region machine-type subnetwork
# ex: python instances-rd.py grc-new2 testing us-east1-b n1-standard-2 rnd-subnet
print("Syntax is: python script.py image tag zone machine-type subnetwork ")
image = sys.argv[1]
tag = sys.argv[2]
# tags try implant it with array
zone = sys.argv[3]
machine = sys.argv[4]
subnetwork = sys.argv[5]
#zone = us-east1-b
# region = zone -2 letters
region = "us-east1"

print("You selected: " + "\nImage: " + image + "\nTag: " + tag + "\nZone: " + zone + "\nMachine Type: " + machine + "\nSubnetwork: " + subnetwork)


print("\nSetting project to be TR-RND")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'tr-rnd'])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])


# Vars:
# for cluster :
# prefix dev-cluster
# for single:
# prefix dev-single
# in cluster take node1,node2... as arg
# in cluster and single after creationn of the machine output the IP of the machine
# wait for ssh
#
#rand = make var to take from jenkins
# visual studio code
##rand = str(random.randint(10, 1000000)) no need
##account = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).decode('utf-8').strip())
##instance = str(image) + "-" + str(account) + "-" + rand
snap = str(image) + "-disk1"
disk = str(snap) + "-" + str(account) + "-" + rand


print("Creating Instance from image")
subprocess.check_call(['gcloud', 'compute', 'instances', 'create', instance, '--image', image, '--machine-type', machine, '--subnet', subnetwork])

print("Creating disk from snapshot")
subprocess.check_call(['gcloud', 'compute', 'disks', 'create', disk, '--source-snapshot', snap])

print("Attaching disk to instance")
subprocess.check_call(['gcloud', 'compute', 'instances', 'attach-disk', instance, '--disk', disk])

print("Setting disk to auto-delete")
subprocess.check_call(['gcloud', 'compute', 'instances', 'set-disk-auto-delete', instance, '--disk', disk])

print("Adding tags to instance")
subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance, '--tags', tag])
