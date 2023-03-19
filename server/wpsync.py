#!/home/emerson/anaconda3/bin/python

import mysql.connector
import ast

table_path = '/mnt/share/scripts/monitoring/workstations/admin/it_table'
wintable_path ='/mnt/share/scripts/monitoring/workstations/admin/win_table'

cnx = mysql.connector.connect(
    user='root',
    password='!+@dMiN',
    database='wp_emersondb',
    unix_socket='/opt/lampp/var/mysql/mysql.sock',
    use_pure=False
)

#sql = "SELECT post_content FROM `wp_posts` WHERE ID='6'"
mycursor = cnx.cursor()
#mycursor.execute(sql)

#dbdat = mycursor.fetchall()
#listdat = ast.literal_eval(dbdat[0][0])

#with open(table_path) as tbp:
#    nfslist = tbp.read().splitlines()

#nfslist.insert(0,listdat[0])
#for i in range(1,len(nfslist)):
#    nfslist[i] = nfslist[i].split()

#strnfslist = str(nfslist).replace('\'', '"')
#sqldump = "UPDATE wp_posts SET post_content='" + strnfslist + "' WHERE ID='6'"
#mycursor.execute(sqldump)

#################         LINUX (OLD VIA NAMECHEAP)          ###################
#wfh_login_file = '/mnt/share/scripts/monitoring/workstations/wfh/nclogin_table.list'
#wfh_login_list = open(wfh_login_file, 'r').read()
#wfh_login_list = str(wfh_login_list).replace('\'', '"')
#sqldump_wfhlogin = "UPDATE wp_posts SET post_content='" + wfh_login_list + "' WHERE ID='616'"
#mycursor.execute(sqldump_wfhlogin)


#################         LINUX (VIA NFS)      ###################
linuxd_file = '/mnt/share/scripts/monitoring/workstations/linux/linux_data.list'
linuxd_list = open(linuxd_file, 'r').read()
linuxd_list = str(linuxd_list).replace('\'', '"')
sqldump_linuxd = "UPDATE wp_posts SET post_content='" + linuxd_list + "' WHERE ID='5'"
mycursor.execute(sqldump_linuxd)

#################         LINUX (VIA NFS)      ###################
linuxdv2_file = '/mnt/share/scripts/monitoring/xims/linux/linux_data.list'
linuxdv2_list = open(linuxdv2_file, 'r').read()
linuxdv2_list = str(linuxdv2_list).replace('\'', '"')
sqldump_linuxdv2 = "UPDATE wp_posts SET post_content='" + linuxdv2_list + "' WHERE ID='220'"
mycursor.execute(sqldump_linuxdv2)

#################         XIMS_WIN         ####################
win_login_file = '/mnt/share/scripts/monitoring/workstations/win/nclogin_wintable.list'
win_login_list = open(win_login_file, 'r').read()
win_login_list = str(win_login_list).replace('\'', '"')
win_login_list = str(win_login_list).replace('\\r', '')
sqldump_winlogin = "UPDATE wp_posts SET post_content='" + win_login_list + "' WHERE ID='12'"
mycursor.execute(sqldump_winlogin)


#################         LINUX PATCH        ###################
patchfile = '/mnt/share/scripts/monitoring/workstations/linux/patch_data.list'
patchlist = open(patchfile, 'r').read()
patchlist = str(patchlist).replace('\'', '"')
sqldump_patch = "UPDATE wp_posts SET post_content='" + patchlist + "' WHERE ID='14'"
mycursor.execute(sqldump_patch)

################         WINDOWS PATCH      ###################
patchfile_win = '/mnt/share/scripts/monitoring/workstations/win/patch_data.list'
patchlist_win = open(patchfile_win, 'r').read()
patchlist_win = str(patchlist_win).replace('\'', '"')
sqldump_patch_win = "UPDATE wp_posts SET post_content='" + patchlist_win + "' WHERE ID='383'"
mycursor.execute(sqldump_patch_win)


#################         PRDCTVITY        ###################
#prdbfile = '/home/ersantiago/.tmp/prdb/.dat/prd_table.list'
prdbfile = '/opt/lampp/htdocs/ftp_xims/prod/prdbdir/prd_table.list'
prdblist = open(prdbfile, 'r').read()
prdblist = str(prdblist).replace('\'', '"')
sqldump_prdb = "UPDATE wp_posts SET post_content='" + prdblist + "' WHERE ID='135'"
mycursor.execute(sqldump_prdb)

