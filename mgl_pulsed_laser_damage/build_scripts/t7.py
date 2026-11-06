import opt, fem1d, time
des=dict(I0=1.62e5,tp=4.66,per=4.87,Np=3,tcool=120.0-3*4.87)
for dt in (0.8,0.4,0.2,0.1,0.05):
    t=time.time(); P,R,m=opt.evaluate("MGL",{},des,dt=dt); print(dt,round(time.time()-t,2),m['minOmT'],m['OmN_h'],m['JO'],m['JF'],m['Tmax'],m['sabs'])
