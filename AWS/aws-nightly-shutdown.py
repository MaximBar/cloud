import boto.ec2
import datetime

ec2conn = boto.ec2.connect_to_region('us-west-2')
instances = ec2conn.get_only_instances(filters={'vpc_id':'vpc-d3a066b6', 'tag:WorkHoursOnly':'Yes','instance-state-name':'running'})
today="{:%B %d, %Y at %H:%M:%S}".format(datetime.datetime.now())
for inst in instances:
  print inst.id + "(" + inst.private_ip_address + ")"
  ec2conn.stop_instances(inst.id)
  ec2conn.create_tags([inst.id], {"StoppedOn": today})
