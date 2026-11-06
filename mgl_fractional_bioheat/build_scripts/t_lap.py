import model, lap, time
p = model.make(h=0.2, alpha=1.0)
xs=[0.05,0.1,0.2,0.3,0.5]
for t in (0.05,0.1,0.2,0.4):
    t0=time.time()
    acc,full,half=lap.invert(p,xs,t,N=2000,nwynn=30)
    print(t, round(time.time()-t0,1))
    for x,a,f,h_ in zip(xs,acc,full,half): print(' ',x,["%.5f"%v for v in a[:3]],["%.5f"%v for v in f[:3]],["%.5f"%v for v in h_[:3]])
