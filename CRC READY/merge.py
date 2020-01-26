from collections import deque

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

def prep(filename,idx,nn=False):
    with open(filename,encoding="utf-8") as f:
        out=dict()
        for i in f:
            el=i.strip().split(',')
            x=prs(el[idx])
            if nn:
                name=''
                out[x[0]]=[name,x[1]]+el[1:]
            else:
                name=el[not idx]
                out[x[0]]=[name,x[1]]+el[2:]
        return out

def getPr(m,d,lidx,en=False):
    for i in d.keys():
        lidd=deque(lidx)
        for j in d[i][2:]:
            try:
                m[i]
            except KeyError:
                m[i]=rawLn()
                m[i][0:2]=d[i][0:2]
            if en:
                j=eV(j)
            m[i][lidd.popleft()]=j
    return m

rawchar='X'

def rawLn():
    x=list()
    for i in range(50):
        x.append(rawchar)
    return x

def main():
    global elng
    elng=dict()
    with open("Electronegativity.csv",encoding="utf-8") as f:
        for i in f:
            j=i.split(',')
            elng[j[0]]=float(j[1])
    elng['D']=elng['H']
    elng['T']=elng['H']


    dip=prep("raw_dip.csv",1)
    dis=prep("raw_dis.csv",0,True)
    ion=prep("raw_ion.csv",0)
    magn=prep("raw_magn.csv",1)
  
    mdict=dict()
    ionk=[10]
    dipk=[20]
    magnk=[49,21]
    disk=[30]
    lenk=[31]
    vark=[4,5]
    freqk=[23]
    
    mdict['idx']=sorted([0,1]+ionk+dipk+magnk+disk+lenk+vark+freqk)
    mdict=getPr(mdict,ion,ionk,True)
    mdict=getPr(mdict,dip,dipk)
    mdict=getPr(mdict,magn,magnk)
    mdict=getPr(mdict,dis,disk,True)


    nistion=dict()
    nistdip=dict()
    
    with open("Ionisation.csv",encoding="utf-8") as f:
        for i in f:
            j=i.split(',')
            if j[3]!='':
                nistion[prs(j[2])[0]]=-float(j[3])
            else:
                nistion[prs(j[2])[0]]=-float(j[4])
        
    for i in nistion.keys():
        try:
            if mdict[i][ionk[0]]==rawchar:
                mdict[i][ionk[0]]=nistion[i]
        except KeyError:
            pass
    
    with open("Dipoles.csv",encoding="utf-8") as f:
        for i in f:
            j=i.split(',')
            nistdip[prs(j[2])[0]]=float(j[3])

    for i in nistdip.keys():
        try:
            if mdict[i][dipk[0]]==rawchar:
                mdict[i][dipk[0]]=nistdip[i]
        except KeyError:
            pass


    ab=dict()

    with open("AB.csv",encoding="utf-8") as f:
        for i in f:
            j=i.strip().split(',')
            if j[0]!='':
                ab[prs(j[0])[0]]=j[1:]
                name=prs(j[0])[0]
            else:
                ab[name]=j[1:]
                
    for i in ab.keys():
        try:
            mdict[i]
        except KeyError:
            mdict[i]=rawLn()
            mdict[i][0:2]=['',2]
        if mdict[i][ionk[0]]==rawchar:
            mdict[i][ionk[0]]=ab[i][14]
        if mdict[i][dipk[0]]==rawchar:
            mdict[i][dipk[0]]=ab[i][9]
        if mdict[i][disk[0]]==rawchar:
            mdict[i][disk[0]]=ab[i][8]
        if mdict[i][lenk[0]]==rawchar:
            mdict[i][lenk[0]]=ab[i][7]
        if mdict[i][vark[0]]==rawchar:
            mdict[i][vark[0]]=ab[i][5]
        if mdict[i][vark[1]]==rawchar:
            mdict[i][vark[1]]=ab[i][6]       


    freq=dict()
    with open("freq.csv",encoding="utf-8") as f:
        for i in f:
            j=i.strip().split(',')
            if int(j[1])==0:
                form=prs(j[2])[0]
                try:
                    freq[form]
                except KeyError:
                    if j[5]!='':
                        freq[form]=j[5]
                        
    for i in freq.keys():
        try:
            if mdict[i][freqk[0]]==rawchar:
                mdict[i][freqk[0]]=freq[i]
        except KeyError:
            pass


    freq2=dict()
    with open("raw_freq.csv",encoding="utf-8") as f:
        for i in f:
            j=i.strip().split(',')
            form=prs(j[0])[0]
            try:
                freq2[form]
            except KeyError:
                freq2[form]=j[1]
                    
                        
    for i in freq2.keys():
        try:
            if mdict[i][freqk[0]]==rawchar:
                mdict[i][freqk[0]]=freq[i]
        except KeyError:
            pass
        
        
    with open("final.csv",encoding="utf-8",mode="w") as final:
        for key in sorted(mdict.keys()):
            val=mdict[key]
            if key!='idx':
                st=key
                it=0
                mis=0
                for el in val:
                    if el!=rawchar or it in mdict['idx']:
                        st+=","+str(el)
                    if it in ionk or it in disk or it in dipk or it in magnk:
                        if el==rawchar:
                            if it in magnk:
                                mis+=0.5
                            else:
                                mis+=1
                    it+=1
                if 1<int(val[1])<3 and mis<2:
                    final.write(st+"\n")
main()
