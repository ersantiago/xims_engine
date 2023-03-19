#!/home/emerson/anaconda3/bin/python
import os, re
import pygsheets
import ast

print('Sync Activity Tracker to Google Sheet.')
it_gsheet = 'https://docs.google.com/spreadsheets/d/1FrXPjHJ3DxsuM66ydv9chpz-2hEwpMUvnDKHwAMmY1w/edit?ts=60b9ed36#gid=0'
#path_cred = 'C:\\git\\emerson_it\\IT-DA-9a643fc39003.json'
#prdtck_file = 'C:\\git\\emerson_it\\prd_table.list'
path_cred = '/mnt/share/scripts/admin_scripts/api/IT-DA-9a643fc39003.json'
prdtck_file = '/opt/lampp/htdocs/ftp_xims/prod/prdbdir/prd_table.list'

# Load Sheet Config
print('Initializing Sheet & Config')
gc = pygsheets.authorize(service_file=path_cred)
wks = gc.open_by_url(it_gsheet)
sheet = wks.worksheet_by_title('Main')

# Load Sync File
print('Updating Worksheet ' + str(wks.title))
load_prdtable = open(prdtck_file, 'r').read()
prdtable = ast.literal_eval(load_prdtable)
sheet.clear()
sheet.update_values('A1', prdtable)
print('Done')
