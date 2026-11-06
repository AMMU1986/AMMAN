import model, lap, fem, time
p = model.make(h=0.2, alpha=1.0)
t0=time.time()
R=fem.run(p,dx=0.005,dt=0.01,T=0.4)
print('fem',time.time()-t0)
xs=[0.05,0.1,0.2,0.3,0.5]
for tt in (0.1,0.2,0.4):
    n=int(round(tt/0.01))
    acc,_,_=lap.invert(p,xs,tt,N=3000,nwynn=40)
    xm,sg=fem.stress(R,n)
    accs,_,_=lap.invert(p,[x+0.0025 for x in xs],tt,N=3000,nwynn=40)
    for x,a,s_ in zip(xs,acc,accs):
        i=min(range(len(xm)),key=lambda k:abs(xm[k]-(x+0.0025)))
        print(tt,x,"th %.4f/%.4f u %.5f/%.5f sig %.4f/%.4f"%(fem.at(R,n,x,'th'),a[0],fem.at(R,n,x,'u'),a[1],sg[i],s_[2]))
