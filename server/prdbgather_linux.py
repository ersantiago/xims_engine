#!/usr/bin/python3
import os, re, ast
from shutil import copyfile
import time
#=================== VARIABLES =====================#

#wksdir = '/home/emersonahs/xit/wksdata'
#tmp_prdb = '/home/emersonahs/prdb'
#prdbdir = '/home/emersonahs/xit/esantiag/prdbdir'

wksdir = '/opt/lampp/htdocs/ftp_xims/linux'
tmp_prdb = '/opt/lampp/htdocs/ftp_xims/prod'
prdbdir = '/opt/lampp/htdocs/ftp_xims/prod/prdbdir'

#prdtable = '/home/emersonahs/xit/esantiag/prdbdir/prd_table'
#prdtable_d = '/home/emersonahs/xit/esantiag/prdbdir/prd_table.list'
#tmpfile = '/home/emersonahs/xit/esantiag/prdbdir/prd_table.tmp'
#linuxtable = '/home/emersonahs/xit/it_linuxtable'
#empfile = '/home/emersonahs/xit/emp_dict'

prdtable = '/opt/lampp/htdocs/ftp_xims/prod/prdbdir/prd_table'
prdtable_d = '/opt/lampp/htdocs/ftp_xims/prod/prdbdir/prd_table.list'
tmpfile = '/opt/lampp/htdocs/ftp_xims/prod/prdbdir/prd_table.tmp'
linuxtable = '/mnt/share/scripts/configs/linuxtable.cfg'
empfile = '/mnt/share/scripts/configs/emp_dict'

#wksdir = 'C:\\Users\\ersantiago\\Desktop\\ftp_xims'
#tmp_prdb = 'C:\\Users\\ersantiago\\Desktop\\prdb'
#prdbdir = 'C:\\Users\\ersantiago\\Desktop\\prdbdir'

#prdtable = 'C:\\Users\\ersantiago\\Desktop\\prdb\\prd_table'
#prdtable_d = 'C:\\Users\\ersantiago\\Desktop\\prdb\\prd_table.list'
#tmpfile = 'C:\\Users\\ersantiago\\Desktop\\prdb\\prd_table.tmp'

#linuxtable = 'C:\\Users\\ersantiago\\Desktop\\it_linuxtable'

#=================== FUNCTIONS =====================#
def astme(dbfile):
    try:
        with open(dbfile, 'r') as f:
            astmee = ast.literal_eval(f.read())
    except:
        astmee = ['nodata']
    return astmee

def first_astme(login_file):
    try:
        with open(login_file, 'r') as f:
            astmee = ast.literal_eval(f.read().splitlines()[0])
    except:
        astmee = ['nodata']
    return astmee

#=================== CHECK DATA =====================#
#datec = os.popen('date +%Y%m%d -d \'+12 hour\'').read().strip()
datec = os.popen('date +%Y%m%d').read().strip()
# datec = '20200907'
print(datec)
os.chdir(tmp_prdb)
allfiles = os.listdir('.')
print(str(allfiles))
#time.sleep(3)
print(datec)
for file in allfiles:
    if not os.stat(file).st_size == 0 and file.endswith('.prdb'):
        if file.startswith(datec):
            filed = os.path.join(prdbdir, file)
            copyfile(file, filed)
            print('copying: ' + str(file) + ' to ' + str(filed))

''' Dictionary Reference:
'lgn'
'lgn_mins'
'online'
'wfica'
    '1st','1st_mins', 'active', 'total'
'chrome': 
    '1st','1st_mins', 'active', 'total'
'others'
'''

#=================== PARSING =====================#
tablelen = 10

writetmp = open(tmpfile, 'w')
writedict = open(prdtable_d, 'w')

reflist = ast.literal_eval(open(linuxtable, 'r').read())

wpsync_format = []
headerlist = ['Tag', 'User', 'Online_hrs', 'PC_login', 'Ctx_Start', 'Ctx_Delay', 'Ctx_Actv', 'Ctx_Total', 'Brws_Start', 'Brws_Actv', 'Brws_Total', 'Idle_hrs', 'Last_Online']
prdblist = ['lgn', 'lgn_mins', 'online', 'wfica/chrome : 1st, 1st_mins, active, total', 'others']
wpsync_format.append(headerlist)

