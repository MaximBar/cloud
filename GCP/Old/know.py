# This:
if (stop_tag not in tags) or (del_tag not in tags):
    print("Deleting Instance " + instance + "...")
    subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', instance])
else:
    print("Cannot Delete Instance, Tags " + str(tags) + " Found!"  )

 

# is the same as this:

if stop_tag not in tags:
        print("Deleting Instance " + instance + "...")
        subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', instance])
elif del_tag not in tags:
        print("Deleting Instance " + instance + "...")
        subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', instance])
else:
    print("Cannot Delete Instance, Tags " + str(tags) + " Found!"  )
 
 
# NOT The same as this:
if stop_tag not in tags:
    if del_tag not in tags:
        print("Deleting Instance " + instance + "...")
        subprocess.check_call(['gcloud', '--quiet', 'compute', 'instances', 'delete', instance])
else:
    print("Cannot Delete Instance, Tags " + str(tags) + " Found!"  )


# but this one behaves differently
# it will check stop and delete tags regardless if stop tag is true
if (stop_tag in tags) or (delete_tag in tags):



