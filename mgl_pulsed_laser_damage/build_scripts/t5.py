import model, lap, cmath, math
des=dict(I0=3e5,tp=2.0,per=5.0,Np=1)
P=model.make("MGL"); P["cw"]=(0,0); P["thc"]=(1e6,1e6)
for k in range(0,1501):
    s=complex(1.5,k*math.pi/8)
    try: lap.solve_s(P,des,s,1e-4)
    except Exception as e:
        print(k,'fail'); L=lap.Layer(P,des,0,s,1e-4); print(L.q,L.vec); break
