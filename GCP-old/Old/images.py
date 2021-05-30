import os
import sys
import subprocess
import random

'''
1. images for boot disk
2. snapshot of second disk

script:
tag name
zone
image name
network name


create instance from image
check image for snapshots
if 2nd image, connect disk
'''


'''
check python ver:

import sys
python2 = sys.version_info[0] == 2
if python2:
    raw_input("Press ENTER to continue.")
else:
    input("Press ENTER to continue.")

'''


# instance = instance name (new)
# disk = disk name (new)
# snap = snapshot name


# Bash gcloud commands:
# gcloud compute instances create [EXAMPLE_INSTANCE] --image [IMAGE_NAME] #creating instance
# gcloud compute disks create [DISK_NAME] --source-snapshot [SNAPSHOT_NAME] #creating disk
# gcloud compute instances attach-disk [INSTANCE_NAME] --disk [DISK_NAME]
# gcloud compute instances add-tags NAME --tags=TAG,[TAG,...] [optional flags]
# gcloud compute instances add-tags example-instance --tags tag-1,tag-2
# gcloud config set compute/zone ZONE

# Add var for machine type

# python images.py two-disk-img-boot test europe-west1-b test1
print("Syntax is: python script.py image tag zone machine-type network ")
image = sys.argv[1]
tag = sys.argv[2]
zone = sys.argv[3]
machine = sys.argv[4]
network = sys.argv[5]

#print("You selected: ", image, tag, zone, network)
print("You selected: " + image + " " + tag + " " + zone + " " + " " + machine + " " + network)

python2 = sys.version_info[0] == 2
if python2:
    raw_input("\nPress ENTER to continue.")
else:
    input("\nPress ENTER to continue.")


print("Setting project to be cloudnow-labs")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'cloudnow-labs'])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])
#gcloud config set compute/zone

print("Creating Instance from image")



#account = str(os.system("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2") ,sys.exit(1))
#account = subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).strip()
#account = os.system("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2")
rand = str(random.randint(10, 1000000))
account = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).decode('utf-8').strip())
instance = str(image) + "-" + str(account) + "-" + rand
print(instance)
snap = str(image) + "-disk1"
disk = str(snap) + "-" + str(account) + "-" + rand

subprocess.check_call(['gcloud', 'compute', 'instances', 'create', instance, '--image', image, '--machine-type', machine, '--subnet', network])

# subprocess.check_call(['gcloud', 'compute', 'instances', 'create', instance, '--image', image])

print("Creating disk from snapshot")
subprocess.check_call(['gcloud', 'compute', 'disks', 'create', disk, '--source-snapshot', snap])

print("Attaching disk to instance")
subprocess.check_call(['gcloud', 'compute', 'instances', 'attach-disk', instance, '--disk', disk])

print("Adding tags to instance")
subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance, '--tags', tag])
