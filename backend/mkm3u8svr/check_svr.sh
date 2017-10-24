#!/bin/sh

while true
do
sn=`ps -ef | grep mkm3u8svr | grep -v grep | grep -v sh |awk '{print $2}'`
#echo $sn
if [ "${sn}" = "" ];
then
#echo "start process....."
cd /home/xhzc/py_mkm3u8
nohup ./mkm3u8svr.py> /dev/null &
fi
sleep 1
done
#####
