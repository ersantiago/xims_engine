#!/bin/bash

ftpsrv='abc.com'
acct="xxxxxxxx"
passwd="xxxxxxxx"
rpath=$2

inpath=$1
file=$(basename $inpath)
lpath=$(dirname $inpath)

cd $lpath
ftp -n $ftpsrv <<END_SCRIPT
quote USER $acct
quote PASS $passwd
cd $rpath
put $file 
quit
END_SCRIPT
exit 0
