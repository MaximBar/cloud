import os
from datetime import datetime, timedelta
import smtplib

grace_period = 5
print "grace_period is " + str(grace_period) +"  days"

projectn = 'cloudnow-labs'
zone = "europe-west1-b"
region = zone[:-2]

print("Setting project to be cloudnow-labs")
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])


print("Get list of all instances older than " + str(grace_period) + " days and send mails to all users")
#all_instances = conn.get_only_instances(filters={'vpc_id':'vpc-d3a066b6'})
old_instances = {}

with open('instances.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)

f = open('instances.json')
all_instances = json.loads(f.read())
f.close()


for ainst in all_instances:
    usermail = "rnd@thetaray.com,CustomerSuccess@thetaray.com"
    if "UserEmail" in ainst.tags:
      usermail = ainst.tags['UserEmail']
    if usermail != "system" and usermail != "dev" and "Name" in ainst.tags:
        lt_datetime = datetime.strptime(ainst.launch_time, '%Y-%m-%dT%H:%M:%S.%fZ')
        lt_delta = datetime.utcnow() - lt_datetime
        if lt_datetime < datetime.utcnow() - timedelta(days = int(grace_period)):
            instance_details = {"name": ainst.tags['Name'], "ip":ainst.private_ip_address, "up_since":ainst.launch_time, "state":ainst.state, "api_term": ainst.get_attribute('disableApiTermination')['disableApiTermination']}
            if old_instances.has_key(usermail):
                old_instances[usermail].append(instance_details)
            else:
                old_instances[usermail] = [instance_details]


# mail details
FROM="jenkins@thetaray.com"
CC="diana.binny@thetaray.com"
SUBJECT="Your old 'unremovable' instances on AWS"
TEXT="Your instances are up for more than " + grace_period + " days and can not be terminated automatically, please make sure to terminate it ASAP. \nIf you still need it, please talk to Diana or Liya.\n\nThe list of the instances:\n"
username = 'jenkins@thetaray.com'
password="admin5555"

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
TEXT += "{:<40}".format("Name") + "\t" + "{:<15}".format("IP") + "\t" + "State" + "\t" + "Up Since" + "\n"

for user, instances_list in old_instances.iteritems():
    instances_list_sorted = sorted(instances_list, key=lambda k: (k['up_since'],k['name']))
    MESSAGE_TEXT = TEXT
    for i in instances_list_sorted:
        MESSAGE_TEXT += "{:<40}".format(i["name"]) + "\t" + i["ip"] + "\t" + i["state"] + "\t" + i["up_since"] + "\n"

    print "Send mail to " + user
    TO=user
    message = 'Subject: %s\n\n%s' % (SUBJECT, MESSAGE_TEXT)
    server.sendmail(FROM, [TO,CC], message)
