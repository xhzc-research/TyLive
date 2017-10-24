#!/usr/local/python3/bin/python3
# -*- coding: utf-8 -*-

import backend_request
import m3u8_task
import threading
import time
import configparser
from sys import exit

def getTaskList(req):
    response = req.getM3U8TaskList()
    if response.status_code != 200:
        raise "response error %d" % response.status_code
    resp_json = response.json()
    rv_code = resp_json["code"]
    items = resp_json["data"]
    if rv_code != '0':
        return -1,""
    if len(items) == 0:
        return 1,""
    return 0,items

def parseTask(items,req,ftproot,ftphost,httphost):
    for x in items:
        id = x["resourceCode"]
        local_path = x["resourceUrl"]
        task = m3u8_task.M3U8Task(id, local_path)
        rv = task.doTask()
        print(rv)
        print("Task over result %d" % rv[0].value)
        resolute_path = rv[1].replace(ftproot,"")
        ftpurl = ftphost + resolute_path
        local_m3u8_addr = httphost + "vod" + resolute_path
        req.reportTaskResult(id, rv[0].value,local_m3u8_addr,ftpurl,"")

if __name__ == "__main__":
    try:
        conf = configparser.ConfigParser()
        conf.read("mkm3u8.conf")
        ftp_root = conf.get('ftp','ftp_root')
        ftp_host = conf.get('ftp','ftp_host')
        http_host = conf.get('http', 'http_host')
    except Exception as err:
        print(err)
        ftp_root = "/home/ismart/uploads/video"
        ftp_host = "ftp://127.0.0.1"
        http_host = "http://127.0.0.1"
    while (1):
        try:
            req = backend_request.BackendRequest('118.89.229.143', 18081, 3)
            get_rv = getTaskList(req)
            if get_rv[0] != 0:
                time.sleep(5)
                continue
            parseTask(get_rv[1],req,ftp_root,ftp_host,http_host)
            time.sleep(5)
        except Exception as err:
            print(err)
            time.sleep(5)
