#!/usr/local/python3/bin/python3
# -*- coding: utf-8 -*-
import subprocess
import os
from pathlib import Path
from enum import Enum

class TASK_ECODE(Enum):
    success=0
    raw_file_not_exists=10001
    ff_error=10002
    mkdir_failed=10003
    other_except=20000

class M3U8Task:
    def __init__(self,id,localpath):
        self.__local_path = localpath
        self.task_id = id

    def doTask(self):
        try:
            path_temp = Path(self.__local_path)
            if path_temp.exists() == False:
                return TASK_ECODE['raw_file_not_exists'],""
            base_dir = path_temp.parent
            print("base_dir %s" % base_dir)
            m3u8path = base_dir.joinpath(path_temp.stem)
            print("m3u8path %s" % m3u8path)
            m3u8path.mkdir(0o777, True, True)
            if m3u8path.is_dir() == False:
                return TASK_ECODE['mkdir_failed'],""
            m3u8path = m3u8path.joinpath("out.m3u8")
            sub_cmd = "ffmpeg -i %s -hls_time %d -hls_list_size 0 -c:v libx264 -c:a aac -strict -2 -f hls %s 1>/dev/null 2>/dev/null" % (self.__local_path,10,m3u8path)
            rv = subprocess.call(sub_cmd,shell=True)
            print("subprocess return %d" % rv)
            if rv == 0:
                if Path(m3u8path).exists():
                    return TASK_ECODE['success'],m3u8path.as_posix()
            return TASK_ECODE['ff_error'],""
        except Exception as err:
            print(err)
            return TASK_ECODE['other_except'],""
