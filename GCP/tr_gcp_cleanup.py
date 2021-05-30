# The Script was written by Maxim Bardin from Cloudnow
# This script gets all Stopped intances,
# and if those instances do not have do-not-stop or do-not-delete tags
# Then it checks their stopped-on tag date and compares it with today
# if today is bigger than stopped-on  by x days, deletes the instance
# Currently only works with Python 2.7

#Imports
import os
import sys
from datetime import timedelta, date, time, datetime
import subprocess
import json
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.message import MIMEMessage
from email.mime.multipart import MIMEMultipart

print("Checking if supplied argument is a digit...")
grace_period = sys.argv[1]
if not grace_period.isdigit():
    print("The parameter MUST be a digit!")
    sys.exit()


projectn = 'tr-rnd'
zone = "us-east1-b"
region = zone[:-2]
stopped_on = "{:%B-%d-%Y-at-%H-%M-%S}".format(datetime.now())
stopped_on_format = datetime.strptime(stopped_on, "%B-%d-%Y-at-%H-%M-%S")

del_tag = 'do-not-delete'
stop_tag = 'do-not-stop'

# The content of the email
f = open('deleted_instances_head.txt', 'wb')
head_text = b"Hi, \n\
Please see attached the list of terminated instances on GCP.\n\
\n\
Thank you,\n\
Infrastructure Team.\n\
\n"

f.write(head_text)
f.close()


print("Setting the project to be " + projectn)
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

# Getting all Stopped instances and putting them into stopped.json file
with open('stopped.json', 'wb') as outfile1: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--filter=STATUS:TERMINATED', '--format', 'json' ] ,stdout=outfile1)
t = open('stopped.json')
stopped = json.loads(t.read())
t.close()



grace_period = int(grace_period)
print("grace_period is " + str(grace_period) + "  days")

print("Terminate all stopped instances older than " + str(grace_period) +" days that are not 'do-not-stop' nor 'do-not-delete'")

f = open('deleted_instances.txt','wb')

# Will only delete instances IF they are TERMINATED/stopped and have the "stopped-on-<date>" tag,
# The stopped-on date must be within the grace period limit
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
                    #print(format(x))
                    x = str(format(x))
                    x = x.replace("stopped-on-","")
                    x = datetime.strptime(x, "%B-%d-%Y-at-%H-%M-%S")
                    delta = datetime.now() - x
                    delta = str(delta)
                    delta_days = delta[0:4]
                    delta_days = re.sub("[^0-9]", "", delta_days) #anything other then digit, will be replaced with null
                    print("delta " + delta_days)
                    #if int(delta_days) < int(grace_period): #for testing only!!!
                    if int(delta_days) > int(grace_period):
                        #print(iname)
                        #print(delta_days)
                        #f.write(iname + " " + IP + "\n")
                        f.write("{:<25}".format(str(iname)) + "\t" + "{:<5}".format(str(IP) + "\n"))
                        print("Deleting " + iname + "...")
                        subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', iname]) #Deletes the instance!!!

f.close()

# Mail server definitions
print("Sending Email")
username = 'jenkins@thetaray.com'
password="admin5555"
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
# Sending a multi part email
msg = MIMEMultipart()
head = open("deleted_instances_head.txt", 'rb')
deleted = open("deleted_instances.txt", 'rb')
content = MIMEText(head.read())
attachment = MIMEText(deleted.read())
# Adding the "deleted_instances.txt" mail as attachment
attachment.add_header('Content-Disposition', 'attachment', filename="deleted_instances.txt")
# Adding both files to the email
msg.attach(content)
msg.attach(attachment)
# To/From/Subject/CC fields def
msg['FROM'] = 'jenkins@thetaray.com'
msg['TO'] = 'amit.taller@thetaray.com'
msg['SUBJECT'] = "Jenkins GCP-cleanup"


s = smtplib.SMTP('localhost')
s.sendmail('jenkins@thetaray.com', ['maximb@cloudnow.co.il'], msg.as_string())
# Syntax: ('from' , ['to1','to2'], msg.as_string())
#s.sendmail('jenkins@thetaray.com', ['maximb@cloudnow.co.il','amit.taller@thetaray.com'], msg.as_string())

s.quit()
head.close()
deleted.close()
