import struct
import telnetlib
import subprocess
import pty
import os
from socket import *

class Pwnable:
    def __init__(self):
        self.sock = None
        self.proc = None
        self.isRemote = None

    def p4(self, x):
        return struct.pack("<L", x)

    def p8(self, x):
        return struct.pack("<Q", x)

    def up4(self, x):
        return struct.unpack("<L", x)[0]

    def up8(self, x):
        return struct.unpack("<Q", x)[0]

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

    def SendLine(self, msg):
        self.Send(msg + "\n")

    def Read(self, size):
        if self.isRemote:
            return self.sock.recv(size)
        else:
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
        else:   # TODO: Need to use non blocking I/O
            while True:
                self.Send(raw_input())
                print self.Read(65535)

    def Close(self):
        if self.isRemote:
            self.sock.close();
        else:
            os.close(self.master_fd)
