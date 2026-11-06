import time, math, sys
import fem, model as M
from model import Model
pr=fem.Props(n=0)
nodes=fem.make_mesh(5.0,0.01,2.6,1.1)
S=fem.Solver(pr,nodes,p=1,a_src=0.05)
print(S.nn)
obs=[0.2,0.4,0.8,1.2]
t0=time.time()
res=S.run(0.0007,0.3,obs_r=obs,record_energy=True)
print('time',time.time()-t0)
dt=0.0007
mod=Model()
for k,r in enumerate(obs):
    H=fem.stress_from_S(res['hist'][k],dt,0.05)
    for t in (0.05,0.1,0.2,0.3):
        i=int(round(t/dt))
        ex=M.invert_line(mod,("step",),[r],t,N=1200,nwynn=8)[0]
        print(r,t,['%.4g'%x for x in H[i]],['%.4g'%x for x in ex])
for t,e in res['energy'][::100]:
    ex=(t-0.02*(1-math.exp(-t/0.02)))/(2*math.pi)
    print(t,e,ex)
