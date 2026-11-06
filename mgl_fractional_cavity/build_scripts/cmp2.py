import mgl, fd_check
a=0.01; t=0.007; tau0=0.02; tau1=0.05
for dr in (0.0005,0.00025,0.000125):
    rn,th,un,srr,spp=fd_check.fd_sphere(a,tau0,tau1,t,dr=dr,rmax=0.12)
    rs=[a,0.02,0.03,0.04,0.05,0.07]
    acc,_,_=mgl.durbin(lambda s: mgl.sphere_fields(s,rs,a,1.0,tau0,tau1),t,4,len(rs),N=1000,nwynn=40)
    print('dr',dr)
    for i,r in enumerate(rs):
        j=int(round((r-a)/dr)); w=max(1,int(0.002/dr))
        lo=max(0,j-w); hi=j+w+1
        sm=lambda x: sum(x[lo:hi])/(hi-lo)
        print(f" {r:.3f} th {acc[i][0]:.4f}/{th[j]:.4f} u {acc[i][1]:.4e}/{un[j]:.4e} srr {acc[i][2]: .3e}/{sm(srr): .3e} spp {acc[i][3]: .3e}/{sm(spp): .3e} spp_raw {spp[j]: .3e}")
