import time, model, fem1d, lap
des=dict(I0=3e5,tp=2.0,per=5.0,Np=1,tcool=10.0)
xs=[0.0,0.002,0.004,0.006,0.010]
for mname in ("Pennes","MGL"):
    P=model.make(mname); P["cw"]=(0,0); P["thc"]=(1e6,1e6); P["tau1"]=1.0
    t=time.time()
    acc,full,half=lap.invert(P,des,xs,4.0,rscale=1e-4,N=1500)
    print(mname,round(time.time()-t,1))
    for r in acc: print([f"{v:.5g}" for v in r])
    R=fem1d.run(P,des,dx=1.25e-4,dt=0.02,Tend=4.0,keep=False)
    import bisect
    for x in xs:
        i=min(range(len(R.xs)),key=lambda k:abs(R.xs[k]-x)); print(x,R.th[-1][i])
