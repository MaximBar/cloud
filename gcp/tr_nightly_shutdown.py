# The Script was written by Maxim Bardin
# This script stops all google cloud platform instances that
# do not have the tag 'do-not-stop'

import datetime
import subprocess
import json


projectn = 'xxx'
zone = "us-east1-b"
region = zone[:-2]
tag = 'do-not-stop'

#today = "{:%m-%d-%Y-at-%H-%M-%S}".format(datetime.datetime.now()) # ex: 04-30-2017-at-15-03-02
today = "{:%B-%d-%Y-at-%H-%M-%S}".format(datetime.datetime.now()) # ex: May-30-2017-at-15-03-02
today = (today.lower())


print("\nSetting project to be XXX")
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

with open('instances_list.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)


with open('instances_list.json') as f: instances_list = json.load(f)

for instance in instances_list:
    iname = instance['name']
    status = instance['status']
    tags = instance['tags'].get('items', [])
    stop_tag = 'do-not-stop'
    stopped_on = "stopped-on-" + today
    check_stopped_tag = 'stopped-on'

    if stop_tag not in tags:
            if status == 'RUNNING':
                print(iname + " " + str(tags) + " " + status)
                print("Looking for stopped-on tag and removing it...")
                for x in tags:
                    if x.startswith("stopped-on"):
                        print(format(x))
                        x = str(format(x))
                        print("Removing Old 'stopped-on' Tag...")
                        subprocess.check_call(['gcloud', 'compute', 'instances', 'remove-tags', iname, '--tags', x])
                print("Adding 'stopped-on' Tag To " + iname + "...")
                subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', iname, '--tags', stopped_on])
                # Stopping the instance
                print("Stopping " + iname + "...")
                subprocess.check_call(['gcloud', 'compute', 'instances', 'stop', iname])
                print("\n")
