import time, math
import fem, mgl
pr=fem.Props(law="power",n=1.0,Lg=1.0,phi0=0.2)
nodes=fem.make_mesh(3.2,0.01,2.6,1.1)
S=fem.Solver(pr,nodes,p=1,a_src=0.05)
dt=0.0005
obs=[0.3,0.8]
t0=time.time()
res=S.run(dt,0.3,obs_r=obs,snap_t=(0.1,0.2),sample_r=[0.2,0.5,1.0],record_energy=True)
print('t',time.time()-t0)
for k in range(2):
    for t in (0.1,0.2,0.3):
        print(obs[k],t,['%.4g'%x for x in res['hist'][k][int(round(t/dt))]])
print(res['snaps'][0.2])
for t,e in res['energy'][::200]:
    print(t,e,(t-0.02*(1-math.exp(-t/0.02)))/(2*math.pi))
# Laplace
ob=[S.locate(r) for r in obs]
for t in (0.1,0.2):
    t0=time.time()
    res2=mgl.durbin(lambda s: fem.laplace_fields(S,s,ob),t,4,2,N=500,ct=6.0,Tfac=2.0,nwynn=8)[0]
    print(t,time.time()-t0,[['%.4g'%x for x in r] for r in res2])
