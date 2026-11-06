import fem, mgl, time
pr=fem.Props(n=1.0,phi0=0.2)
nodes=fem.make_mesh(3.2,0.0125,2.5,1.1)
S=fem.Solver(pr,nodes,p=2,a_src=0.05)
ob=[S.locate(0.3)]
for N,ct,Tf in ((600,6,2),(1500,6,2),(1500,8,2),(3000,6,3)):
    t0=time.time()
    r=mgl.durbin(lambda s: fem.laplace_fields(S,s,ob),0.3,4,1,N=N,ct=ct,Tfac=Tf,nwynn=8)
    print(N,ct,Tf,['%.5g'%x for x in r[0][0]],['%.5g'%x for x in r[1][0]],time.time()-t0)
res=S.run(0.0005,0.3+0.001,obs_r=[0.3])
print(['%.5g'%x for x in res['hist'][0][600]])
res=S.run(0.00025,0.3+0.001,obs_r=[0.3])
print(['%.5g'%x for x in res['hist'][0][1200]])
