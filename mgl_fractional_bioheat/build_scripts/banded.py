class Banded:
    """Banded matrix with half bandwidth bw, LU without pivoting."""

    def __init__(self, n, bw):
        self.n, self.bw = n, bw
        self.a = [[0.0] * (2 * bw + 1) for _ in range(n)]  # a[i][j-i+bw]

    def add(self, i, j, v):
        self.a[i][j - i + self.bw] += v

    def lu(self):
        n, bw, a = self.n, self.bw, self.a
        for k in range(n):
            piv = a[k][bw]
            hi = min(n, k + bw + 1)
            for i in range(k + 1, hi):
                aik = a[i][k - i + bw]
                if aik == 0.0:
                    continue
                m = aik / piv
                a[i][k - i + bw] = m
                ri, rk = a[i], a[k]
                for j in range(k + 1, hi):
                    ri[j - i + bw] -= m * rk[j - k + bw]

    def solve(self, b):
        n, bw, a = self.n, self.bw, self.a
        y = list(b)
        for i in range(n):
            lo = max(0, i - bw)
            s = y[i]
            ai = a[i]
            for j in range(lo, i):
                s -= ai[j - i + bw] * y[j]
            y[i] = s
        for i in range(n - 1, -1, -1):
            hi = min(n, i + bw + 1)
            s = y[i]
            ai = a[i]
            for j in range(i + 1, hi):
                s -= ai[j - i + bw] * y[j]
            y[i] = s / ai[bw]
        return y

