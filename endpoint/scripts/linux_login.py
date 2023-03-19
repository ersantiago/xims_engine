#!/usr/bin/python3
import re
import os
import ast

print('Get Config from abc.com/infra')
try:
    cfglinux = ast.literal_eval(os.popen('curl http://172.16.41.17/infra/configs/xims_linux.cfg').read())
except:
    cfglinux = ast.literal_eval(os.popen('curl http://abc.com/infra/xims_linux.cfg').read())

cfgrtime = []
for config in cfglinux:
    status = config[1]
    schedule = config[2]
    if schedule == 'login' and status == 'active':
        cfgrtime.append(config)
test1 = 'xxxxxxxxxxxxxxxxxxxxxx'
dpw = bytes.fromhex(test1).decode('utf-8')

### Get mac address
cmdout = os.popen('ip a').read()

# regexes
rgxip = re.compile(r'inet\s+(172.*)?/')
rgxmac = re.compile(r'link/ether\s(.*)?\sbrd')

# get data
maclst = rgxmac.findall(cmdout)[0].lower().split(':')
mac = ''.join([maclst[0],maclst[1],'.',maclst[2],maclst[3],'.',maclst[4],maclst[5]])
print(mac)

results = []
results.append(['Variable', 'Result'])

for i in range(len(cfgrtime)):
    varname, status, sched, cmdtype, cmd = cfgrtime[i]
    if sched == 'login':
        try:
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
        except:
            cmdout = 'Runtime error'
        print('  cmdout  : ' + str(cmdout))
        result = [varname, cmdout]
        results.append(result)
    else:
        result = [varname, 'sched_err']
        results.append(result)
print('Done results')
print(str(results))
res_dict ={}
for result in results:
    rkey, rval = result
    res_dict[rkey] = rval
print(res_dict)

#====================== Transfer via FTP =========================#
ftfile = mac.replace('.','_') + '_login.info'
print('Creating temp directory and files...')
tempf = os.path.join('/home/.xims/tmp', ftfile)
tempfb = os.path.basename(tempf)
print(tempf)
tempwr = open(tempf, 'w')
tempwr.write(str(res_dict) + '\n')
for result in results:
    tempwr.write("".join(word.ljust(17) for word in result) + '\n')
tempwr.close()
os.popen('chmod 777 ' + str(tempf) + ' 2> /dev/null')
