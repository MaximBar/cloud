import os
import sys
import subprocess

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
region = zone[:-2]
#region = "us-east1"
#instance_tags: '{"Name":"{{ ec2_tag_Name }}","Type":"{{ ec2_tag_Type }}","WorkHoursOnly":"{{ ec2_tag_WorkHours }}","UserEmail":"{{ ec2_tag_UserEmail }}"}'

print("You selected: " + "\nImage: " + image + "\nTag: " + tag + "\nZone: " + zone + "\nMachine Type: " + machine + "\nSubnetwork: " + subnetwork)


print("\nSetting project to be TR-RND")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'tr-rnd'])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

#Single: tr-single-hagit-<machine name>
#Cluster: tr-cluster-min-hagit-<machine name>-node-1

# Vars:
# for cluster :
# prefix dev-cluster
# for single:
# prefix dev-single
# in cluster take node1,node2... as arg
# in cluster and single after creationn of the machine output the IP of the machine
# wait for ssh
# convention name for single:
# dev-thetaray-imagename
# convention name for cluster:
# dev-cluster-min-imagename-node-1/2/3...

#rand = make var to take from jenkins
# visual studio code
##rand = str(random.randint(10, 1000000)) no need
account = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).decode('utf-8').strip())
instance = "dev-thetaray" + str(image) + "-" + str(account) + "-" + rand
snap = str(image) + "-disk1"
#disk = str(snap) + "-" + str(account) + "-" + rand


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

# Output IP of the instance
with open('new_instance.txt', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'describe', instance ] ,stdout=outfile)
IP = subprocess.check_output("grep 'natIP' test.txt", shell=True)
print(IP).strip()[7:]
