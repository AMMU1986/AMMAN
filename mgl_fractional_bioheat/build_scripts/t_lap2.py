import model, lap, time
p = model.make(h=0.2, alpha=1.0)
xs=[0.05,0.3,0.5]
for t in (0.2,0.4):
  for N in (4000,16000,48000):
    t0=time.time()
    acc,full,half=lap.invert(p,xs,t,N=N,nwynn=0)
    print(t,N, round(time.time()-t0,1), [["%.4f"%v for v in r[:3]] for r in full])
