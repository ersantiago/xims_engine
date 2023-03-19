#!/usr/bin/python3
import time
import os

# Patch Engine Runs
while True:
    patch_run = '/home/.xims/scripts/patch_rtime.py'
    patch_results = os.popen(patch_run).read()
    print(patch_results)
    time.sleep(30)
