import cmath, math, mgl
t=0.007
for N,nw in [(200,20),(400,30),(1000,40),(2000,40)]:
    F=lambda s: [(1/s,), (cmath.exp(-0.01*cmath.sqrt(s))/s,), (cmath.exp(-0.03*cmath.sqrt(s))/s,),(cmath.exp(-0.005*s)/s,),(cmath.exp(-0.0069*s)/s,),(cmath.exp(-0.0071*s)/s,), (cmath.exp(-0.003*s)/s**2,)]
    acc,f,h=mgl.durbin(F,t,1,7,N=N,nwynn=nw)
    print(N,nw,[round(x[0],7) for x in acc])
print(math.erfc(0.01/(2*math.sqrt(t))),math.erfc(0.03/(2*math.sqrt(t))), 0.004)
