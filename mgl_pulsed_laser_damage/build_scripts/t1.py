import time, model, fem1d
for mname in ("Pennes","CV","MGT","MGL"):
    P=model.make(mname)
    des=dict(I0=3e5,tp=2.0,per=5.0,Np=4,tcool=20.0)
    t=time.time(); R=fem1d.run(P,des); m=fem1d.metrics(R)
    print(mname, round(time.time()-t,2), {k:(round(v,4) if isinstance(v,float) else v) for k,v in m.items()})
