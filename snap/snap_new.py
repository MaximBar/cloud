from datetime import datetime
from time import gmtime, strftime
import os
import time
import datetime
import json
import subprocess
import sys
from sys import argv



subprocess.check_output("gcloud compute snapshots list --format json > snapshotlist.json", shell=True)
f = open('snapshotlist.json');
data = json.loads(f.read())

snap_date=subprocess.check_call(['/usr/bin/gcloud', 'compute', 'snapshots', 'list', '|', 'grep' snapname ])