# Add to reflist
allfiles = os.listdir(prdbdir)
print(str(allfiles))
#time.sleep(3)
for file in allfiles:
    if file.startswith(datec):
        filemac = '.'.join(file.strip('.prdb').split('_')[1:4])
        if filemac not in str(reflist):
            addme = "".join(word.ljust(11) for word in ['NoTag', 'NoTag', filemac])
            addme = ['NoTag', 'NoTag', filemac]
            print(str(addme))
            reflist.append(addme)

empdict = astme(empfile)

for pc in reflist:
    mac = pc[2]
    bfilename = mac.replace('.', '_') + '_lgn.info'
    pcfilename = mac.replace('.', '_') + '_pc.info'
    dbfilename = datec + '_' + mac.replace('.', '_') + '.prdb'

    login_file = os.path.join(wksdir, bfilename)
    rt_file = os.path.join(wksdir, pcfilename)
    prdb_file = os.path.join(prdbdir, dbfilename)

    if os.path.exists(prdb_file):
        print('prdb file exists : ' + dbfilename)

        try:
            login_info = first_astme(login_file)
            rt_info = first_astme(rt_file)
            prdb_info = astme(prdb_file)
            headerlist = ['Tag', 'User', 'First_Name', 'Online_hrs', 'PC_login', 'Ctx_Start', 'Ctx_Delay', 'Ctx_Actv',
                          'Ctx_Total', 'Brws_Start', 'Brws_Delay', 'Brws_Actv', 'Brws_Total']
            prdblist = ['lgn', 'lgn_mins', 'online', 'wfica/chrome : 1st, 1st_mins, active, total', 'others']
            tag  = pc[0]

            try:
                user = login_info['user']
                if user == 'guest':
                    user = pc[3]
            except:
                user = 'tbi'
            try:
                #last = login_info['last_seen'].split('_')[-1].strip('[').strip(']')
                last = rt_info['last_active']
            except:
                last = '00:00'
            try:
                fname = empdict[user]
            except:
                fname = 'notfound'

            try:
                online   = str(round(float(prdb_info['online']) / 60,2))
            except:
                online = 'nodata'
            pclogin  = prdb_info['lgn']
            ctxstart = prdb_info['wfica']['1st']

            try:
                ctxdel   = str(prdb_info['wfica']['1st_mins'] - prdb_info['lgn_mins'])
            except:
                ctxdel = str(prdb_info['wfica']['1st_mins'] - 0)
            try:
                ctxactv  = str(round(float(prdb_info['wfica']['active']) / 60, 2))
            except:
                ctxactive = 'nodata'

            try:
                ctxtot   = str(round(float(prdb_info['wfica']['total']) / 60, 2))
            except:
                ctxtot = 'nodata'

            brwstart = prdb_info['chrome']['1st']
            brwdel   = str(prdb_info['chrome']['1st_mins'] - prdb_info['lgn_mins'])
            brwactv  = str(round(float(prdb_info['chrome']['active']) / 60, 2))
            brwtot   = str(round(float(prdb_info['chrome']['total']) / 60, 2))

            try:
                idle = str(round(float(prdb_info['idle']) / 60, 2))
            except:
                idle = 'nodata'
            temp = [tag, user, online, pclogin, ctxstart, ctxdel, ctxactv, ctxtot, brwstart, brwactv, brwtot, idle, last]
            login_print = "".join(word.ljust(17) for word in temp)
            wpsync_format.append(temp)
        except:
            temp = pc[0:3]
            temp.append('corrupt_file')
            while len(temp) != tablelen:
                temp.append(' ')
            login_print = "".join(word.ljust(17) for word in temp)
            # wpsync_format.append(temp)
            print('No data. No need to append for ' + str(mac))

        print(login_print)
        writetmp.write(login_print + '\n')
    else:
        print('prdb file does not exist : ' + dbfilename + ' No action done.')
writedict.write(str(wpsync_format) + '\n')
writetmp.close()
copyfile(tmpfile, prdtable)
