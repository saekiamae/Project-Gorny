import numpy as np

def deParse(st):
    bfr=False
    dep=0
    out=list()
    v=dict()
    for i in range(5):
        out.append(list())
       
    def clear():
        v['a']=''
        v['n']=''
        v['d']=0
        v['m']=1

    def apply():
        if v['n']!='':
            num=int(v['n'])
        else:
            num=1
        out[0].append(v['a'])
        out[1].append(num)
        out[2].append(v['d'])
        out[3].append(v['m'])
        out[4].append(val(v['a'],v['m'],v['d']))

    clear()
    
    for c in st:
        if c.isupper():
            if bfr and dep<1:
                apply()
                clear()
            v['a']+=c
            bfr=True
        elif c.islower():
            v['a']+=c
        elif c.isdigit():
            if dep<1:
                v['n']+=c
            else:
                v['a']+=c
        elif c=='(':
            if bfr and dep<1:
                apply()
                clear()
            bfr=True
            dep+=1
        elif c==')':
            v['d']=dep
            dep-=1
            x=reParse(deParse(v['a']))
            v['a']=x[0]
            v['m']=x[1]
            
        elif c=='·':
            if bfr and dep<1:
                clear()
                apply()
            dep=2
            v['d']=2
    apply()
    return out
    
def reParse(outr):
    out=list(zip(*outr))       
    numout=0
    for i,j in zip(outr[1],outr[3]):
        numout+=i*j
    out.sort(key=lambda row: row[4:])
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
    return [st,numout]

def val(a,m,d):
    if m==1 and d!=2:
        try:
            return elng[a]
        except KeyError as e:
            print(e)
            return 100
    elif d==2:
        return 1000
    else:
        return 5

def prs(st):
    return reParse(deParse(st))

def eV(x):
    return str(float(x)*-1*0.010364)

def cl(matrix, i):
    return [row[i] for row in matrix]

def prep(filename,idx):
    lst=list()
    with open(filename,encoding="utf-8") as f:
        for i in f:
            el=i.strip().split(',')
            x=prs(el[idx])
            el[idx]=x[0]
            el.append(str(x[1]))
            lst.append(el)
    return lst

def main():
    global elng
    elng=dict()
    with open("Electronegativity.csv",encoding="utf-8") as f:
        for i in f:
            j=i.split(',')
            elng[j[0]]=float(j[1])
    elng['D']=elng['H']
    elng['T']=elng['H']
    nistion=dict()
    nistdip=dict()
    with open("Dipoles.csv",encoding="utf-8") as f:
        for i in f:
            j=i.split(',')
            nistdip[prs(j[2])[0]]=float(j[3])
    with open("Ionisation.csv",encoding="utf-8") as f:
        for i in f:
            j=i.split(',')
            if j[3]!='':
                nistion[prs(j[2])[0]]=float(j[3])
            else:
                nistion[prs(j[2])[0]]=float(j[4])
    dip=prep("raw_dip.csv",1)
    dis=prep("raw_dis.csv",0)
    ion=prep("raw_ion.csv",0)
    magn=prep("raw_magn.csv",1)
    with open("final.csv",encoding="utf-8",mode="w") as final:
        mlist=list()
        for i in ion:
            form=i[0]
            name=i[1]
            eion=eV(i[2])
            try:                
                idx=cl(dis,0).index(i[0])
                edis=eV(dis[idx][1])
                del dis[idx]
            except ValueError:
                edis=""
            try:
                idx=cl(dip,1).index(i[0])
                mdip=dip[idx][2]
                del dip[idx]
            except ValueError:
                mdip=""
            try:
                idx=cl(magn,1).index(i[0])
                msus=magn[idx][3]
                msu=magn[idx][2]
                del magn[idx]
            except ValueError:
                msus=""
                msu=""
            mlist.append([form,name,i[-1],eion,mdip,msu,msus,edis])
        for i in dis:
            form=i[0]
            name=""
            eion=""
            edis=eV(i[1])
            try:
                idx=cl(dip,1).index(i[0])
                name=dip[idx][0]
                mdip=dip[idx][2]
                del dip[idx]
            except ValueError:
                mdip=""
            try:
                idx=cl(magn,1).index(i[0])
                name=magn[idx][0]
                msus=magn[idx][3]
                msu=magn[idx][2]
                del magn[idx]
            except ValueError:
                msus=""
                msu=""
            mlist.append([form,name,i[-1],eion,mdip,msu,msus,edis])
        for i in dip:
            form=i[1]
            name=i[0]
            eion=""
            edis=""
            mdip=i[2]
            try:
                idx=cl(magn,1).index(i[1])
                name=magn[idx][0]
                msus=magn[idx][3]
                msu=magn[idx][2]
                del magn[idx]
            except ValueError:
                msus=""
                msu=""
            mlist.append([form,name,i[-1],eion,mdip,msu,msus,edis])
        for i in magn:
            form=i[1]
            name=i[0]
            eion=""
            edis=""
            mdip=""
            msus=i[3]
            msu=i[2]
            mlist.append([form,name,i[-1],eion,mdip,msu,msus,edis])
        mlist.sort(key=lambda row: row[0:])
        for r in mlist:
            if r[3]=="" and r[0] in nistion.keys():
                r[3]=str(nistion[r[0]])
            if r[4]=="" and r[0] in nistdip.keys():
                r[3]=str(nistdip[r[0]])
            if 1<int(r[2])<4:
                for el in r[:-1]:
                    final.write(el+",")
                final.write(r[-1]+"\n")
main()
