#!/usr/bin/python
import os, re, ast
from shutil import copyfile

# Get from temp directory
ftpdir_tmp = '/opt/lampp/htdocs/ftp_xims/linux/patch'
os.chdir(ftpdir_tmp)
allfiles = os.listdir('.')
for file in allfiles:
    if not os.stat(file).st_size == 0 and file.endswith('_patch.info'):
        filed = os.path.join('/mnt/share/scripts/monitoring/workstations/linux/patch', file)
        copyfile(file, filed)
admin_cfg = [['user'],['local_ip'],['last_active']]
wfh_cfglogin = ast.literal_eval(os.popen('curl http://172.16.41.17/infra/configs/patchlinux.cfg').read())
wfh_cfglogin = admin_cfg + wfh_cfglogin
cfglen = len(wfh_cfglogin) + 3

wksdir = '/mnt/share/scripts/monitoring/workstations/linux'
datdir = os.path.join(wksdir, 'patch')

lgntable = '/mnt/share/scripts/monitoring/workstations/linux/patch_data'
lgntable_d = '/mnt/share/scripts/monitoring/workstations/linux/patch_data.list'

tmpfile = os.path.join(wksdir, 'patch_tmp.txt')
writetmp = open(tmpfile, 'w')
writedict = open(lgntable_d, 'w')

#wfh_cfgtable = os.path.join(wksdir, 'it_linuxtable')
linuxtable = '/mnt/share/scripts/configs/linuxtable.cfg'
reflist = ast.literal_eval(open(linuxtable, 'r').read())

cfglist = []
for i in range(len(wfh_cfglogin)):
    cfglist.append(wfh_cfglogin[i][0])

wpsync_format = []
headerlist = ['Site', 'PC-tag', 'Mac'] + cfglist
wpsync_format.append(headerlist)

# Add to reflist
allfiles = os.listdir(datdir)
for file in allfiles:
    filemac = '.'.join(file.split('_')[0:3])
    if filemac not in str(reflist):
        addme = "".join(word.ljust(11) for word in ['NoTag', 'NoTag', filemac])
        addme = ['NoTag', 'NoTag', filemac]
        print(str(addme))
        reflist.append(addme)
for pc in reflist:
    mac = pc[2]
    bfile = mac.replace('.', '_') + '_patch.info'
    login_file = os.path.join(datdir, bfile)
    try:
        with open(login_file, 'r') as f:
            login_info = ast.literal_eval(f.read().splitlines()[0])
        temp = pc[0:3]
        for cfg in cfglist:
            try:
                login_info[cfg] = str(login_info[cfg]).replace('\n','---').strip()
                login_info[cfg] = str(login_info[cfg]).replace('Runtime error','0').strip()
                if len(login_info[cfg]) > 18:
                    login_info[cfg] = login_info[cfg][0:18]
                temp.append(login_info[cfg])
            except:
                temp.append('---')
        temp[3] = '   ' + temp[3]
        login_print = "".join(word.ljust(17) for word in temp)
        wpsync_format.append(temp)

    except:
        temp = pc[0:3]
        temp.append('   nofile')
        while len(temp) != cfglen:
            temp.append('-')
        login_print = "".join(word.ljust(17) for word in temp)
        wpsync_format.append(temp)
    print(login_print)
    writetmp.write(login_print + '\n')
writedict.write(str(wpsync_format) + '\n')
writetmp.close()
copyfile(tmpfile, lgntable)
