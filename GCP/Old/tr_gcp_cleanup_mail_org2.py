# The Script was written by Maxim Bardin from Cloudnow
# This script gets all Stopped intances,
# and if those instances do not have do-not-stop or do-not-delete tags
# Then it checks their stopped-on tag date and compares it with today
# if today is bigger than stopped-on  by x days, sends an email

import os
import sys
from datetime import timedelta, date, time, datetime
import subprocess
import json
import re
import smtplib
from email.mime.text import MIMEText

grace_period = sys.argv[1]
if not grace_period.isdigit():
    print("The parameter MUST be a digit!")
    sys.exit()

if int(grace_period) < int(3):
    print("The number must be higher than 2")
    sys.exit()


projectn = 'tr-rnd'
zone = "us-east1-b"
region = zone[:-2]
stopped_on = "{:%B-%d-%Y-at-%H-%M-%S}".format(datetime.now())
stopped_on_format = datetime.strptime(stopped_on, "%B-%d-%Y-at-%H-%M-%S")
del_tag = 'do-not-delete'
stop_tag = 'do-not-stop'

f = open('old_instances.txt', 'wb')
head_text = b"Hi, \n\
Please see attached the list of stopped instances on GCP that are going to be terminated in 2 days from now.\n\
If you still need any of these machine, please talk to Diana or Amit.\n\
\n\
Thank you,\n\
Infrastructure Team\n\
\n"

f.write(head_text)

print("Setting the project to be " + projectn)
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

with open('stopped.json', 'wb') as outfile1: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--filter=STATUS:TERMINATED', '--format', 'json' ] ,stdout=outfile1)
t = open('stopped.json')
stopped = json.loads(t.read())
t.close()


grace_period = int(grace_period)
grace_period = grace_period -2

print("grace_period is " + str(grace_period) + "  days")


print "Prepare mail with the list of all stopped instances that will be removed in 2 days"
#f = open('old_instances.txt','wb')

for instance in stopped:
    iname = instance['name']
    zone = instance['zone']
    status = instance['status']
    tags = instance['tags'].get('items', [])
    IP = str([i['networkIP'] for i in instance.get('networkInterfaces', [])])
    # Cleaning the IP string
    IP = IP.replace("u","")
    IP = IP.replace("[","")
    IP = IP.replace("]","")
    IP = IP.replace("'","")
    #print("Checking Tags...")
    if (stop_tag not in tags) and (del_tag not in tags):
        if "TERMINATED" in status:
            for x in tags:
                if x.startswith("stopped-on-"):
                    x = str(format(x))
                    x = x.replace("stopped-on-","")
                    x = datetime.strptime(x, "%B-%d-%Y-at-%H-%M-%S")
                    delta = datetime.now() - x
                    delta = str(delta)
                    delta_days = delta[0:4]
                    delta_days = re.sub("[^0-9]", "", delta_days)
                    print("delta " + delta_days)
                    if int(delta_days) < int(grace_period): #for testing only!!!
                    #if int(delta_days) > int(grace_period):
                        print(iname)
                        print(delta_days)
                        #f.write(iname + " (" + IP + ")\n")
                        f.write("{:<25}".format(str(iname)) + "\t" + "{:<5}".format(str( " (" + IP + ")\n")))

f.close()


username = 'jenkins@thetaray.com'
password="admin5555"

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)

print("Sending Email")
unrem = open("old_instances.txt", 'rb')
msg =  MIMEText(unrem.read())
msg['FROM'] = 'jenkins@thetaray.com'
msg['TO'] = 'maximb@cloudnow.co.il,amit.taller@thetaray.com'
msg['SUBJECT'] = "GCP instances that are going to be terminated in 2 days"


s = smtplib.SMTP('localhost')
#s.sendmail('jenkins@thetaray.com', ['maximb@cloudnow.co.il'], msg.as_string())
s.sendmail('jenkins@thetaray.com', ['maximb@cloudnow.co.il','amit.taller@thetaray.com'], msg.as_string())
s.quit()