#!/usr/bin/python
import os, re, ast
from shutil import copyfile

# Get from temp directory
ftpdir_tmp = '/opt/lampp/htdocs/ftp_xims/linux'
xims_dir = '/mnt/share/scripts/monitoring/xims/linux'
xims_cfg = 'http://172.16.41.17/infra/configs/xims_linux.cfg'
pc_table = '/mnt/share/scripts/configs/linuxtable.cfg'

os.chdir(ftpdir_tmp)
allfiles = os.listdir('.')
for file in allfiles:
    if not os.stat(file).st_size == 0 and file.endswith('_pc.info'):
        filed = os.path.join(xims_dir, 'pcdata', file)
        copyfile(file, filed)

# Get config details
xims_cfgraw = ast.literal_eval(os.popen('curl ' + xims_cfg).read())
xims_cfg = []
for config in xims_cfgraw:
     if config[2] == 'realtime':
        print('OK realtime')
        xims_cfg.append(config)
cfglen   = len(xims_cfg) + 4
sortasnum = ['bw_24', 'bw_r']

# Data Paths
datdir    = os.path.join(xims_dir, 'pcdata')
data_table   = os.path.join(xims_dir, 'linux_data')
data_list = os.path.join(xims_dir, 'linux_data.list')
tmpfile   = os.path.join(xims_dir, 'linux_tmp.txt')

writetmp  = open(tmpfile, 'w')
writedict = open(data_list, 'w')

# Get Devices List
reflist = ast.literal_eval(open(pc_table, 'r').read())

cfglist = []
for i in range(len(xims_cfg)):
    cfglist.append(xims_cfg[i][0])

wpsync_format = []
headerlist = ['Site', 'PC-Tag', 'MAC', 'Assignee'] + cfglist
wpsync_format.append(headerlist)

# Add to reflist
allfiles = os.listdir(datdir)
for file in allfiles:
    filemac = '.'.join(file.split('_')[0:3])
    if filemac not in str(reflist):
        #addme = "".join(word.ljust(11) for word in ['NoTag', 'NoTag', 'NoTag', filemac])
        addme = ['NoTag', 'NoTag', filemac, 'NoTag']
        reflist.append(addme)
        print(addme)
for pc in reflist:
    mac = pc[2]
    bfile = mac.replace('.', '_') + '_pc.info'
    login_file = os.path.join(datdir, bfile)
    try:
        with open(login_file, 'r') as f:
            login_info = ast.literal_eval(f.read().splitlines()[0])
        temp = pc[0:4]
        for cfg in cfglist:
            try:
                login_info[cfg] = str(login_info[cfg]).replace('\n','---').strip()
                login_info[cfg] = str(login_info[cfg]).replace('Runtime error','0').strip()
                if len(login_info[cfg]) > 18:
                    login_info[cfg] = login_info[cfg][0:18]
                temp.append(login_info[cfg])
            except:
                if cfg in sortasnum:
                    temp.append('0')
                else:
                    temp.append('---')
        temp[4] = '   ' + temp[4]
        gatherer_print = "".join(word.ljust(17) for word in temp)
        wpsync_format.append(temp)

    except:
        temp = pc[0:4]
        temp.append('   nofile')
        while len(temp) != cfglen:
            temp.append(' ')
        gatherer_print = "".join(word.ljust(17) for word in temp)
        wpsync_format.append(temp)
    print(gatherer_print)
    writetmp.write(gatherer_print + '\n')
writedict.write(str(wpsync_format) + '\n')
writetmp.close()
copyfile(tmpfile, data_table)
