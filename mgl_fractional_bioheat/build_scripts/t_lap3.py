import model, lap, time
p = model.make(h=0.2, alpha=1.0)
xs=[0.05,0.3,0.5]
for t in (0.2,0.4):
  for N,nw in ((4000,40),(8000,40),(16000,40),(16000,200)):
    acc,full,half=lap.invert(p,xs,t,N=N,nwynn=nw)
    print(t,N,nw, [["%.4f"%v for v in r[:3]] for r in acc])
