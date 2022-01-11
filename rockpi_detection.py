#coding=utf-8
import paramiko
import paramiko.client as pc
import argparse
import socket
import subprocess
import time
import sys 
from time import gmtime, strftime
import os

hosts = ["10.214.211.107","10.214.211.109","10.214.211.111","10.214.211.159","10.214.211.61", "10.214.211.67", "10.82.65.175", "10.82.65.176"]
client = pc.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def get_parser():
    parser = argparse.ArgumentParser(description="Show rockpi system states ")
    parser.add_argument("--host", type=str, help="host ips", nargs='*')
    parser.add_argument("--port", type=int, help="port", default=22)
    parser.add_argument("--username", type=str, help="username", required=True)
    parser.add_argument("--password", type=str, help="password", required=True)
    return parser

def ping_host(ip, f_handler):
    res = subprocess.run(['ping', '-c2', '-w10', ip], stdout=subprocess.PIPE)
    # 将输出标准流解码成中文
    output = res.stdout.decode('gbk')
    # ping通代码为0
    if res.returncode == 0:
        f_handler.write('ping %-20s%-20s\n' % (ip, 'success'))
        # # ping通结果写入文本
        # with open('ping_success.txt', 'a+') as f:
        #     f.write('%-20s%-20s' % (ip, 'success'))
        # # ping执行结果写入文本
        # with open('ping_result.txt', 'a+') as f:
        #     f.write(output)
        #     f.write('-'*50)
        return True
    # ping不通代码为1
    else:
        f_handler.write('ping %-20s%-20s\n' % (ip, 'failure'))
        # # ping不通结果写入文本
        # with open('ping_failure.txt', 'a+') as f:
        #     f.write('%-20s%-20s' % (ip, 'success'))
        # # ping执行结果写入文本
        # with open('ping_result.txt', 'a+') as f:
        #     f.write(output)
        #     f.write('-' * 50)
        return False

def show_state(host, port, username, password, f_handler):
    f_handler.write("================================================================================\n")
    f_handler.write(host)
    f_handler.write("\n\n")
    try:
        res = ping_host(host, f_handler)
        f_handler.write("\n")
    except Exception as e:
        f_handler.write(repr(e) + "\n")

    if res:
        try:
            client.connect(host, port = port, username=username, password=password, timeout=1)
            stdin, stdout, stderr = client.exec_command('date')
            for line in stdout.readlines():
                f_handler.write(line)
                f_handler.write("\n")
            # stdin, stdout, stderr = client.exec_command('vmstat')
            # for line in stdout.readlines():
            #     f_handler.write(line)
            # f_handler.write("\n")
            stdin, stdout, stderr = client.exec_command('top -b -n1 | head -17')
            for line in stdout.readlines():
                f_handler.write(line)
        except Exception as e:
            f_handler.write(repr(e) + "\n")
            
        finally:
            client.close()
    


    f_handler.write("================================================================================\n")

def main(fname, fname_write):
    args = get_parser().parse_args()
    if args.host is None:
        args.host = hosts

    cnt = 0
    while True:
        f_handler = open(fname_write, 'w', buffering=1)

        for h in args.host:
            show_state(h, args.port, args.username, args.password, f_handler)
        f_handler.flush()
        os.fsync(f_handler)
        f_handler.close()
        os.rename(fname_write, fname)
        cnt += 1
        curtime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print("{}: {}".format(curtime, cnt))
        time.sleep(30)

fname = "states.txt"
fname_write = "states_new.txt"

if __name__ == "__main__":
    main(fname, fname_write)