##################        NETWORK CHARTS : ISP1       ###################
pingtrace_file = '/mnt/share/scripts/db/ispstat_pldt.csv'
ping_list = open(pingtrace_file, 'r').read().splitlines()
us1_wpsync_list = ['a:',str(len(ping_list)-1),':{']
in1_wpsync_list = ['a:',str(len(ping_list)-1),':{']
lcy_wpsync_list = ['a:',str(len(ping_list)-1),':{']
# append_format = 'i:<INDEX>;a:3:{i:0;s:4:"<TIME>";i:1;d:<VAL1>;i:2;d:<VAL2>;i:3;d:<VAL3>;}'
for i in range(1,len(ping_list)):
    time, trus01, trin01, dnscf_us01, dsngg_us01, dnscf_in01, dnsgg_in01 = ping_list[i].split(',')

    # Chart US01 parse (pldt)
    us1_parsed = ['i:', str(i - 1), ';a:4:{i:0;s:5:"', time, '";i:1;d:', trus01, ';i:2;d:', dnscf_us01, ';i:3;d:', dsngg_us01, ';}']
    us1_wpsync_list.append(''.join(us1_parsed))

    # Chart IN01 parse (pldt)
    in1_parsed = ['i:', str(i - 1), ';a:4:{i:0;s:5:"', time, '";i:1;d:', trin01, ';i:2;d:', dnscf_in01, ';i:3;d:', dnsgg_in01, ';}']
    in1_wpsync_list.append(''.join(in1_parsed))

    # Chart Latency parse (pldt)
    lcy_parsed = ['i:', str(i - 1), ';a:3:{i:0;s:5:"', time, '";i:1;d:', trus01, ';i:2;d:', trin01, ';}']
    lcy_wpsync_list.append(''.join(lcy_parsed))

# Chart US01 (pldt)
us1_wpsync_list.append('}')
us1_wpsync_join = ''.join(us1_wpsync_list)
sqldump_us1 = "UPDATE wp_posts SET post_content='" + us1_wpsync_join + "' WHERE ID='230'"
mycursor.execute(sqldump_us1)
cnx.commit()

# Chart IN01 (pldt)
in1_wpsync_list.append('}')
in1_wpsync_join = ''.join(in1_wpsync_list)
sqldump_in1 = "UPDATE wp_posts SET post_content='" + in1_wpsync_join + "' WHERE ID='450'"
mycursor.execute(sqldump_in1)
cnx.commit()

# Chart Latency (pldt)
# ID number equivalent to id number in visualizer dashboard
lcy_wpsync_list.append('}')
lcy_wpsync_join = ''.join(lcy_wpsync_list)
sqldump_lcy = "UPDATE wp_posts SET post_content='" + lcy_wpsync_join + "' WHERE ID='265'"
mycursor.execute(sqldump_lcy)
cnx.commit()


##################        NETWORK CHARTS : RISE       ###################
pingtrace_file = '/mnt/share/scripts/db/ispstat_rise.csv'
ping_list = open(pingtrace_file, 'r').read().splitlines()
us1_wpsync_list = ['a:',str(len(ping_list)-1),':{']
in1_wpsync_list = ['a:',str(len(ping_list)-1),':{']
lcy_wpsync_list = ['a:',str(len(ping_list)-1),':{']
# append_format = 'i:<INDEX>;a:3:{i:0;s:4:"<TIME>";i:1;d:<VAL1>;i:2;d:<VAL2>;i:3;d:<VAL3>;}'
for i in range(1,len(ping_list)):
    time, trus01, trin01, dnscf_us01, dsngg_us01, dnscf_in01, dnsgg_in01 = ping_list[i].split(',')

    ''''# Chart US01 parse
    us1_parsed = ['i:', str(i - 1), ';a:4:{i:0;s:5:"', time, '";i:1;d:', trus01, ';i:2;d:', dnscf_us01, ';i:3;d:', dsngg_us01, ';}']
    us1_wpsync_list.append(''.join(us1_parsed))

    # Chart IN01 parse
    in1_parsed = ['i:', str(i - 1), ';a:4:{i:0;s:5:"', time, '";i:1;d:', trin01, ';i:2;d:', dnscf_in01, ';i:3;d:', dnsgg_in01, ';}']
    in1_wpsync_list.append(''.join(in1_parsed))
    '''

    # Chart Latency parse
    lcy_parsed = ['i:', str(i - 1), ';a:3:{i:0;s:5:"', time, '";i:1;d:', trus01, ';i:2;d:', trin01, ';}']
    lcy_wpsync_list.append(''.join(lcy_parsed))

'''
# Chart US01 (pldt)
us1_wpsync_list.append('}')
us1_wpsync_join = ''.join(us1_wpsync_list)
sqldump_us1 = "UPDATE wp_posts SET post_content='" + us1_wpsync_join + "' WHERE ID='470'"
mycursor.execute(sqldump_us1)
cnx.commit()

# Chart IN01 (pldt)
in1_wpsync_list.append('}')
in1_wpsync_join = ''.join(in1_wpsync_list)
sqldump_in1 = "UPDATE wp_posts SET post_content='" + in1_wpsync_join + "' WHERE ID='450'"
mycursor.execute(sqldump_in1)
cnx.commit()
'''

# Chart Latency (rise)
lcy_wpsync_list.append('}')
lcy_wpsync_join = ''.join(lcy_wpsync_list)
sqldump_lcy = "UPDATE wp_posts SET post_content='" + lcy_wpsync_join + "' WHERE ID='273'"
mycursor.execute(sqldump_lcy)
cnx.commit()


cnx.close()
print("WP Sync Done.")
