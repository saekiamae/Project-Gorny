from collections import deque

name="diss2";
with open("./"+name+".txt",encoding="utf-8") as r:
    with open("./"+name+".csv","w",encoding="utf-8") as w:
        for line in r:
            words=line.replace(",","-").split(" ")
            if len(words)>2:
                print("ERR:"+line)
            elif len(words)>1:
                nw=deque()
                test=words[0].split("9")
                if len(test)>2:
                    print("ERR:",line)
                else:
                    nw.append("&".join(test))
                    nw.append(words[1])
                    nline="";
                    for i in list(nw)[0:-1]:
                        nline+=i+","
                    nline+=nw[-1]
                    w.write(nline)

