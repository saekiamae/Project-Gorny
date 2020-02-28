from collections import deque
import json

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
    
    buff=dict()
    for i in out:
        try:
            buff[i[0]][0]+=i[1]
        except KeyError:
            buff[i[0]]=[i[1],i[2:]]
    out=list()
    for i in buff.keys():
        out.append([i,buff[i][0]]+list(buff[i][1]))
    
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


def load(filename,keys,nameidx=0,validx=1,name=False,en=False,neg=False,nist=False,mod=False,mods=False,adrx=[],freqcheck=False,var2=False,src=""):
    with open(filename,encoding="utf-8") as f:
        for i in f:
            molecule=dict()
            el=i.strip().split(',')
            x=prs(el[nameidx])
            key=x[0]
            vals=el[validx:]
            skip=False
            
            if nist:
                if el[3]!='':
                    vals=[el[3]]
                else:
                    vals=[el[4]]

            if adrx:
                vals=list()
                for u in adrx:
                    vals.append(el[u])

            if freqcheck:
                if float(el[1])!=0:
                    skip=True
                    
            molecule['atcnt']=x[1]
            
            if name:
                molecule['name']=el[not nameidx]
               
            it=0

            if not skip:
                for i in keys:
                    if vals[it]!='':
                        try:
                            mdict[key]
                        except KeyError:
                            mdict[key]=molecule
                        if i=="X":
                            lkey=el[nameidx]
                        else:
                            lkey=i
                        try:
                            mdict[key][lkey]
                        except KeyError:
                            if en:
                                mdict[key][lkey]=eV(vals[it])
                            elif neg:
                                mdict[key][lkey]=-float(vals[it])
                            elif var2:
                                mdict[key][lkey]="{"+str(vals[it])+","+str(vals[it+1])+"}"
                                break
                            else:
                                mdict[key][lkey]=vals[it]
                            mdict[key][lkey+"_src"]=src
                    it+=1
                if mod:                
                    for n in range(2,len(el),2):
                        mdict[key][el[n]]=el[n+1]
                if mods:                
                    for n in range(1,len(el)):
                        mdict[key][el[n]]=el[n+1]

def main():
    global elng,mdict
    elng=dict()
    mdict=dict()
    
    with open("Electronegativity.csv",encoding="utf-8") as f:
        for i in f:
            j=i.split(',')
            elng[j[0]]=float(j[1])
    elng['D']=elng['H']
    elng['T']=elng['H']
    
    load("raw_dip.csv",['dip'],nameidx=1,validx=2,name=True,src="CRC")
    load("raw_dis.csv",['dis'],en=True,src="CRC")
    load("raw_ion.csv",['ion'],neg=True,validx=2,name=True,src="CRC")
    load("raw_magn.csv",['state','magn'],nameidx=1,validx=2,name=True,src="CRC")
    load("Ionisation.csv",['ion'],nameidx=2,neg=True,nist=True,src="NIST")
    load("Dipoles.csv",['dip'],nameidx=2,nist=True,src="NIST")
    load("raw_len.csv",['str'],mod=True,src="CRC")
    load("addlen.csv",['simlen'],src="NIST")
    load("diss2.csv",["X"],en=True,src="LANGE")
    load("var2.csv",["X"],var2=True,src="NIST")
    load("addvar.csv",['leftv','rightv'],src="NIST")
    load("AB.csv",['leftv','rightv','simlen','dis','dip','ion'],adrx=[6,7,8,9,10,15],src="ADR")
    load("freq.csv",['freq'],nameidx=2,validx=5,freqcheck=True,src="NIST")
    load("raw_freq.csv",['freq'],src="CRC")
        
    with open("../Molecules v5/data.json",encoding="utf-8",mode="w") as final:
        final.write(json.dumps(mdict))
main()
