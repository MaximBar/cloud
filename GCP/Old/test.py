import datetime
import subprocess
import json


projectn = 'tr-rnd'
zone = "us-east1-b"
region = zone[:-2]
tag = 'do-not-stop'

#today = "{:%m-%d-%Y-at-%H-%M-%S}".format(datetime.datetime.now()) # ex: 04-30-2017-at-15-03-02
today = "{:%B-%d-%Y-at-%H-%M-%S}".format(datetime.datetime.now()) # ex: May-30-2017-at-15-03-02
today = (today.lower())


print("\nSetting project to be TR-RND")
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
                print("Looking for stopped-on tag and removing it")
                for x in tags:
                    if x.startswith("stopped-on"):
                        print(format(x))
                        x = str(format(x))
                        print("Removing Old 'stopped-on' Tag")
                        print("Removing instance tag " + iname + " Tag: " + x)
                        #subprocess.check_call(['gcloud', 'compute', 'instances', 'remove-tags', iname, '--tags', x])
                print("Adding 'stopped-on' Tag To " + iname)
                print("Instance: " + iname + " Tag " + stopped_on)
                #subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', iname, '--tags', stopped_on])
                # Stopping the instance
                print("Stopping " + iname)
                #subprocess.check_call(['gcloud', 'compute', 'instances', 'stop', iname])
                print("\n")


'''
#zone = sys.argv[1]
#region = zone[:-2]
#print(region)

#instance_tags: '{"Name":"{{ ec2_tag_Name }}","Type":"{{ ec2_tag_Type }}","WorkHoursOnly":"{{ ec2_tag_WorkHours }}","UserEmail":"{{ ec2_tag_UserEmail }}"}'

tag_name = "name: " + sys.argv[2]
tag_type = "type: " + sys.argv[3]
tag_work = "work-hours"
tag_mail =


with open('new_instance.txt', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'describe', 'tr-single-maximb-thetaray-image-rhel-17-3-0-java' ]
 ,stdout=outfile)
IP = subprocess.check_output("grep 'natIP' new_instance.txt", shell=True)
#print(str(IP)).strip()[7:]
print((IP).strip()[7:])

IP = ((IP).strip()[7:])
with open('ip.txt', 'wb') as ipfile:
    ipfile.write(IP)



    "tags": {
      "fingerprint": "O-skakeqO3Y=",
      "items": [
        "ce-replicator"


            "networkInterfaces": [
      {
        "accessConfigs": [
          {
            "kind": "compute#accessConfig",
            "name": "External NAT",
            "natIP": "25.135.21.178",
            "type": "ONE_TO_ONE_NAT"
          }
        ],
        "kind": "compute#networkInterface",
        "name": "nic0",
        "network": "default",
        "networkIP": "12.112.0.6",

'''
