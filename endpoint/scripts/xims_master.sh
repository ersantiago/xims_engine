#!/bin/bash
#================== Checking logged accounte =================#
hostname=`hostname`
user=`whoami`
if [ "$user" == "root" ] || [ "$hostname" == "nfs01" ] || [ "$user" == "emerson" ]
   then
   echo "Running on root account or NFS server. Global script not executed."
   exit
fi
#================== Initialize Settings ======================#
sed -i 's/MouseSendsControlV=True/MouseSendsControlV=False/g' /home/$USER/.ICAClient/wfclient.ini 2> /dev/null

#================= Commands to Run as Admin ==================#
# Hosts, VPN
/usr/bin/python3 /home/.xims/scripts/xims_sudep.pyc

#================== WFH Engine ===============================#
chkrunning=`ps -e | grep wfh_engine | wc -l`
if [ "$chkrunning" -ne 0 ]
   then
   echo "Linux_engine already running."
else
   /home/.xims/scripts/xims_engine.py &
fi
