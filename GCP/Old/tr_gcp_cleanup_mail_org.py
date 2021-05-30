import os
from datetime import timedelta, date, time, datetime
import subprocess
import json
import re
import smtplib
from email.mime.text import MIMEText

projectn = 'tr-rnd'
zone = "us-east1-b"
region = zone[:-2]
stopped_on = "{:%B-%d-%Y-at-%H-%M-%S}".format(datetime.now())
stopped_on_format = datetime.strptime(stopped_on, "%B-%d-%Y-at-%H-%M-%S")
check_stopped_tag = 'stopped-on'
del_tag = 'do-not-delete'
stop_tag = 'do-not-stop'


print("Setting the project to be " + projectn)
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

#stopped_instances = subprocess.check_call(['/usr/bin/gcloud', 'compute', 'instances', 'list', '--filter=STATUS:TERMINATED'])
#stopped_instances = subprocess.check_output("gcloud compute instances list --filter=STATUS:TERMINATED --format json > terminated.json", shell=True)

'''
"{:%m-%d-%Y-at-%H:%M:%S}".format(datetime.now())
'05-03-2017-at-11:56:21'

>>> print(datetime.now())
2017-05-03 11:56:36.758600

"timestamp": "2017-05-03T07:31:54.069506Z"
'''



with open('stopped.json', 'wb') as outfile1: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--filter=STATUS:TERMINATED', '--format', 'json' ] ,stdout=outfile1)
t = open('stopped.json')
stopped = json.loads(t.read())
t.close()

#stopped_instances2 = subprocess.check_output(['gcloud', 'compute', 'instances', 'list', '--filter=STATUS:TERMINATED', '--format json' ])
'''
with open('instances_log.json', 'wb') as outfile2: subprocess.call(['gcloud', 'beta', 'logging', 'read',
'resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/' + projectn + '/logs/compute.googleapis.com%2Factivity_log', '--format', 'json' ] ,stdout=outfile2)
i = open('instances_log.json')
instances_log= json.loads(i.read())
i.close()
'''

#term_log2 = subprocess.check_output(['gcloud', 'beta', 'logging', 'read',
#'resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/' + projectn + '/logs/compute.googleapis.com%2Factivity_log'])


#term_log = subprocess.Popen('gcloud beta logging read "resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/" + projectn + "/logs/compute.googleapis.com%2Factivity_log" | grep -e "timestamp" -e "name"', shell=True)
#term_log = subprocess.Popen('gcloud beta logging read "resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/cloudnow-labs/logs/compute.googleapis.com%2Factivity_log" | grep -e "timestamp" -e "name"', shell=True)

grace_period = 5
grace_period = grace_period -2
grace_period = int(grace_period)
print("grace_period is " + str(grace_period) + "  days")

# log oldest 2017-04-23
# log lates
#if term['name'] == instances_log['name']:
    #for i in instances_log:
#    print(instances_log['name'])
#    print term['name']

# stopped-on-04-30-2017-at-15-25-13
# 2017-04-30T06:21:33.031089Z


# you need to actually deserialize json data in a variable:
#data = json.loads(json_string); then you can do `name = data[0]['jsonPayload']['resource']['name']`
# `i['jsonPayload']['resource']['name']` instead of `i['resource']['name']`


'''
print("Testing2")
for i in instances_log:
    name = i['jsonPayload']['resource']['name']
    nid =  i['jsonPayload']['resource']['id']
'''

#f = open('instances_log.json')
#f = open('terminated.json')
#instances = json.loads(f.read())
#f.close()


'''
>>> before = "{:%B-%d-%Y-at-%H-%M-%S}".format(datetime.now())
>>> before = (before.lower())
>>> before2 = datetime.strptime( before, "%B-%d-%Y-at-%H-%M-%S")
>>> print(now - before2)
'''


print "Prepare mail with the list of all stopped instances that will be removed in 2 days"
f = open('old_instances.txt','wb')

