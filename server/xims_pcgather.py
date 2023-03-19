#!/usr/bin/python3
import os, re, ast

nfs_cfglogin = '/mnt/share/scripts/configs/xims_cfglogin'
logintable = '/mnt/share/scripts/monitoring/workstations/admin/login_table'
logintable_dict = '/mnt/share/scripts/monitoring/workstations/admin/login_table.list'
wksdir = '/mnt/share/scripts/monitoring/workstations'
tmpfile = '/mnt/share/scripts/monitoring/workstations/admin/login_tmp.txt'
writetmp = open(tmpfile, 'w')
writedict = open(logintable_dict, 'w')

with open(nfs_cfglogin, 'r') as f:
    cfglogin = ast.literal_eval(f.read())

cfgtable = '/mnt/share/scripts/configs/it_table.cfg'
cfgtable_d = open(cfgtable, 'r')
reflist = cfgtable_d.read().splitlines()

cfglist = []
for i in range(len(cfglogin)):
    cfglist.append(cfglogin[i][0])

wpsync_format = []
headerlist = ['pc-tag', 'sw_prt', 'mac'] + cfglist
wpsync_format.append(headerlist)

for pc in reflist:
    mac = pc.split()[2]
    login_file = os.path.join(wksdir, mac, 'login.dict')
    try:
        with open(login_file, 'r') as f:
            login_info = ast.literal_eval(f.read())
        temp = pc.split()[0:3]
        for cfg in cfglist:
            try:
                temp.append(login_info[cfg])
            except:
                temp.append('')
        login_print = "".join(word.ljust(17) for word in temp)
        wpsync_format.append(temp)

    except:
        #print('No data found for ' + mac + ' . Report asap.')
        temp = pc.split()[0:3]
        temp.append('   nofile')
        login_print = "".join(word.ljust(17) for word in temp)
        wpsync_format.append(temp)
    print(login_print)
    writetmp.write(login_print + '\n')
writedict.write(str(wpsync_format) + '\n')
writetmp.close()
os.replace(tmpfile, logintable)