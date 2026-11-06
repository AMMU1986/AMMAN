import cmath, math, mgl
for x,k0,k1 in [(1,0.4210244382,0.6019072302),(2,0.1138938727,0.1398658818),(5,3.691098334e-3,4.044613445e-3)]:
    a,b=mgl.kscaled(complex(x,0)); print(x, a.real*math.exp(-x)/k0-1, b.real*math.exp(-x)/k1-1)
for z in [2*cmath.exp(1j*t) for t in (0,0.5,1.0,1.5)]+[1.9+0.6j, 0.1+1.98j]:
    print(z, [abs(p-q)/abs(q) for p,q in zip(mgl._k_series(z), mgl._k_integral(z))])
def asym(z,nu):
    mu=4*nu*nu; s=1; t=1
    for k in range(1,12):
        t*= (mu-(2*k-1)**2)/(k*8*z); s+=t
    return cmath.sqrt(math.pi/(2*z))*s
for z in [30+0j, 3+40j, 0.5+60j]:
    a,b=mgl.kscaled(z); print(z, abs(a/asym(z,0)-1), abs(b/asym(z,1)-1))
# Durbin tests
t=0.007
for kk in (0.01,0.03):
    F=lambda s: [(cmath.exp(-kk*cmath.sqrt(s))/s,)]
    f,h=mgl.durbin(F,t,1,1,N=2000)
    print('erfc',f[0][0], math.erfc(kk/(2*math.sqrt(t))), h[0][0])
F=lambda s: [(1/s,)]
f,h=mgl.durbin(F,t,1,1,N=2000); print('unit',f[0][0],h[0][0])
