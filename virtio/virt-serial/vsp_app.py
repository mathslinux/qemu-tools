#!/usr/bin/python
# encoding: utf-8

import socket
import time

class VSPApp(object):
    def __init__(self, path):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(path)

    def run(self):
        count = 0
        while True:
            time.sleep(1)
            count += 1
            self.sock.send("free_mem")
            data = self.sock.recv(1024)
            if data:
                print data
            else:
                # peer close the socket
                print "peer close the socket, exit!!!"
                break
            if count >= 10:
                self.sock.send("shutdown")
            
if __name__ == "__main__":
    VSPApp("/tmp/vspagent").run()
