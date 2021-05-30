import sys
zone = sys.argv[1]
region = zone[:-2]
print(region)
#instance_tags: '{"Name":"{{ ec2_tag_Name }}","Type":"{{ ec2_tag_Type }}","WorkHoursOnly":"{{ ec2_tag_WorkHours }}","UserEmail":"{{ ec2_tag_UserEmail }}"}'

tag_name = "name: " + sys.argv[2]
tag_type = "type: " + sys.argv[3]
tag_work = "work-hours"
tag_mail =
