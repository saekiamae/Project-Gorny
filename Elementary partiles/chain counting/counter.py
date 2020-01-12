q1=-1/3
q2=2/3

def g(x):
    return "%.4f" % x

for n in range(60):
    #in case of opposite charges:
    if q1*q2<0:
        rd=1/(2*n+1)

        #counting dc
        dc=0
        if n>0:
            for i in range(1,2*n-1+1):
                dc+=(-1)**i*(1/9)*(2*n-i)/(i*rd)

        #counting dtc
        dtc=0
        if n>0:
            for i in range(1,2*n+1):
                dtc+=(-1)**i*(1/3)*(abs(q1)+abs(q2))/(i*rd)

    else:
        rd=1/(2*n+2)

        #counting dc
        dc=0
        if n>0:
            for i in range(1,2*n+1):
                dc+=(-1)**i*(1/9)*(2*n-i+1)/(i*rd)

        #counting dtc
        dtc=0
        if n>0:
            for i in range(1,2*n+1+1):
                dtc+=(-1)**i*(1/3)*(abs(q1)+abs(q2))/(i*rd)

    #counting dt
    dt=q1*q2
    
    print("n:",n,"rd:",g(rd),"d:",g(dc+dtc+dt),"dc:",g(dc),"dtc:",g(dtc),"dt:",g(dt))
        
