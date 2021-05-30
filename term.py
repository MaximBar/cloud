import subprocess
import os
import sys
import json

projectn = "cloudnow-labs"
#instance = stackdriver-internalip-monitor
##log = subprocess.Popen('gcloud beta logging read "resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/cloudnow-labs/logs/compute.googleapis.com%2Factivity_log" | grep -e "timestamp" -e "compute.googleapis.com/resource_name"', shell=True)

#log2 = term_log = subprocess.Popen('gcloud beta logging read "resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/"projectn"/logs/compute.googleapis.com%2Factivity_log" | grep -e "timestamp" -e "name"', shell=True)

# u want subprocess.check_output(["gcloud", "beta", ..., "logName=projects/" + projectn + "/logs/compute.googleapis.com%2Factivity_log"]), and to not use grep, just use python.

#log3 = subprocess.check_output(['gcloud', 'beta', 'logging', 'read', 'resource.type=gce_instance', 'AND', 'jsonPayload.event_subtype=compute.instances.stop', 'AND', 'logName=projects/' + projectn + '/logs/compute.googleapis.com%2Factivity_log'])

#log4 = subprocess.check_output(['gcloud', 'beta', 'logging', 'read', 'resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/' + projectn + '/logs/compute.googleapis.com%2Factivity_log'])

# with open('foo', 'w') as fh: fh.write(subprocess.check_output('ls'))
# [16:12] <Wooble> MaximB: probably don't use check_output for that. Use .call() and give stdout=your_file_object
# [16:12] <cdunklau> MaximB: or provide the file as stdout
# with open('')
#  with open('term.json', 'wb') as outfile: subprocess.call(..., stdout=outfile)
with open('term.json', 'wb') as outfile: subprocess.call(['gcloud', 'beta', 'logging', 'read',
'resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/' + projectn + '/logs/compute.googleapis.com%2Factivity_log',
'--format', 'json'] ,stdout=outfile)
#term = subprocess.check_output(['gcloud', 'beta', 'logging', 'read', 'resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND logName=projects/' + projectn + '/logs/compute.googleapis.com%2Factivity_log', '--format', 'json'])
##print(log)

f = open('term.json')
data = json.loads(f.read())
f.close()
#print(data)
for row in data:
    #name = row['compute.googleapis.com/resource_name']
    sname = row['name']
    sdate = row['timestamp']
    print(sname + sdate)

# compute.googleapis.com/resource_name:
# timestamp:

stopped_instances1 = subprocess.check_output(['gcloud', 'compute', 'instances', 'list', '--filter=STATUS:TERMINATED']) # '--format json' ])
#print(stopped_instances1)
stopped_instances2 = subprocess.check_output(['gcloud', 'compute', 'instances', 'list', '--filter=STATUS:TERMINATED', '--format', 'json' ])
for i in stopped_instances2:
    name = i['name']
    status = i['status']
    print(name + status)

#print(stopped_instances2)

'''
for row in stopped_instances2:
    instance=row['name']
    stopped_date=['timestamp']
    print(instance + stopped_date)
'''
#print(stopped_instances2)

#print(log4)
