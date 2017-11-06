#!/usr/bin/env python

import os
import sys
import time
import commands


def handle(rentention):
    if len(sys.argv) != 2:
        print 'please give the root path'
        return
    directory = os.path.abspath(sys.argv[1])
    cmd_pattern = "whisper-resize.py {} {}"
    rm_bak_file = "rm {}.bak"
    progress = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith(".wsp"):
                c_cmd = cmd_pattern.format(file_path, rentention)
                print c_cmd
                commands.getstatusoutput(c_cmd)
                rm_bak_file_cmd = rm_bak_file.format(file_path)
                print rm_bak_file_cmd
                commands.getstatusoutput(rm_bak_file_cmd)
            progress += 1
            if progress % 10000 == 0:
                print progress


def main():
    start = int(time.time() * 1000)
    rentention = "10s:1d 1m:30d 1d:5y"
    handle(rentention)
    print 'total cost %d ms' % (int(time.time() * 1000) - start)

if __name__ == "__main__":
    main()