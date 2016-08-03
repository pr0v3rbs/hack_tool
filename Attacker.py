import struct
import telnetlib
import shellcodelib
import time
from socket import *

p8 = lambda x : struct.pack("<L", x)
p16 = lambda x : struct.pack("<Q", x)
up8 = lambda x : struct.unpack("<L", x)[0]
up16 = lambda x : struct.unpack("<Q", x)[0]

def ReadUntil(s, chkStr) :
    data = s.recv(len(chkStr))
    while not data.endswith(chkStr) :
        tmp = s.recv(1)
        if not tmp: break
        data += tmp

    return data

HOST = "hack.me"
PORT = 1234

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

#exploit!

t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
