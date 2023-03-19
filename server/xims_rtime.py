#!/usr/bin/python3
import os, re
import ast

### GLOBAL VARIABLES & PATHS ###
nfs_cfglogin = '/mnt/share/scripts/configs/xims_cfgrtime'

# load login config
with open(nfs_cfglogin, 'r') as f:
    cfglogin = ast.literal_eval(f.read())

# for output file
cmdout = os.popen('ip a').read()
rgxmac = re.compile(r'link/ether\s(.*)?\sbrd')
maclst = rgxmac.findall(cmdout)[0].lower().split(':')
mac = ''.join([maclst[0],maclst[1],'.',maclst[2],maclst[3],'.',maclst[4],maclst[5]])

# writing new file
pcfile = os.path.join('/mnt/share/scripts/monitoring/workstations/', mac, 'rtime.info')
tmpfile = os.path.join('/mnt/share/scripts/monitoring/workstations/', mac, 'rtimetmp.info')
tmpfile_d = open(tmpfile, 'w')

# execute configs
for cfg in cfglogin:
    varname, cmdtype, cmd = cfg
    #print(varname)
    if cmdtype == 'unix':
        print(varname)
        print('  cmdtype : unix')
        cmdout = os.popen(cmd).read().strip()
    elif cmdtype == 'python':
        print(varname)
        print('  cmdtype : python')
        exec(cmd)
        try:
            cmdout = str(eval(varname))
        except:
            cmdout = 'Variable name not the same as used in command.'
    else:
        print(varname + '\tcmdtype : unknown')
        cmdout = 'Invalid command type (unix/python)'
    print('  cmdout  : ' + str(cmdout))
    results = [varname, cmdout]
    outprint = "".join(word.ljust(17) for word in results)
    #print(outprint)
    tmpfile_d.write(outprint + '\n')
tmpfile_d.close()
os.replace(tmpfile, pcfile)