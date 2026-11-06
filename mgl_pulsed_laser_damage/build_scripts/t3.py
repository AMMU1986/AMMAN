import random, math, time, model, fem1d
from multiprocessing import Pool
def ev(x):
    I0,tp,du,Np=x
    per=tp/du
    P=model.make("MGL")
    des=dict(I0=I0,tp=tp,per=per,Np=Np,tcool=30.0)
    R=fem1d.run(P,des,dt=0.1); m=fem1d.metrics(R)
    return x,per,m
if __name__=="__main__":
    random.seed(1)
    xs=[]
    while len(xs)<400:
        I0=math.exp(random.uniform(math.log(3e4),math.log(6e5))); tp=math.exp(random.uniform(math.log(0.2),math.log(8)))
        du=random.uniform(0.15,1.0); Np=random.randint(1,12)
        if Np*tp/du>60: continue
        xs.append((I0,tp,du,Np))
    t=time.time()
    with Pool(8) as p: out=p.map(ev,xs)
    print(time.time()-t)
    ok=[o for o in out if o[2]['minOmT']>=math.log(100) and o[2]['Tmax']<373.15]
    print(len(ok))
    ok.sort(key=lambda o:o[2]['JO'])
    for x,per,m in ok[:12]: print([round(v,3) for v in x],round(per,2),round(m['Tmax']-273.15,1),round(m['sabs']/1e3,1),'JO',m['JO']*1e3,'JF',m['JF']*1e3,'OmNmax',round(m['OmN_max'],2),round(m['OmT_h'],1))
    print('---')
    for x,per,m in ok[-5:]: print([round(v,3) for v in x],round(per,2),round(m['Tmax']-273.15,1),round(m['sabs']/1e3,1),'JO',m['JO']*1e3,'OmNmax',round(m['OmN_max'],2))
    print(min(o[2]['sabs'] for o in ok)/1e3)
