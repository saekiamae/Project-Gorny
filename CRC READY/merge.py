import numpy as np

def deParse(st):
    bfr=False
    abf=''
    nbf=''
    dpf=0
    outl=list()
    outn=list()
    outd=list()
    dep=0
    for c in st:
        if c.isupper():
            if bfr and dep<1:
                if nbf!='':
                    num=int(nbf)
                else:
                    num=1
                outl.append(abf)
                outn.append(num)
                outd.append(dpf)
                nbf=''
                abf=''
                dpf=0
            abf+=c
            bfr=True
        elif c.islower():
            abf+=c
        elif c.isdigit():
            if dep<1:
                nbf+=c
            else:
                abf+=c
        elif c=='(':
            if bfr and dep<1:
                if nbf!='':
                    num=int(nbf)
                else:
                    num=1
                outl.append(abf)
                outn.append(num)
                outd.append(dpf)
                nbf=''
                abf=''
                dpf=0
            bfr=True
            dep+=1
        elif c==')':
            dpf=dep
            dep-=1
            abf=reParse(deParse(abf))
        elif c=='·':
            if bfr and dep<1:
                if nbf!='':
                    num=int(nbf)
                else:
                    num=1
                outl.append(abf)
                outn.append(num)
                outd.append(dep)
                nbf=''
                abf=''
            dep=2
            dpf=2
    if nbf!='':
        num=int(nbf)
    else:
        num=1
    outl.append(abf)
    outn.append(num)
    outd.append(dpf)
    return [outl,outn,outd]

def reParse(out):
    out=list(zip(*out))
    out.sort(key=lambda row: row[0:])
    st=''
    for i in out:
        if i[2]==1:
            st+='('+i[0]+')'
        elif i[2]==0:
            st+=i[0]
        else:
            st+='·'+i[0]
        if i[1]!=1 and i[2]!=2:
            st+=str(i[1])
    return st

def prs(st):
    return reParse(deParse(st))

def eV(x):
    return str(float(x)*0.010364)
                
def main():            
    with open("raw_dip.csv",encoding="utf-8") as f:
        dip=list()
        for i in f:
            el=i.strip().split(',')
            el[1]=prs(el[1])
            dip.append(el) 
    with open("raw_dis.csv",encoding="utf-8") as f:
        dis=list()
        for i in f:
            el=i.strip().split(',')
            el[0]=prs(el[0])
            dis.append(el)
    with open("raw_ion.csv",encoding="utf-8") as f:
        ion=list()
        for i in f:
            el=i.strip().split(',')
            el[0]=prs(el[0])
            ion.append(el)
                
    with open("raw_magn.csv",encoding="utf-8") as f:
        magn=list()
        for i in f:
            el=i.strip().split(',')
            el[1]=prs(el[1])
            magn.append(el)
    with open("final.csv",encoding="utf-8",mode="w") as final:
        mlist=list()
        for io in ion:
            form=io[0]
            name=io[1]
            eion=eV(io[2])
            try:
                idx=dis[:][0].index(io[0])
                edis=eV(dis[idx][1])
                del dis[idx]
            except ValueError:
                edis=""
            try:
                idx=dip[:][1].index(io[0])
                mdip=dip[idx][2]
                del dip[idx]
            except ValueError:
                mdip=""
            try:
                idx=magn[:][1].index(io[0])
                msus=magn[idx][3]
                del magn[idx]
            except ValueError:
                msus=""
            mlist.append([form,name,eion,edis,mdip,msus])
        for di in dis:
            form=di[0]
            name=""
            eion=""
            edis=eV(di[1])
            try:
                idx=dip[:][1].index(io[0])
                name=dip[idx][0]
                mdip=dip[idx][2]
                del dip[idx]
            except ValueError:
                mdip=""
            try:
                idx=magn[:][1].index(io[0])
                name=dip[idx][0]
                msus=magn[idx][3]
                del magn[idx]
            except ValueError:
                msus=""
            mlist.append([form,name,eion,edis,mdip,msus])
        for dp in dip:
            form=dp[1]
            name=dp[0]
            eion=""
            edis=""
            mdip=dp[2]
            try:
                idx=magn[:][1].index(io[1])
                msus=magn[idx][3]
                del magn[idx]
            except ValueError:
                msus=""
            mlist.append([form,name,eion,edis,mdip,msus])
        for m in magn:
            form=m[1]
            name=m[0]
            eion=""
            edis=""
            mdip=""
            msus=m[3]
            mlist.append([form,name,eion,edis,mdip,msus])
        mlist.sort(key=lambda row: row[0:])
        for r in mlist:
            for el in r[:-1]:
                final.write(el+",")
            final.write(r[-1]+"\n")
main()
