#!/usr/bin/env python
import os
import sys
import commands
import time


#new cluster ip:hostname
HOST_IP = {
    '1.2.3.4': 'hostname1',
    '2.3.4.5': 'hostname2',
}
#whisper tmp backup dir in new clusters
WHISPER_BACKUP_DIR = '/home/xxx/whisper_backup'
final_res = {}
#carbonate configuration file
carbonate_conf = os.path.join(os.getcwd(), 'zys_carbonate.conf')

#find metric's new hash location
def handle(root_dir):
    cmd_pattern = 'carbon-lookup -c {} {}'

    if os.path.isfile(root_dir) and root_dir.endswith('.wsp'):
        absoulte_path = root_dir
        metric_name = absoulte_path.split('.')[0]
        metric_name_list = metric_name.split('/')
        metric_name = ".".join(metric_name_list[5:])
        # print metric_name
        cmd = cmd_pattern.format(carbonate_conf, metric_name)
        # print cmd
        res = commands.getstatusoutput(cmd)
        host = res[1].split(':')[0]
        # print host
        if host not in final_res.keys():
            final_res[host] = [metric_name]
        else:
            final_res[host].append(metric_name)
        print 'handle ', metric_name, ' done'

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            absoulte_path = os.path.join(root, file)
            if absoulte_path.endswith(".wsp"):
                metric_name = absoulte_path.split('.')[0]
                metric_name_list = metric_name.split('/')
                metric_name = ".".join(metric_name_list[5:])
                #print metric_name
                cmd = cmd_pattern.format(carbonate_conf, metric_name)
                #print cmd
                res = commands.getstatusoutput(cmd)
                host = res[1].split(':')[0]
                #print host
                if host not in final_res.keys():
                    final_res[host] = [metric_name]
                else:
                    final_res[host].append(metric_name)
                print 'handle ', metric_name, ' done'


#scp whisper file to new hash location
def scp_file(key, filename_list):
    for filename in filename_list:
        #whisper storage dir
        prefix = '/data/whisper/'
        tmp_list = filename.split('.')
        true_name = '/'.join(tmp_list)
        true_name = true_name + '.wsp'
        true_name = os.path.join(prefix, true_name)
        cp_cmd = 'cp %s %s' % (true_name, filename)
        res = commands.getstatusoutput(cp_cmd)
        if res[0] != 0:
            print filename, ' cp error happend'
            continue
        scp_cmd = 'scp %s %s:%s' % (filename, HOST_IP[key], WHISPER_BACKUP_DIR)
        res = commands.getstatusoutput(scp_cmd)
        if res[0] != 0:
            print filename, ' scp error happend'
            continue
        rm_cmd = 'rm %s' % filename
        res = commands.getstatusoutput(rm_cmd)
        if res[0] != 0:
            print filename, ' rm error happend'
            continue
        print 'scp ', filename, ' done'


def main():
    if len(sys.argv) != 2:
        print 'please give the root path'
        return
    root_dir = os.path.abspath(sys.argv[1])
    print 'start find nodes at: ', time.ctime()
    handle(root_dir)
    print 'end find nodes at: ', time.ctime()
    print 'start scp at: ', time.ctime()
    for key in final_res.keys():
        print key+":"+HOST_IP[key]+":"
        print final_res[key]
        scp_file(key, final_res[key])
    print 'end scp at: ', time.ctime()


if __name__ == "__main__":
    main()