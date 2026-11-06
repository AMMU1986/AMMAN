import time, mgl, fd_check
a=0.01; t=0.007; tau0=0.02; tau1=0.05
rs=[a,0.015,0.02,0.03,0.04,0.05,0.055,0.06,0.07]
t0=time.time()
F=lambda s: mgl.sphere_fields(s,rs,a,1.0,tau0,tau1)
acc,_,_=mgl.durbin(F,t,4,len(rs),N=1000,nwynn=40)
acc2,_,_=mgl.durbin(F,t,4,len(rs),N=500,nwynn=40)
print('durbin',time.time()-t0)
t0=time.time()
rn,th,un,srr,spp=fd_check.fd_sphere(a,tau0,tau1,t)
print('fd',time.time()-t0)
for i,r in enumerate(rs):
    j=int(round((r-a)/0.0005))
    print(f"{r:.3f} th {acc[i][0]: .5e} {th[j]: .5e} | u {acc[i][1]: .4e} {un[j]: .4e} | srr {acc[i][2]: .4e} {srr[j]: .4e} | spp {acc[i][3]: .4e} {spp[j]: .4e} | conv {max(abs(acc[i][k]-acc2[i][k]) for k in range(4)):.1e}")
