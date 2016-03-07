#! /usr/bin/env python

import sys
import paramiko
import time
from paramiko import SSHClient

try:
    demo = sys.argv[1]
    hostnames = sys.argv[2].split(',')
    url = "http://oob-mgmt-server.lab.local/cldemo-config/%s/"%demo
except:
    print("Usage: pushconfig [demo] [leaf01,leaf02,etc]")
    sys.exit(-1)

for host in hostnames:
    expect = paramiko.SSHClient()
    expect.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    expect.connect(host, username="cumulus", password="CumulusLinux!")
    stdin, stdout, stderr = expect.exec_command("sudo su", get_pty=True)
    for line in ['CumulusLinux!',
                 'wget %s/%s/interfaces'%(url, host),
                 'wget %s/%s/Quagga.conf'%(url, host),
                 'wget %s/%s/daemons'%(url, host),
                 'mv interfaces /etc/network/interfaces',
                 'mv Quagga.conf /etc/quagga/Quagga.conf',
                 'mv daemons /etc/quagga/daemons',
                 'reboot']:
        print("%s: %s"%(host, line))
        stdin.write('%s\n'%line)
        stdin.flush()
        time.sleep(2)
    expect.close()