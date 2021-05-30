import os
import sys
import subprocess
import json

# Syntax python script.py instance-name
instance = sys.argv[1]
zone = "us-east1-b"
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

f = open('instances_list.json')
instances_list = json.loads(f.read())
f.close()


found = False
for inst in instances_list:
    found = instance in inst['name']
    if found:
        print("Instance found")
        break
if not found:
    print("Instance NOT found!")
    sys.exit()

'''
# other ways to do it:

# one way - will fail if instance_list empty
for inst in instances_list:
    iname = inst['name']
    if instance in iname:
        print("Instance Found")
        break
if instance not in iname:
    print("Instance NOT found!")
    sys.exit()
'''

'''
if all(instance not in inst['name'] for inst in instances_list):
    print("Instance NOT found!")
    sys.exit()
'''


'''
for instance in instances:
    iname = instance['name']
    if instance_name in iname:
        print("Machine Already Exists!")
        sys.exit()
    else:
        continue
'''
# instance_json.get('tags', {'items': []}) gives you the value of the 'tags' key, or if that doesn't exist a dict with an 'items' key that is an empty list.
# it's not the same thing as instance_json['tags']['items'], which gets you the 'items' list of the dict that is the 'tags' key
# You just have to index the dict you get.
# instance_json.get('tags') is just like instance_json['tags'], except it does a different thing when the key doesn't exist.
# no, if there's no 'tags' key in the dict, you'll get that dict you pass as the second argument to instance_json.get,
# which does have an 'items' key. Can you show the problematic JSON, the code you run and the error you get?
# then the dict does have a 'tags' key, but the value of that doesn't have an 'items' item. Use instance_json['tags'].get('items', []) instead
# not json related, what you ahve is just a dict. The json module gives you regular dicts, lists, strings, integers, etc.
#instance = 'tr-cluster-min-maximb-grc-predix-new-node1'
stop_tag = 'do-not-stop'
del_tag = 'do-not-delete'


print("Checking Tags...")
with open('instance.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'describe', instance, '--format', 'json' ] ,stdout=outfile)


f = open('instance.json')
instance_json = json.loads(f.read())
f.close()

for i in instance_json:
    iname = instance_json['name']
    tags = instance_json['tags'].get('items', [])
    #tags = instance_json.get('tags', {'items': []})
    #tags = tags['items']
    #tags = instance_json.get('tags', 'items')
    #tags = instance_json['tags']['items']
print(tags)
if stop_tag not in tags:
    if del_tag not in tags:
        print("Deleting Instance " + instance + "...")
        #subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', instance])
else:
    print("Cannot Delete Instance, Tags " + str(tags) + " Found!"  )
