import mgl, compute_all as c, math
VW=1/math.sqrt((1+mgl.EPS)*0.02)
cases=[("sphere",t,1.0,0.05) for t in (0.005,0.007,0.009)]+[("sphere",0.007,a,0.05) for a in (0.5,0.75,0.9)]+[("sphere",0.007,1.0,0.03),("sphere",0.007,1.0,0.08),("cylinder",0.007,1.0,0.05)]
for g,t,al,t1 in cases:
    rs=c.grid(321 if g=="sphere" else 161)
    f=mgl.sphere_fields if g=="sphere" else mgl.cylinder_fields
    F=lambda s: f(s,rs,c.A,al,c.TAU0,t1)
    A,_,_=mgl.durbin(F,t,4,len(rs),N=4000,nwynn=60); B,_,_=mgl.durbin(F,t,4,len(rs),N=2000,nwynn=60)
    rw=c.A+VW*t; dr=rs[1]-rs[0]
    fails=[(rs[i],k) for i in range(len(rs)) for k in range(4) if abs(A[i][k]-B[i][k])>1e-6*abs(A[i][k])]
    far=max([abs(r-rw) for r,k in fails if r>c.A+1e-12] or [0])
    mx=[max(abs(A[i][k]) for i in range(len(rs))) for k in range(4)]
    outside=max([abs(A[i][k]-B[i][k])/mx[k] for i in range(len(rs)) for k in range(4) if abs(rs[i]-rw)>2.01*dr] )
    print(g,t,al,t1,len(fails),"wall fails",[k for r,k in fails if r<c.A+1e-12],"max dist from front %.4f"%far,"max rel-to-max change outside 2dr %.1e"%outside)
