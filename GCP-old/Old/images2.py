import os
import sys
import subprocess
import random
import json


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



# python images.py two-disk-img-boot test europe-west1-b test1
print("Syntax is: python3 script.py image tag zone network ")
image = sys.argv[1]
tag = sys.argv[2]
zone = sys.argv[3]
network = sys.argv[4]

#print("You selected: ", image, tag, zone, network)
print("You selected: " + image + " " + tag + " " + zone + " " + network)

'''
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
'''
#account = str(os.system("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2") ,sys.exit(1))
#account = os.system("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2") #,sys.exit(1)
# get the command output as json, parse the json with json.loads, and pick out the field you want
#  the gcloud info --format=json will give you a json document, you can json.loads that to get a python dict,
#extract the Account field, then use either a regex or other string manipulation to get the actual part of the account you need.
# json.loads(output.decode('utf-8'))

'''
python2 = sys.version_info[0] == 2
if python2:
    account = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).strip())
else:
    accountb = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).strip())
    account = account1b[1:]

'''
# subprocess.check_output(['gcloud', 'info'], universal_newlines=True), and then doing the grepping and cutting in Python instead.
# ac = subprocess.check_output(['gcloud', 'info'], universal_newlines=True)
account = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).decode('utf-8').strip())
#account = accountb[1:]
print(account)
#print(account)
##account1x = str(subprocess.check_output("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2" ,shell=True).strip())
#account1 = subprocess.check_output("sed 's/^.\{5\}//' |" account1x)
#account1 = subprocess.check_output(account1x '| awk '{print $2}'')
##account1 = account1x[1:]
##account2 = subprocess.Popen("gcloud info |grep Account | cut -d '@' -f 1 | cut -d'[' -f2", stdout=subprocess.PIPE, shell=True).stdout.read().strip()

'''
output = subprocess.check_output(['gcloud', 'info', '--format=json'])
#aname = json.loads(output.decode('utf-8'))
aname = json.loads(output)
print(aname)
#account_name = aname['account']
#print("Account: ", account_name)
'''
#print("Account1x: ", account1x)
#print("Account1: ", account1)
#print("Account2: ", account2)

'''
for row in structure:
    snapname = row['account']
    print(snapname)
'''
'''
rand = str(random.randint(10, 1000000))
instance = str(image) + "-" + str(account) + "-" + rand

snap = str(image) + "-disk1"
disk = str(snap) + "-" + str(account) + "-" + rand

print("Account: ",account_name)

#print("account: " ,account)
print("instance: " ,instance)
print("disk: " ,disk)

'''
'''
subprocess.check_call(['gcloud', 'compute', 'instances', 'create', instance, '--image', image, '--subnet', network])

# subprocess.check_call(['gcloud', 'compute', 'instances', 'create', instance, '--image', image])

print("Creating disk from snapshot")
subprocess.check_call(['gcloud', 'compute', 'disks', 'create', disk, '--source-snapshot', snap])

print("Attaching disk to instance")
subprocess.check_call(['gcloud', 'compute', 'instances', 'attach-disk', instance, '--disk', disk])

print("Adding tags to instance")
subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', instance, '--tags', tag])
'''
