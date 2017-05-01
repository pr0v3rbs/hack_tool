import struct
import telnetlib
from socket import *

class Pwnable:
    def __init__(self):
        self.sock = None

    def p4(self, x):
        return struct.pack("<L", x)

    def p8(self, x):
        return struct.pack("<Q", x)

    def up4(self, x):
        return struct.unpack("<L", x)[0]

    def up8(self, x):
        return struct.unpack("<Q", x)[0]

    def Connect(self, HOST, PORT):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect((HOST, PORT))

        return self.sock

    def Send(self, msg):
        self.sock.send(msg);

    def SendLine(self, msg):
        self.Send(msd + "\n")

    def Read(self, size):
        return self.sock.recv(size)

    def ReadUntil(self, chkStr):
        data = self.Read(len(chkStr))
        while not data.endswith(chkStr):
            tmp = self.Read(1)
            if not tmp: break
            data += tmp

        return data

    def Interact(self):
        t = telnetlib.Telnet()
        t.sock = self.sock
        t.interact()

    def Close(self):
        self.sock.close();
