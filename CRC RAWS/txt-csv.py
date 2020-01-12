from collections import deque

name="raw_magn";
with open("./"+name+".txt",encoding="utf-8") as r:
    with open("./"+name+".csv","w",encoding="utf-8") as w:
        for line in r:
            words=line.split(" ")
            if len(words)>1:
                nw=deque()
                nw.appendleft(words[-1])
                nw.appendleft(words[-2])
                nw.appendleft(words[-3])
                rest=""
                for i in words[0:-4]:
                    rest+=i+" "
                rest+=words[-4]
                nw.appendleft(rest)
                nline="";
                for i in list(nw)[0:-1]:
                    nline+=i+","
                nline+=nw[-1]
                w.write(nline)