#print("\nStopped")
for instance in stopped:
    iname = instance['name']
    #iname = instance['resource']['name']
    ##print(iname)
    zone = instance['zone']
    #print(zone)
    status = instance['status']
    #tags = instance['tags']['items']
    tags = instance['tags'].get('items', [])
    IP = str([i['networkIP'] for i in instance.get('networkInterfaces', [])])
    # Cleaning the IP string
    IP = IP.replace("u","")
    IP = IP.replace("[","")
    IP = IP.replace("]","")
    IP = IP.replace("'","")
    #print( iname + " " + status + " " + tags)
    ##print(tags)
    stop_tag = 'do-not-stop'
    #stopped_on = "stopped-on-" + today
    check_stopped_tag = 'stopped-on'
    del_tag = 'do-not-delete'
    #print("Checking Tags...")
    if (stop_tag not in tags) and (del_tag not in tags):
        for x in tags:
            if x.startswith("stopped-on"):
                #print(format(x))
                x = str(format(x))
                x = x.replace("stopped-on-","")
                x = datetime.strptime(x, "%B-%d-%Y-at-%H-%M-%S")
                delta = datetime.now() - x
                delta = str(delta)
                delta_days = delta[0:4]
                delta_days = re.sub("[^0-9]", "", delta_days)
                #delta_days = int(delta_days)
                #print(iname)
                #print(delta)
                print("delta " + delta_days)
                if int(grace_period) > int(delta_days):
                    print(iname)
                    print(delta_days)
                    #f.write(inst.tags['Name'] + " (" + inst.private_ip_address+ ")\n")
                    f.write(iname + " " + IP + "\n")

f.close()


username = 'jenkins@thetaray.com'
password="admin5555"

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)

#fromaddr = 'mb2love@gmail.com'
#toaddr = ['maximb@cloudnow.co.il']
print("Sending Email")
unrem = open("old_instances.txt", 'rb')
msg =  MIMEText(unrem.read())
msg['FROM'] = 'jenkins@thetaray.com'
msg['TO'] = 'maximb@cloudnow.co.il,amit.taller@thetaray.com'
msg['SUBJECT'] = "Instances to Delete in 2 days!"


s = smtplib.SMTP('localhost')
s.sendmail('jenkins@thetaray.com', ['maximb@cloudnow.co.il'], msg.as_string())
#s.sendmail('jenkins@thetaray.com', ['maximb@cloudnow.co.il','amit.taller@thetaray.com'], msg.as_string())
s.quit()

            #if status == 'RUNNING':
            #print(iname)
            #print(tags)
            #print(status)
            #stopped_on = datetime.strptime( inst.tags['StoppedOn'], "%B %d, %Y at %H:%M:%S")

            #print(iname + " " + tags + " " + status)





'''
print("\nStopped-2")
for i in stopped:
    stopped_srv = i['name']
    #print(term_srv)
    #print("\nInstances_log")
    #if term_srv in instances_log:
    for i in instances_log:
        #name = instances_log['resource']['name']
        name = i['jsonPayload']['resource']['name']
        print(name)
        # 2017-04-30T06:21:33.031089Z
        dt = i['timestamp']
        date = dt.split('T')[0]
        t = dt.split('T')[1] #8
        t2 = t[:8]
        ##time = t2.replace(":","-")
        #t3 = t1[:10]
        #time = t2[:19]
        #status = instances_log['status']
        #stopped_on = instances_log['timestamp']
        #print(time[:-17])
        #print(name)
        print(date + " " + t2)
        ##print(date+"-"+time)
        #print(time)
        #print(time[:10])
        #print(str(name) + " " + str(stopped_on))

        #print(name)
'''

'''
print("\nTerminated")
for i in term:
    name = i['name']
    print(name)
'''
'''
for instance in instances:
    iname = instance['name']
    status = instance['status']
    tags = instance['tags']['items']
    tag = 'work-hours-only-yes'
    stopped_on = "stopped-on-" + today

    if tag in tags:
        if status == 'RUNNING':
            print(iname + " " + tag + " " + status)
            subprocess.check_call(['gcloud', 'compute', 'instances', 'add-tags', iname, '--tags', stopped_on])

'''

'''
# GRACE_PERIOD is set in the general Jenkins Configuration. Hard coded to value 5.
'''
#for inst in stopped_instances2:
#    print()


'''
print("Prepare mail with the list of all stopped instances that will be removed in 2 days")
f = open('old_instances.txt','w')
for inst in stopped_instances:
    print inst.tags['Name']


'''
'''
    if 'StoppedOn' in inst.tags and inst.tags['StoppedOn'] != "":
        stopped_on = datetime.strptime( inst.tags['StoppedOn'], "%B %d, %Y at %H:%M:%S")
        st_delta = datetime.now() - stopped_on
        disableApiTermination = inst.get_attribute('disableApiTermination')['disableApiTermination']
        if stopped_on < datetime.utcnow() - timedelta(days = grace_period) and not disableApiTermination:
            f.write(inst.tags['Name'] + " (" + inst.private_ip_address+ ")\n")

f.close()
'''

#stopped_instances = gcloud compute instances list --filter='STATUS:TERMINATED'
# gcloud compute instances list
#projectn = sys.argv[1]
#automate_snapshot
#DATE = time.strftime('%d-%m-%Y')
#sym = "-"
#data=subprocess.check_output("gcloud compute disks list --format json > diskslist.json", shell=True)
