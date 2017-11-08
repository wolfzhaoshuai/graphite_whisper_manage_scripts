#!/usr/bin/env python

import os
import commands
import time


#whisper tmp backup dir in new clusters
ORIGIN_DIR = '/home/xxx/whisper_backup'
#whisper storage location
WHISPER_PREFIX = '/data/whisper'

#if the whisper file exists, then whisper-merge, otherwhise
# to find if upper dir exists, if not, then mkdir, then copy
#finally rm this whisper file
def handle():
    for filename in os.listdir(ORIGIN_DIR):
        src_name = os.path.join(ORIGIN_DIR, filename)
        tmp_list = filename.split('.')
        dst_dir_name = '/'.join(tmp_list[:len(tmp_list)-1])
        dst_dir_name = os.path.join(WHISPER_PREFIX, dst_dir_name)
        if not os.path.exists(dst_dir_name):
            mkdir_cmd = 'sudo -u xxx mkdir -p %s' % dst_dir_name
            res = commands.getstatusoutput(mkdir_cmd)
            if res[0] != 0:
                print dst_dir_name, ' make error'
                continue
            print 'mkdir ', dst_dir_name, ' done'
        true_name = '/'.join(tmp_list)
        true_name = true_name + '.wsp'
        dst_name = os.path.join(WHISPER_PREFIX, true_name)
        merge_cmd = 'sudo cp %s %s' % (src_name, dst_name)
        if os.path.exists(true_name):
            merge_cmd = 'sudo whisper-fill %s %s' % (filename, true_name)
        res = commands.getstatusoutput(merge_cmd)
        if res[0] != 0:
            print filename, ' merge error'
            continue
        chown_cmd = 'sudo chown -R xxx %s' % dst_dir_name
        chgrp_cmd = 'sudo chgrp -R xxx %s' % dst_dir_name
        commands.getstatusoutput(chown_cmd)
        commands.getstatusoutput(chgrp_cmd)
        print 'merge ', filename, ' done'
        clear_cmd = 'rm %s' % src_name
        res = commands.getstatusoutput(clear_cmd)
        if res[0] != 0:
            print filename, ' rm error'
            continue
        #print 'rm ', src_name, ' done'


def main():
    print 'start merge at: ', time.ctime()
    handle()
    print 'end merge at: ', time.ctime()


if __name__ == "__main__":
    main()
