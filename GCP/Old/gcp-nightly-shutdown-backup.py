import datetime
import subprocess
import json

zone = "europe-west1-b"
region = "europe-west1"
tag = 'work-hours-only-yes'
# {u'items': [u'testtag4', u'work-hours-only'], u'fingerprint': u'3pArz8AVWVY='}
#tag = "u'work-hours-only'"
today = "{:%B %d %Y at %H:%M:%S}".format(datetime.datetime.now())

print(today)

print("Setting project to be cloudnow-labs")
subprocess.check_call(['gcloud', 'config', 'set', 'project', 'cloudnow-labs'])

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
    tags = instance['tags']['items']
    #tags = instance['tags']['items']
    #print(tags)
    #tags = json.entry.get("tags", {}).json.get("items")
    #print(str(iname) + " " + str(tags))
    tag = 'work-hours-only-yes'
    #dic = tags['items']
    #tag = {u'items': [u'work-hours-only-yes']}
    #tag = {'items': 'work-hours-only-yes'}
    #tag = tags['items']
    #print(type(tags))
    #print(tags)
    if tag in tags:
    #    if tag in tags:
        print(iname + " " + tag)

    #if tag in tags:
    #    print(tag)
    #zone = instance['zone']
    #if tag in instances:
    #    print tag
    #for tag in tags:
    #    print tag
    #any(x == 'work-hours-only' for x in tags)
    #if tag in tags:
    #   print(tags)
    #print(type(tags.keys))
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
