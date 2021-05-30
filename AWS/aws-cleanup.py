import boto.ec2
from datetime import datetime, timedelta
import os
import time

conn = boto.ec2.connect_to_region('us-west-2')
stopped_instances = conn.get_only_instances(filters={'vpc_id':'vpc-d3a066b6', 'instance-state-name':'stopped'})

grace_period = int(os.environ['GRACE_PERIOD'])
print "grace_period is " + str(grace_period) +"  days"

print "Terminate all stopped instances older than " + str(grace_period) +" days that are not 'DoNotTerminate'"
terminated_instances = []
for inst in stopped_instances:
    if 'StoppedOn' in inst.tags and inst.tags['StoppedOn'] != "":
        stopped_on = datetime.strptime( inst.tags['StoppedOn'], "%B %d, %Y at %H:%M:%S")
        st_delta = datetime.now() - stopped_on
        disableApiTermination = inst.get_attribute('disableApiTermination')['disableApiTermination']
        if stopped_on < datetime.utcnow() - timedelta(days = grace_period) and not disableApiTermination:
            print inst.tags['Name'] + " (" + inst.private_ip_address+ ")" + ":" + str(st_delta)
            print "Stopped for more than " + str(grace_period) + " days and will be terminated!"
            terminated_instances.append ({"name": inst.tags['Name'], "ip":inst.private_ip_address })
            inst.terminate()

terminated_instances_sorted = sorted(terminated_instances, key=lambda k: k['name'])

f = open('terminated_instances.txt','w')
for i in terminated_instances_sorted:
    f.write("{:<40}".format(i["name"]) + "\t" + i["ip"] + "\n")
f.close()

time.sleep(60)
print "Delete available volumes"
available_volumes = conn.get_all_volumes(filters={"status":"available"})
for volume in available_volumes:
  print volume.id
  conn.delete_volume(volume.id)
