import boto.ec2
import os
from datetime import datetime, timedelta

conn = boto.ec2.connect_to_region('us-west-2')
stopped_instances = conn.get_only_instances(filters={'vpc_id':'vpc-d3a066b6', 'instance-state-name':'stopped'})

grace_period = int(os.environ['GRACE_PERIOD']) - 2
# GRACE_PERIOD is set in the general Jenkins Configuration. Hard coded to value 5.

print "grace_period is " + str(grace_period) + "  days"

# checking when instance was terminated (if avialable in the logs)
# gcloud beta logging read "resource.type=gce_instance AND jsonPayload.event_subtype=compute.instances.stop AND \
# logName=projects/cloudnow-labs/logs/compute.googleapis.com%2Factivity_log" | grep -e 'name' -e 'timestamp'


print "Prepare mail with the list of all stopped instances that will be removed in 2 days"
f = open('old_instances.txt','w')
for inst in stopped_instances:
    print inst.tags['Name']
    if 'StoppedOn' in inst.tags and inst.tags['StoppedOn'] != "":
        stopped_on = datetime.strptime( inst.tags['StoppedOn'], "%B %d, %Y at %H:%M:%S")
        st_delta = datetime.now() - stopped_on
        disableApiTermination = inst.get_attribute('disableApiTermination')['disableApiTermination']
        if stopped_on < datetime.utcnow() - timedelta(days = grace_period) and not disableApiTermination:
            f.write(inst.tags['Name'] + " (" + inst.private_ip_address+ ")\n")

f.close()
