#!/usr/bin/python
# encoding: utf-8

import select
import os
import time

class VSPAgent(object):
    def __init__(self, path):
        self.port = os.open(path, os.O_RDWR)

    def get_free_mem(self):
        free = 0
        for line in open('/proc/meminfo'):
            var, value = line.strip().split()[0:2]
            if var in ('MemFree:', 'Buffers:', 'Cached:'):
                free += long(value)
        return free
        
    def run(self):
        rlist = [self.port]
        while True:
            readable, writable, exceptional = select.select(rlist, [], [], 2)
            if readable:
                data = os.read(self.port, 1024)
                if data == "free_mem":
                    os.write(self.port, "mem:%d" %(self.get_free_mem()))
                elif data == "shutdown":
                    os.write(self.port, "shutdown!")
                    time.sleep(3);
                    os.system("shutdown -h now")
                
if __name__ == "__main__":
    VSPAgent("/dev/virtio-ports/vspagent").run()
