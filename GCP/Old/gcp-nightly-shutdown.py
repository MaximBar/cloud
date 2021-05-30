import datetime
import subprocess
import json


# 'do-not-terminate' for deletion,
# 'do-not-stop' for stop

projectn = 'cloudnow-labs'
zone = "europe-west1-b"
region = zone[:-2]
tag = 'work-hours-only-yes'

today = "{:%m-%d-%Y-at-%H-%M-%S}".format(datetime.datetime.now()) # ex: 04-30-2017-at-15-03-02

print(today)

print("Setting project to be cloudnow-labs")
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

with open('instances.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)

f = open('instances.json')
instances = json.loads(f.read())
f.close()

for instance in instances:
    iname = instance['name']
    #print(iname)
    #zone = instance['zone']
    #print(zone)
    status = instance['status']
    tags = instance['tags']['items']
    work_tag = 'work-hours-only-yes'
    stop_tag = 'do-not-stop'
    stopped_on = "stopped-on-" + today
    check_stopped_tag = 'stopped-on'

    if stop_tag not in tags:
            if work_tag in tags:
                if status == 'RUNNING':
                    print(iname + " " + work_tag + " " + status)
                    # Looking for stopped-on tag and removing it
                    for x in tags:
                        if x.startswith("stopped-on"):
                            print(format(x))
                            x = str(format(x))
                            subprocess.check_call(['gcloud', 'compute', 'instances', 'remove-tags', iname, '--tags', x])
                    # Stopping the instance
                    print("Stopping " + iname)
                    subprocess.check_call(['gcloud', 'compute', 'instances', 'stop', iname,])
                    # Adding Stopped On Tag
                    print("Adding Stopped On Tag To " + iname)
                    subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', iname, '--tags', stopped_on])


                    #for check_stopped_tag in str(tags):
                #        x = tags
            #            print("Found " + str(x))
                        #
                    #if check_stopped_tag not in str(tags):
                        #print("Stopped Tag WAS NOT found")
                        #subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', iname, '--tags', stopped_on])
                    #else:
                #        print("Tag Not Found")

                        #print("Stopped Tag Found!")




    '''
    subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])
    with open('desc.json', 'w+') as outfile2: subprocess.call(['gcloud', 'compute', 'instances', 'describe', iname, '--format', 'json' ],stdout=outfile2)
    out2 = open('desc.json')
    desc = json.loads(out2.read())
    out2.close()

    if tag in desc:
        print(tag)
'''
    #desc = subprocess.check_output(['gcloud', 'compute', 'instances', 'describe', iname, '--format', 'json' ])
    #if 'working-hours-only' in desc:
    #    print 'working-hours-only'
    #print(desc)

'''
    for iname in desc:
        work = iname['working-hours-only']
        print(work)
'''

'''
for inst in instances:
  print inst.id + "(" + inst.private_ip_address + ")"
  ec2conn.stop_instances(inst.id)
  ec2conn.create_tags([inst.id], {"StoppedOn": today})
'''
