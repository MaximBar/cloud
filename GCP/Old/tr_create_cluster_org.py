import os
import sys
import subprocess
import json
import random
import string
import time


'''
Single: tr-single-<user name>-<machine name> (e.g. tr-single-hagit-zamir-myinstance)
Cluster: tr-cluster-<deploy type>-<username>-<machine-name>-<node number> (e.g tr-cluster-min-hagit-zamir-myinstance-node1)
'''

print("Syntax is: python tr_create_cluster.py image zone machine-size subnetwork 'do not stop(yes/no)' 'do not delete(yes/no)' machine-type node-number(1-9)")
print("Example: python tr_create_cluster.py grc-new2 us-east1-b n1-standard-2 rnd-subnet yes no cluster 1")

image = sys.argv[1]
zone = sys.argv[2]
machine_size = sys.argv[3]
subnetwork = sys.argv[4]
do_not_stop_tag = sys.argv[5]
do_not_delete_tag = sys.argv[6]
machine_type = sys.argv[7]
deploy_type = sys.argv[8]
node = sys.argv[9]
#zone = us-east1-b
region = zone[:-2]
#region = "us-east1"

if machine_type == 'single':
    print("You must type 'Cluster' at the 'machine_type' field, for 'Single', use the 'create_single' script")
    sys.exit()

if do_not_stop_tag != 'yes':
    if do_not_stop_tag != 'no':
        print("You must only type 'yes' or 'no' at the 'do_not_stop_tag' field ")
        sys.exit()

if do_not_delete_tag != 'yes':
    if do_not_delete_tag != 'no':
        print("You must only type 'yes' or 'no' at the 'do_not_delete_tag' field ")
        sys.exit()

if node.isdigit():
    pass
else:
    print("The node field must be a digit")
    sys.exit()


print("You selected: " + "\nImage: " + image + "\nZone: " + zone + "\nMachine Size: " + machine_size
 + "\nSubnetwork: " + subnetwork
 + "\nDo Not Stop: " +  do_not_stop_tag + "\nDo Not Delete: " + do_not_delete_tag + "\nMachine Type: " + machine_type
 + "\nNode: " + node)

print("\nSetting project to be TR-RND")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'tr-rnd'])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

s = string.lowercase+string.digits
rand = ''.join(random.sample(s,8))
account_dot = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).decode('utf-8').strip())
account = account_dot.replace('.','-')
instance_name = "tr-cluster-" + deploy_type + "-" + str(account) + "-" + str(image) + "-" + "node" + str(node)
# instance_name = "tr-cluster-" + str(size) + "-" + str(account) + "-" + str(image) + "-node-" + node
snap = str(image) + "-disk1"
disk = str(snap) + "-" + str(account) + "-" + rand


print("Checking if machine already exists")
with open('instances.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)

f = open('instances.json')
instances = json.loads(f.read())
f.close()

for instance in instances:
    iname = instance['name']
    if instance_name in iname:
        print("Machine Already Exists!")
        sys.exit()
    else:
        continue

print("Check passed successfully")

print("Creating Instance from image")
subprocess.check_call(['gcloud', 'compute', 'instances', 'create', instance_name, '--image', image, '--machine-type', machine_size, '--subnet', subnetwork])

print("Creating disk from snapshot")
subprocess.check_call(['gcloud', 'compute', 'disks', 'create', disk, '--source-snapshot', snap])

print("Attaching disk to instance")
subprocess.check_call(['gcloud', 'compute', 'instances', 'attach-disk', instance_name, '--disk', disk])

print("Setting disk to auto-delete")
subprocess.check_call(['gcloud', 'compute', 'instances', 'set-disk-auto-delete', instance_name, '--disk', disk])


print("Adding tags to instance")

print("Adding Do Not Stop tag")
if do_not_stop_tag == "no":
    do_not_stop = "do-not-stop-no"
    subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance_name, '--tags', do_not_stop])
if do_not_stop_tag == "yes":
    do_not_stop = "do-not-stop-yes"
    subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance_name, '--tags', do_not_stop])

print("Adding Do Not Delete tag")
if do_not_delete_tag == "no":
    do_not_delete = "do-not-delete-no"
    subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance_name, '--tags', do_not_delete])
if do_not_delete_tag == "yes":
    do_not_delete = "do-not-delete-yes"
    subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance_name, '--tags', do_not_delete])


# Output IP of the instance
#print("Waiting for the instance to be created")
#time.sleep(10)
with open('new_instance.txt', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'describe', instance_name ] ,stdout=outfile)
IP = subprocess.check_output("grep 'natIP' new_instance.txt", shell=True)
print("\nThe full name of the new instance is: " + instance_name  )
print("The External IP of the new instance is: ")
print(IP).strip()[7:]
print("Instance created, script finished")
