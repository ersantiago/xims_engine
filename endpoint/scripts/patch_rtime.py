#!/usr/bin/python3
import re
import os
import ast

print('\n===================================================================================')
print('|                                    PATCH CHECK                                  |')
print('===================================================================================\n')

##############################################################
############              FUNCTIONS               ############
##############################################################

def cfgrtime():
    try:
        patchlinux = ast.literal_eval(os.popen('curl http://172.16.41.17/infra/configs/patchlinux.cfg').read())
    except:
        patchlinux = ast.literal_eval(os.popen('curl http://abc.com/infra/patchlinux.cfg').read())
    patchrtime = []
    for patch in patchlinux:
        status = patch[1]
        if status == 'active':
            patchrtime.append(patch)
    return patchrtime

def getmac():
    ### Get mac address
    cmdout = os.popen('ip a').read()

    # regexes
    rgxip = re.compile(r'inet\s+(172.*)?/')
    rgxmac = re.compile(r'link/ether\s(.*)?\sbrd')

    # get data
    maclst = rgxmac.findall(cmdout)[0].lower().split(':')
    mac = ''.join([maclst[0], maclst[1], '.', maclst[2], maclst[3], '.', maclst[4], maclst[5]])
    return mac

##############################################################
############                                      ############
##############################################################

test1 = 'xxxxxxxxxxxxxxxxxxx'
dpw = bytes.fromhex(test1).decode('utf-8')

# Get from functions
print('Checking Patch Engine Configs. . .')
patchrtime = cfgrtime()
mac = getmac()

#print(patchrtime)
print('\nMac Address: ' + mac + '\n')
print('============================================\n')
results = []
results.append(['Variable', 'Result'])
#Add current user
user = os.popen('who | grep -v root | head -1 | awk \'{print $1}\' | grep -v 172.16.41.17').read().strip()
results.append(['User', user])
last_seen = os.popen('date +%b%d_%G_[%R]').read().strip()
results.append(['Last_seen', last_seen])
for i in range(len(patchrtime)):
    patchname, status, target, maclist, cmdtype, fullcmd, crittype, critcmd = patchrtime[i]
    maclist = maclist.splitlines()

    print('Patch Name: ' + patchname)

    ##############################################################
    ############          CRITERIA CHECKING           ############
    ##############################################################

    # Target Condition
    if target == 'all':
        target_chk = True
    elif target == 'mac':
        if mac in maclist:
            target_chk = True
        else:
            target_chk = False
    else:
        target_chk = False
    print('\tTarget PC: ' + str(target_chk))

    # Criteria Condition
    if target_chk:
        print('\tChecking run criteria...')
        if crittype == 'unix':
            print('\t\tcriteria_cmdtype => unix')
            run_con = os.popen(critcmd).strip()

        elif crittype == 'python':
            print('\t\tcriteria_cmdtype => python')
            exec(critcmd)
            try:
                run_con = str(eval(patchname))
            except:
                run_con = 'critvar_err'
        else:
            run_con = 'False'
        print('\t\truncrit_cmdres : ' + run_con)

        false_strs = ['false', 'f', 'n', 'no']
        true_strs = ['true', 't', 'y', 'yes']

        if run_con.lower() in true_strs:
            run_con = 'yes'
        elif run_con.lower() in false_strs:
            run_con = 'no'
        else:
            run_con = 'boolean_err'

        ##############################################################
        #################          EXECUTE        ####################
        ##############################################################

        if run_con == 'yes':
            print('\tExecuting Patch.')
            try:
                if cmdtype == 'unix':
                    print('\t\t' + patchname + ' : cmdtype => unix')
                    
                    fullcmd = ' ; '.join(fullcmd.splitlines())
                    execute_cmd = os.popen(fullcmd).read()
                    print(execute_cmd)
                    cmdout = 'deploy_ip'
                elif cmdtype == 'python':
                    print(patchname + ' : cmdtype => python')
                    exec(fullcmd)
                    cmdout = 'deploy_ip'
                else:
                    print(patchname + '\tcmdtype : unknown')
                    cmdout = 'cmdtype_err'
            except:
                cmdout = 'Runtime_err'

        elif run_con == 'no':
            print('\t\tCriteria already met, no action.')
            cmdout = 'OK'

        else:
            cmdout = 'var_err'

    else:
        run_con = 'no'
        cmdout = 'Skip'
    print('\tRun Criteria: ' + str(run_con))

    print('Patch Status  : ' + str(cmdout))
    print('\n============================================\n')
    result = [patchname, cmdout]
    results.append(result)
print('')
#print(str(results))
res_dict ={}
for result in results:
    rkey, rval = result
    res_dict[rkey] = rval
print(res_dict)

#====================== Transfer via FTP =========================#
ftfile = mac.replace('.','_') + '_patch.info'
print('\nCreating temp directory and files...')
tempf = os.path.join('/home/.xims/tmp', ftfile)
tempfb = os.path.basename(tempf)
print(tempf)
tempwr = open(tempf, 'w')
tempwr.write(str(res_dict) + '\n')
for result in results:
    tempwr.write("".join(word.ljust(17) for word in result) + '\n')
tempwr.close()
os.popen('chmod 777 ' + str(tempf) + ' 2> /dev/null')

# Upload patch stats to nfs and nc
umacv2 = mac.replace('.','_')
patchfile = '/home/.xims/tmp/' + umacv2 + '_patch.info'
pcfile = '/home/.xims/tmp/' + umacv2 + '_pc.info'
lgnfile = '/home/.xims/tmp/' + umacv2 + '_lgn.info'

ftpnfs_patch = ' '.join(['/home/.xims/scripts/nfs_ftsyn.sh',patchfile,'ftp_temp/linuxpatch'])
ftpnfs_pc = ' '.join(['/home/.xims/scripts/nfs_ftsyn.sh',pcfile,'ftp_temp/linuxpatch'])
ftpnfs_lgn = ' '.join(['/home/.xims/scripts/nfs_ftsyn.sh',lgnfile,'ftp_temp/linuxpatch'])

ftpnc_patch = ' '.join(['/home/.xims/scripts/nc_ftsyn.sh',patchfile,'ftp_xims/linuxpatch'])
ftpnc_pc = ' '.join(['/home/.xims/scripts/nc_ftsyn.sh',pcfile,'ftp_xims/linuxpatch'])
ftpnc_lgn = ' '.join(['/home/.xims/scripts/nc_ftsyn.sh',lgnfile,'ftp_xims/linuxpatch'])

patchup1 = os.popen(ftpnfs_patch).read()
pcup1 = os.popen(ftpnfs_pc).read()
lgnup1 = os.popen(ftpnfs_lgn).read()

patchup2 = os.popen(ftpnc_patch).read()
pcup2 = os.popen(ftpnc_pc).read()
lgnup2 = os.popen(ftpnc_lgn).read()

print('Patch updates done.\n')
print('===================================================================================\n')
