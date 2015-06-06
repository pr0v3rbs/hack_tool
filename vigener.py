import string
alpha = string.ascii_lowercase

cipher = "xbv jvak cj nojycjpknh-wrqzuw"
key = 'eureka'
keyIdx = 0
decodeStr = ''

for i in cipher :
    if i not in alpha :
        decodeStr += i
        continue
    temKey = 26 - alpha.find(key[keyIdx])
    decodeStr += alpha[(alpha.find(i) + temKey) % 26]
    keyIdx = (keyIdx + 1) % 6
    
print decodeStr
