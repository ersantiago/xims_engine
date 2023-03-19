#!/usr/bin/python3
import time
import re
import os
import sys

scripts_db = '/mnt/share/scripts/admin_scripts/cfgadmin'

# Check if linux_engine is already running.
#chkrunning = os.popen('ps -e | grep linux_engine').read()
#print(chkrunning)
#if 'linux_engine' in chkrunning:
#    print('Linux engine already running.')
#    exit()
while True:
    loadscripts = open(scripts_db, 'r').read().splitlines()
    for script in loadscripts:
        if not script.startswith('#'):
            print('Running: ' + str(script))
            run_results = os.popen(script).read()
            print('Done.')
    time.sleep(30)
