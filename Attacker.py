import struct
import telnetlib
from socket import *

p8 = lambda x : struct.pack("<L", x)
p16 = lambda x : struct.pack("<Q", x)

def ReadUntil(s, chkStr, isPrint = True) :
    chkLen = len(chkStr)
    data = s.recv(1)
    while True :
        while data[-1] != chkStr[0] :
            data += s.recv(1)
        tem = s.recv(chkLen - 1)
        data += tem
        # tem possible part of chkStr
        # need to fix
        if tem == chkStr[1:] :
            break
        
    if isPrint :
        print data

HOST = "hack.me"
PORT = 1234

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))

#exploit!

t = telnetlib.Telnet()
t.sock = s
t.interact()

s.close()
