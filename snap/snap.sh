#!/bin/bash

PARAM_DIR=/root/SCRIPTS
DISK_LIST=`cat $PARAM_DIR/$1`
SNAPSHOT_TYPE=daily
SNAP_DATE=`date +"%d-%m-%y-%H%M"`
SNAP_PROJECT=`echo $1 | cut -d"." -f1`
SNAP_LOG=/tmp/snap_log_${SNAP_DATE}.txt
/usr/bin/gcloud config set project $SNAP_PROJECT
##### Creating new SNAPS #####
echo "Starting $SNAP_PROJECT disks snap" > $SNAP_LOG
for disk in $DISK_LIST
do
        echo "Creating $SNAPSHOT_TYPE snap for $disk" >> $SNAP_LOG
        SNAP_ZONE=`/usr/bin/gcloud compute disks list $disk | tail -1 | awk '{print $2}'`
        #echo "$disk $SNAP_ZONE"
        #echo $SNAP_PROJECT
        /usr/bin/gcloud compute --project "$SNAP_PROJECT" disks snapshot "$disk" --snapshot-names ${SNAPSHOT_TYPE}-${disk}-${SNAP_DATE} --zone ${SNAP_ZONE}
        if [ $? -eq 0 ]
        then
                echo "$disk snap ${SNAPSHOT_TYPE}-${disk}-${SNAP_DATE} created..." >> $SNAP_LOG
        else
                echo "There was a problem creating snap for $disk !!!" >> $SNAP_LOG
        fi
done

##### Delete old Snaps #####
SNAPSHOT_LIST="$(gcloud compute snapshots list --uri | grep daily)"
echo $SNAPSHOT_LIST >> $SNAP_LOG
# loop through the snapshots
echo "${SNAPSHOT_LIST}" | while read line ; do
      # get the snapshot name from full URL that google returns
      SNAPSHOT_NAME="${line}"
      echo $SNAPSHOT_NAME >> $SNAP_LOG
      # get the date that the snapshot was created
      SNAPSHOT_DATETIME="$(gcloud compute snapshots describe ${SNAPSHOT_NAME} | grep "creationTimestamp" | cut -d " " -f 2 | tr -d \' | cut -f 1 -d T)"
      echo $SNAPSHOT_DATETIME >> $SNAP_LOG
      # format the date
      SNAPSHOT_DATETIME="$(date -d ${SNAPSHOT_DATETIME} +%Y%m%d)"
      echo $SNAPSHOT_DATETIME >> $SNAP_LOG
      echo $SNAPSHOT_NAME >> $SNAP_LOG
      #CHECK IF DAILY SNAPSHOT - DELETE AFTER 7 DAYS
      if [[ $SNAPSHOT_NAME == *"daily-"* ]]
        then

         # get the expiry date for snapshot deletion (currently 3 days)
         SNAPSHOT_EXPIRY="$(date -d " -4 days" +"%Y%m%d")"
         echo $SNAPSHOT_EXPIRY >> $SNAP_LOG
         # check if the snapshot is older than expiry date
         if [ $SNAPSHOT_EXPIRY -ge $SNAPSHOT_DATETIME ];
           then
              # delete the snapshot
              gcloud compute snapshots delete ${SNAPSHOT_NAME} --quiet
         fi
      fi
done
