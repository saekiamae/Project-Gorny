from collections import deque

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

name="raw_len";
with open("./"+name+".txt",encoding="utf-8") as r:
    with open("./"+name+".csv","w",encoding="utf-8") as w:
        for line in r:
            words=line.strip().replace(",","-").split(" ")
            if len(words)>1:
                nw=deque()
                sstr=''
                struct=True
                nw.append(words[0])
                for word in words[1:]:
                    if word=='(re)':
                        pass
                    elif word.find('—')>=0:
                        if struct:
                            struct=False
                            nw.append(sstr)
                        nw.append(word)
                    elif isfloat(word):
                        nw.append(word)
                    elif word.find('∠')>=0:
                        nw.append(word)
                    else:
                        if struct:
                            sstr+=word
                nline=''
                for i in list(nw)[0:-1]:
                    nline+=i+","
                nline+=nw[-1]
                w.write(nline+'\n')
