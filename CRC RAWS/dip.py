from collections import deque

name="raw_dip";
with open("./"+name+".txt",encoding="utf-8") as r:
    with open("./"+name+".csv","w",encoding="utf-8") as w:
        for line in r:
            words=line.replace(",","-").split(" ")
            if len(words)>1:
                nw=deque()
                if words[-2]!="liq":
                    nw.appendleft(words[-2].split('(')[0])
                    end=2
                else:
                    nw.appendleft(words[-3].split('(')[0])
                    end=3
                end=end+1
                nw.appendleft(words[-end])
                rest=words[0]
                for i in words[1:-end]:
                    rest+=" "+i
                nw.appendleft(rest)
                nline="";
                for i in list(nw)[0:-1]:
                    nline+=i+","
                nline+=nw[-1]+'\n'
                w.write(nline)
