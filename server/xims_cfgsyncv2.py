#!/home/emerson/anaconda3/bin/python
import os, re
import pygsheets
import ast

### GLOBAL VARIABLES & PATHS ###
#path_cred = 'C:\\PyEx\\hr_scripts\\api\\IT-DA-9a643fc39003.json'
#nfs_cfgdir = 'C:\\Git\\emerson_it\\configs'

it_gsheet = 'https://docs.google.com/spreadsheets/d/1OXuBnhvfe2_iC-xkrdtadMtVv8TH9TcIscrUCZeKM2Q/edit?ts=5dcd6517#gid=0'
path_cred = '/mnt/share/scripts/admin_scripts/api/IT-DA-9a643fc39003.json'
nfs_cfgdir = '/mnt/share/scripts/configs'

# Load Sheet Config
gc = pygsheets.authorize(service_file=path_cred)
wks = gc.open_by_url(it_gsheet)

# Functions #

def getcfg(sheetname, start, end, sw_addr):
    cfgraw = wks.worksheet_by_title(sheetname).get_values(start, end)
    cfgraw[:] = (value for value in cfgraw if value != ['','',''])
    switch = wks.worksheet_by_title(sheetname).get_value(sw_addr)
    cfgfin = []
    for cfg in cfgraw:
        try:
            varname, status, sched, cmdtype, fullcmd = cfg
            if '' in cfg:
                varname = cfg[0]
                cfgerr = [varname, 'active', 'realtime', 'unix', 'echo ConfigError']
                cfgfin.append(cfgerr)
            elif status == 'active':
                cfgfin.append(cfg)
        except:
            varname = cfg[0]
            cfgerr = [varname, 'active', 'realtime', 'unix', 'echo ConfigError']
            cfgfin.append(cfgerr)
    return cfgfin, switch


def getpatch(sheetname, start, end, sw_addr):
    cfgraw = wks.worksheet_by_title(sheetname).get_values(start, end)
    cfgraw[:] = (value for value in cfgraw if value != ['','',''])
    switch = wks.worksheet_by_title(sheetname).get_value(sw_addr)
    cfgfin = []
    for cfg in cfgraw:
        try:
            varname, status, target, maclist, type_cmd, full_cmd, type_criteria, criteria_cmd  = cfg
            if '' in cfg:
                varname = cfg[0]
                cfgerr = [varname, 'active', 'realtime', 'unix', 'echo ConfigError']
                cfgfin.append(cfgerr)
            elif status == 'active':
                cfgfin.append(cfg)
        except:
            varname = cfg[0]
            cfgerr = [varname, 'active', 'realtime', 'unix', 'echo ConfigError']
            cfgfin.append(cfgerr)
    return cfgfin, switch

def gettable(sheetname, start, end, sw_addr):
    table = wks.worksheet_by_title(sheetname).get_values(start, end)
    table[:] = (value for value in table if value != ['','',''])
    switch = wks.worksheet_by_title(sheetname).get_value(sw_addr)
    return table, switch

def astme(filename):
    nfs_file = os.path.join(nfs_cfgdir, filename)
    try:
        with open(nfs_file, 'r') as f:
            ref_cfg = ast.literal_eval(f.read())
    except:
        ref_cfg = ['nodata']
    return ref_cfg, nfs_file

def ftupload(filepath, destpath):
    updscript = '/mnt/share/scripts/admin_scripts/nc_ftsyn.sh'
    updcmd = ' '.join([updscript, filepath, destpath])
    os.popen(updcmd).read()

# Ref filenames
wintable       = 'it_wintable'
linuxtable     = 'it_linuxtable'
cfglinux_rtime = 'cfglinux_rtime'
cfglinux_login = 'cfglinux_login'
cfgwin_rtime   = 'cfgwin_rtime'
cfgwin_login   = 'cfgwin_login'
cfgtemp        = 'xims_tmp'

# Sync
# Linux Rtime

def cfgsync(cfgtab, start, end, sw_addr, filename, rpath):
    cfgload, switch = getcfg(cfgtab, start, end, sw_addr)
    print('Config sheet tab: ' + cfgtab)
    print('Config filename: ' + filename)
    print('Sync mode : ' + switch)
    if switch == 'YES':
        print('Sync mode is on. Checking for config updates.')
        ref_cfg, fpath = astme(filename)
        if not os.path.exists(fpath):
            open(fpath, 'a').close()
        if cfgload != ref_cfg:
            print('Config out of sync detected.')
            with open(fpath, 'w') as cfgwrite:
                cfgwrite.write(str(cfgload))
            print('Updating file ' + fpath)
            print('Uploading ' + filename + ' to NC ftp. Location : ' + rpath)
            ftupload(fpath, rpath)
            print('Sync Done')
        else:
            print('Config already in sync, no updates required.')
    else:
        print('Sync mode is off. Exiting sync script.')
    print('\n')

def patchsync(cfgtab, start, end, sw_addr, filename, rpath):
    cfgload, switch = getpatch(cfgtab, start, end, sw_addr)
    print('Config sheet tab: ' + cfgtab)
    print('Config filename: ' + filename)
    print('Sync mode : ' + switch)
    if switch == 'YES':
        print('Sync mode is on. Checking for config updates.')
        ref_cfg, fpath = astme(filename)
        if not os.path.exists(fpath):
            open(fpath, 'a').close()
        if cfgload != ref_cfg:
            print('Config out of sync detected.')
            with open(fpath, 'w') as cfgwrite:
                cfgwrite.write(str(cfgload))
            print('Updating file ' + fpath)
            print('Uploading ' + filename + ' to NC ftp. Location : ' + rpath)
            ftupload(fpath, rpath)
            print('Sync Done')
        else:
            print('Config already in sync, no updates required.')
    else:
        print('Sync mode is off. Exiting sync script.')
    print('\n')

def tablesync(cfgtab, start, end, sw_addr, filename, rpath):
    cfgload, switch = gettable(cfgtab, start, end, sw_addr)
    print('Table sheet tab: ' + cfgtab)
    print('Table filename: ' + filename)
    print('Sync mode : ' + switch)
    if switch == 'YES':
        print('Sync mode is on. Checking for table updates.')
        ref_cfg, fpath = astme(filename)
        if not os.path.exists(fpath):
            open(fpath, 'a').close()
        if cfgload != ref_cfg:
            print('Config out of sync detected.')
            with open(fpath, 'w') as cfgwrite:
                cfgwrite.write(str(cfgload))
            print('Updating file ' + fpath)
            print('Uploading ' + filename + ' to NC ftp. Location : ' + rpath)
            ftupload(fpath, rpath)
            print('Sync Done')
        else:
            print('Config already in sync, no updates required.')
    else:
        print('Sync mode is off. Exiting sync script.')
    print('\n')

# For sysnc, follow below inputs
# cfgsync('configs sheet tab name', 'start cell address', 'end cell address', 'sync cell address', 'config file name', 'path in remote namecheap' #

# Engine Updates
cfgsync('cfglinux','A4','E100','B1','xims_linux.cfg','public_html/infra')
cfgsync('cfgwin', 'A4', 'E100','B1','xims_win.cfg','public_html/infra')

patchsync('patchlinux','A4','H100','B1','patchlinux.cfg','public_html/infra')
patchsync('patchwin', 'A4','H100','B1','patchwin.cfg','public_html/infra')

tablesync('linuxtable','A4','D501','B1','linuxtable.cfg','xit')
tablesync('wintable','A4','D151','B1','wintable.cfg','xit')
