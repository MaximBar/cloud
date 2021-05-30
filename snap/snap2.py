import subprocess
import time
import sys


# Usage: python script.py filename
# prints the supplied argument (file)
# print(sys.argv[0]) #this will print the name of the script
# print("Project name is " + sys.argv[1]) #prints name of the second argument


projectn = sys.argv[1]
current_date = time.strftime('%d-%m-%Y')
snap_type = "daily"
# szones = "europe-west1-b" #   zone name, change if needed
sym = "-"
print("Setting the project to be " + projectn)
subprocess.check_call(['/usr/bin/gcloud',
                       'config',
                       'set',
                       'project',
                       projectn])

with open(projectn, 'r') as f:
    for line in f.readlines():
        diskn = line.split()[0]
        p = subprocess.Popen(['/usr/bin/gcloud', 'compute', 'disks', 'list', diskn,
                              '|',
                              'tail -1',
                              '|',
                              'awk',
                              '{print $2}'],
                             stdout=subprocess.PIPE)
        nzones, _ = p.communicate()
        # Creating snapshots
        print(nzones)
        print("Creating snapshot for: {}".format(diskn))
        subprocess.check_call(['/usr/bin/gcloud',
                               'compute',
                               '--project',
                               projectn,
                               'disks',
                               'snapshot',
                               diskn,
        '--snapshot-names', '{}-{}-{}'.format(snap_type,
                                              diskn,
                                              current_date),
                               '--zone',
                               nzones])
