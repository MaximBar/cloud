# The Script was written by Maxim Bardin
# This script checks all instances for tags 'do-not-stop' and 'do-not-delete'
# If at least one of the tags was found, it sends an email of the instance name + IP + State + Creation date
# Currently only works with Python 2.7

from datetime import timedelta, date, time, datetime
import subprocess
import json
import smtplib
import io
import re
from email.mime.text import MIMEText

projectn = 'xxx'
zone = "us-east1-b"
region = zone[:-2]
tag = 'do-not-stop'

today = "{:%Y-%m-%d}".format(datetime.now())

print("\nSetting project to be XXX")
subprocess.check_call(['gcloud', 'config', 'set', 'project', projectn])

print("Setting region to be " + region)
subprocess.check_call(['gcloud', 'config', 'set', 'compute/region', region])

print("Setting Zone to be " + zone )
subprocess.check_call(['gcloud', 'config', 'set', 'compute/zone', zone])

with open('instances_list.json', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'list', '--format', 'json' ] ,stdout=outfile)

with open('instances_list.json') as f: instances_list = json.load(f)



unrem = open('unrem.txt', 'wb')
head_text = b"Your instances are up for more than 5 days and can not be terminated automatically, please make sure to terminate it ASAP.\n\
If you still need it, please talk to Diana or Amit.\n\
\n\
The list of the instances:\n\
{:<48}".format("Name") + "\t" + "{:<25}".format("IP") + "\t" + "{:<15}".format("State") + "\t" + "{:<15}".format("Up Since")


unrem.write(head_text)

for instance in instances_list:
    iname = instance['name']
    status = instance['status']
    tags = instance['tags'].get('items', [])
    stop_tag = 'do-not-stop'
    delete_tag = 'do-not-delete'
    IP = str([i['networkIP'] for i in instance.get('networkInterfaces', [])])
    # Cleaning the IP string
    IP = IP.replace("u","")
    IP = IP.replace("[","")
    IP = IP.replace("]","")
    IP = IP.replace("'","")
    dt = instance['creationTimestamp']
    dt_small = dt.split('.')[0]
    date_string = dt.split('T')[0]
    t = dt.split('T')[1]
    time = t[:8]
    full_date_past_string = str(date_string + "-" + time)
    full_date_past = datetime.strptime(full_date_past_string, '%Y-%m-%d-%H:%M:%S')

    delta = datetime.now() - full_date_past
    delta = str(delta)
    days = delta[0:4]
    days = re.sub("[^0-9]", "", days) #anything other then digit, will be replaced with null
    print("delta: " + delta)
    print("days: " + days)

    if (stop_tag in tags) or (delete_tag in tags):
        if 5 < int(days):
                #if status == 'RUNNING':
                print("Name: " + iname + " Tags: " + str(tags) + " Internal IP: " + str(IP) + " Date: " + dt_small + " Status: " + status)
                text_org = ("\n" + "{:<35}".format(str(iname)) + "\t" + "{:<25}".format(str(IP)) + "\t" + "{:<15}".format(str(status)) + "\t" + "{:<15}".format(str(dt_small)) )
                text = text_org.replace('TERMINATED','Stopped')
                unrem.write(text)

unrem.close()

print("Sending Email")
# Mail server definitions
username = 'xxx@gmail.com'
password="xxx"
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)


unrem = open("unrem.txt", 'rb')
msg =  MIMEText(unrem.read())
# To/From/Subject/CC fields def
msg['FROM'] = 'xxx@gmail.com'
msg['TO'] = 'xxx@gmail.com'
msg['SUBJECT'] = "Your old 'unremovable' instances on GCP"


s = smtplib.SMTP('localhost')
#s.sendmail('jxxx@gmail.com', ['xxx@gmail.com'], msg.as_string())
# Syntax: ('from' , ['to1','to2'], msg.as_string())
s.sendmail('xxx@gmail.com', ['xxx@gmail.com'], msg.as_string())
s.quit()
unrem.close()
