import model, fem1d
P=model.make("MGT"); P["kstar_lit"]=False;P["arr"][0]["A"]=0; P["arr"][1]["A"]=0
des=dict(I0=3e5,tp=2.0,per=5.0,Np=4,tcool=20.0)
R=fem1d.run(P,des,Tend=3,keep=False)
for n in range(0,31,3): print(n, [round(v,3) for v in R.th[n][:4]])
