import json
R=json.load(open('results.json'))
f=lambda l:['%.3g'%x for x in l]
for k,v in R['valid'].items():
    print(k,{a:(f(b) if isinstance(b,list) and not isinstance(b[0],list) else b) for a,b in v.items()})
print('lap',[f(x) for x in R['laplace_L2']])
for r in R['reg']: print(r[0],f(r[1]),f(r[2]))
for k,v in R['conv'].items():
    if isinstance(v,list): print(k,f(v)); continue
    print(k,v.get('nn'),v.get('dt'),f(v['hist']) if 'hist' in v else '', f(v['prof']) if 'prof' in v else '', '%.1f'%v['cpu'])
for k,v in R['cases'].items(): print(k,'%.2g'%v['energy_err'],'%.1f'%v['cpu'],f(v['cmp'][0][-1]),f(v['cmp'][1][-1]))
print(R['travel'])
