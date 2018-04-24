import struct
import telnetlib
import subprocess
import pty
import os
import time
import sys
import thread
from socket import *

def p4(x):
    return struct.pack("<L", x)

def p8(x):
    return struct.pack("<Q", x)

def up4(x):
    return struct.unpack("<L", x)[0]

def up8(x):
    return struct.unpack("<Q", x)[0]

class Pwnable:
    def __init__(self):
        self.sock = None
        self.proc = None
        self.isRemote = None

    def Connect(self, HOST, PORT):
        self.isRemote = True
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((HOST, PORT))

    def Process(self, command):
        self.isRemote = False
        args = command.split()
        self.master_fd, slave_fd = pty.openpty()
        self.proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=slave_fd, stderr=subprocess.STDOUT, close_fds=True)
        os.close(slave_fd)

    def Send(self, msg):
        if self.isRemote:
            self.sock.send(msg)
        else:
            self.proc.stdin.write(msg)
            self.proc.stdin.flush()

    def Sendline(self, msg):
        self.Send(msg + "\n")

    def Read(self, size):
        if self.isRemote:
            return self.sock.recv(size)
        else:
            time.sleep(0.01)
            return os.read(self.master_fd, size)

    def ReadUntil(self, chkStr):
        data = self.Read(len(chkStr))
        while not data.endswith(chkStr):
            tmp = self.Read(1)
            if not tmp: break
            data += tmp

        return data

    def Interact(self):
        if self.isRemote:
            t = telnetlib.Telnet()
            t.sock = self.sock
            t.interact()
        else:
            thread.start_new_thread(self.InteractRead, ())
            while True:
                self.Sendline(raw_input())

    def InteractRead(self):
        while True:
            sys.stdout.write(self.Read(65536))

    def Close(self):
        if self.isRemote:
            self.sock.close();
        else:
            os.close(self.master_fd)
