with open("abc.txt")as f:
    with open("abc.csv","w")as w:
        key=list()
        w1=list()
        w2=list()
        it=0
        for i in f:
            j=i.strip()
            it+=1
            if it<=18:
                key.append(j)
            elif it<=36:
                w1.append(j)
            else:
                w2.append(j)
        for i in range(len(key)):
            w.write(key[i]+","+w1[i]+","+w2[i]+"\n")
