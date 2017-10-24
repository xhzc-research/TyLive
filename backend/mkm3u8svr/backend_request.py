#!/usr/local/python3/bin/python3
# -*- coding: utf-8 -*-
import requests
import json
class BackendRequest:
    def __init__(self,host,port,timeout):
        self.__host = host
        self.__port = port
        self.__timeout = timeout
        self.__url = "http://%s:%d" % (host,port)

    def getM3U8TaskList(self):
        req_url = self.__url + "/vod/videoList"
        return requests.post(req_url,timeout=self.__timeout)

    def reportTaskResult(self,task_id,result,m3u8url,ftpurl,msg):
        req_url = self.__url + "/vod/reportCutResult"
        req_params = "?resourceCode=%s&msgCode=%d&resourceUrl=%s&ftpUrlCdn=%s&msgDetail=%s" % (task_id,result,m3u8url,ftpurl,msg)
        rv = requests.post(req_url+req_params,timeout=self.__timeout)
        print(rv.url)
        return rv
