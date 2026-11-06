import exact_uniform as E, model as M, fem, time
q=fem.Props().ratios(0.5); print(q)
t0=time.time()
a=E.invert(0.2,[0.3,0.8],q,0.02,0.05)
b=M.invert_line(M.Model(),("step",),[0.3,0.8],0.2,N=1200,nwynn=8)
print(time.time()-t0); print(a); print(b)
