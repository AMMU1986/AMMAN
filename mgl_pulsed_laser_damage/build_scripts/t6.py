import time, opt, math, sys
from multiprocessing import Pool
if __name__=="__main__":
    with Pool(8) as p:
        for name,ov in (("MGL",{}),("MGL",{"normal_as_tumour":True})):
            t=time.time(); r=opt.run_case(p,name,ov,nps=(1,2,4,8,12),nstart=1)
            b=r["best"]; m=b["m"]
            print(name,ov,round(time.time()-t),'nev',r["nev"])
            print({k:round(v,4) for k,v in b["des"].items()}, b["v"])
            print('Tmax C',m["Tmax"]-273.15,'sabs',m["sabs"],'minOm',m["minOmT"],'JO mm',m["JO"]*1e3,'JF',m["JF"]*1e3,'OmN_h',m["OmN_h"],'dd',m['dd'],'J',b["J"])
            for q in r["per_np"]: print(' Np',q["Np"],round(q["J"],4),[round(a,3) for a in q["v"]],round(q["des"]["I0"]),round(q["des"]["tp"],2),round(q["des"]["per"],2))
