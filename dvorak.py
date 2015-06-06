str = "Ydco lprxn.m p.'gcp.o frgp o.bo.v Ln.ao. er frgp x.oy! C-nn er mf x.oy! /dcby= Yd. T.f frg ap. nrrtcbi urp co yd. bam.oat. ru ydco t.fxrapev"

str = str.lower()

dic = {'[':'-', ']':'=',
       "'":'q', ',':'w', '.':'e', 'p':'r', 'y':'t', 'f':'y', 'g':'u', 'c':'i', 'r':'o', 'l':'p', '/':'[', '=':']',
       'a':'a', 'o':'s', 'e':'d', 'u':'f', 'i':'g', 'd':'h', 'h':'j', 't':'k', 'n':'l', 's':';',
       ';':'z', 'q':'x', 'j':'c', 'k':'v', 'x':'b', 'b':'n', 'm':'m', 'w':',', 'v':'.', 'z':'/'}

decodeStr = ""

for i in str :
 if i in dic :
  decodeStr += dic[i]
 else :
  decodeStr += i

print decodeStr
