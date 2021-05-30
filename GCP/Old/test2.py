import os
import sys
import subprocess


instance = "ansible-master"

with open('test.txt', 'wb') as outfile: subprocess.call(['gcloud', 'compute', 'instances', 'describe', instance ] ,stdout=outfile)
'''
f = open('test.txt')
server = json.loads(f.read())
f.close()

'''
#IP = subprocess.check_output("gcloud compute instances describe instance | grep natIP" ,shell=True).decode('utf-8').strip()
#IP2 = subprocess.check_call(['gcloud', 'compute', 'instances', 'describe', instance])
# hosts = subprocess.check_output("grep 'host:' /root/test.txt", shell=True)
IP = subprocess.check_output("grep 'natIP' test.txt", shell=True)
#IP3 = subprocess.check_output(IP2
print(IP).strip()[7:]
