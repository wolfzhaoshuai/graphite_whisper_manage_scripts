import os
import sys
import commands
import re
import time

def handle(rentention, xFileFactor, method, directory):
    pattern = "^/data/data/whisper/whisper/nginx/[a-zA-Z0-9_./-]+/status_code/[1-5]\d+\.wsp$"
    resize_cmd_pattern = "whisper-resize.py --nobackup {} {} --xFilesFactor={}"
    reset_method_pattern = "whisper-set-aggregation-method.py {} {}"
    progress = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if re.match(pattern, file_path):
                print file_path
                resize_cmd = resize_cmd_pattern.format(file_path, rentention, xFileFactor)
                print resize_cmd
                commands.getstatusoutput(resize_cmd)
                reset_method_cmd = reset_method_pattern.format(file_path, method)
                print reset_method_cmd
                commands.getstatusoutput(reset_method_cmd)
            progress += 1
            if progress % 1000 == 0:
                print progress
    print 'total handled %d files' % progress


def main():
    if len(sys.argv) != 2:
        print 'please give the root path'
        return
    root_dir = os.path.abspath(sys.argv[1])
    print 'start at: ', time.ctime()
    method = 'sum'
    x_file_factor = '0.0'
    rentention = "10s:1d 1m:30d 1d:5y"
    handle(rentention, x_file_factor, method, root_dir)
    print 'end at: ', time.ctime()


if __name__ == "__main__":
    main()