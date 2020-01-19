from collections import deque

name="raw_dis";
with open("./"+name+".txt",encoding="utf-8") as r:
    with open("./"+name+".csv","w",encoding="utf-8") as w:
        for line in r:
            words=line.replace(",","-").split(" ")
            if len(words)>1:
                nw=deque()
                nw.append(words[0])
                if words[1][0].isdigit():
                    nw.append(words[1])
                else:
                    nw.append(words[1][1:])
                nline=''
                for i in list(nw)[0:-1]:
                    nline+=i+","
                nline+=nw[-1]+'\n'
                w.write(nline)
