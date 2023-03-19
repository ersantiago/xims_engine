#!/usr/bin/python3
import time
import os

# Startup Runs
startup_run = '/home/.xims/scripts/linux_login.py'
startup_results = os.popen(startup_run).read()
print(startup_results)

# Realtime Runs
while True:
    rtime_run = '/home/.xims/scripts/linux_rtime.py'
    rtime_results = os.popen(rtime_run).read()
    print(rtime_results)
    time.sleep(15)
