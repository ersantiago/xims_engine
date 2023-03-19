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
    cfg = wks.worksheet_by_title(sheetname).get_values(start, end)
    cfg[:] = (value for value in cfg if value != ['','',''])
    switch = wks.worksheet_by_title(sheetname).get_value(sw_addr)
    return cfg, switch

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
    if switch == 'yes':
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
# For sysnc, follow below inputs
# cfgsync('configs sheet tab name', 'start cell address', 'end cell address', 'sync cell address', 'config file name', 'path in remote namecheap' #

# Devices Table
cfgsync('it_linuxtable','A4','C401','B2','it_linuxtable','xit')
cfgsync('it_wintable','A4','C201','B2','it_wintable','xit')

# Configs
#cfgsync('cfg_linux','A4','C21','B2','cfglinux_login','public_html/infra')
#cfgsync('cfg_linux','G4','I21','H2','cfglinux_rtime','public_html/infra')

#cfgsync('cfg_windows','A4','C21','B2','cfgwindows_login','public_html/infra')
#cfgsync('cfg_windows','G4','I21','H2','cfgwindows_rtime','public_html/infra')

cfgsync('cfg_linux','G4','I21','H2','cfgwfh','public_html/infra')
cfgsync('cfg_windows','G4','I21','H2','cfgwin','public_html/infra')

# v2 tests
#cfgsync('cfg_linuxv2','A4','E30','B1','cfglinuxv2','public_html/infra')
