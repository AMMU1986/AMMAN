import model, lap, fem, time, math, sys
alpha=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
p = model.make(h=0.2, alpha=alpha)
pts=[0.05*k for k in range(1,20)]
def ref(t):
    a,_,_=lap.invert(p,pts,t,N=3000,nwynn=40)
    return a
def err(R,t,a):
    n=int(round(t/R.dt))
    e={'th':0,'u':0,'sg':0};nr={'th':0,'u':0,'sg':0}
    xm,sg=fem.stress(R,n)
    for x,r in zip(pts,a):
        f=fem.at(R,n,x,'th'); e['th']+=(f-r[0])**2; nr['th']+=r[0]**2
        f=fem.at(R,n,x,'u'); e['u']+=(f-r[1])**2; nr['u']+=r[1]**2
    # sigma at midpoints near pts: compare using lap at midpoint
    return {k:math.sqrt(e[k]/nr[k]) for k in ('th','u')}
for t in (0.2,0.4):
    a=ref(t)
    for dx,dt in ((0.01,0.02),(0.005,0.01),(0.0025,0.005),(0.00125,0.0025)):
        R=fem.run(p,dx=dx,dt=dt,T=t)
        print(alpha,t,dx,dt,err(R,t,a))
