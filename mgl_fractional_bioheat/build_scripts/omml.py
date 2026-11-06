"""Tiny LaTeX-subset -> OMML converter for Word equations."""
from xml.sax.saxutils import escape

SYM = {
    "alpha": "α", "beta": "β", "gamma": "γ", "Gamma": "Γ", "delta": "δ", "Delta": "Δ",
    "epsilon": "ε", "varepsilon": "ε", "theta": "θ", "vartheta": "ϑ", "lesssim": "≲", "gtrsim": "≳", "arcsin": "arcsin", "kappa": "κ", "lambda": "λ",
    "mu": "μ", "rho": "ρ", "sigma": "σ", "tau": "τ", "phi": "φ", "varphi": "φ",
    "omega": "ω", "eta": "η", "pi": "π", "partial": "∂", "nabla": "∇", "infty": "∞",
    "to": "→", "rightarrow": "→", "le": "≤", "ge": "≥", "approx": "≈", "propto": "∝",
    "cdot": "⋅", "times": "×", "pm": "±", "mp": "∓", "neq": "≠", "sim": "∼",
    "ll": "≪", "gg": "≫", "prime": "′", "ldots": "…", "Pi": "Π", "varpi": "ϖ", "Gamma": "Γ", "Sigma": "Σ", "mathsf": None, "dots": "…", "cdots": "⋯", "ge": "≥", "quad": "\u2003", "qquad": "\u2003\u2003",
    ",": "\u2009", ";": "\u2005", "{": "{", "}": "}", "sum": None, "int": None,
    "!": "", " ": "\u2005", "arcsin": "arcsin", "Re": "Re", "Im": "Im", "xi": "ξ", "varrho": "ϱ", "Xi": "Ξ", "simeq": "≃", "ne": "≠", "leftrightarrow": "↔", "zeta": "ζ", "Phi": "Φ", "Psi": "Ψ", "Lambda": "Λ", "nu": "ν", "chi": "χ", "ast": "∗", "Rightarrow": "⇒", "equiv": "≡", "Omega": "Ω", "in": "∈", "Delta": "Δ", "leq": "≤", "geq": "≥", "hbar": "ħ", "ell": "ℓ", "Sigma": "Σ", "Theta": "Θ", "sqrt": None,
}
FUNCS = {"det", "tanh", "cos", "sin", "exp", "ln", "log", "Re", "Im", "max", "min", "lim", "sinh", "cosh", "erfc", "arcsin", "cot", "tan", "arg", "sgn"}


def run(text, plain=False):
    if not text:
        return ""
    sty = '<m:rPr><m:sty m:val="p"/></m:rPr>' if plain else ""
    return ('<m:r>%s<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'
            '<m:t xml:space="preserve">%s</m:t></m:r>') % (sty, escape(text))


class P:
    def __init__(self, s):
        self.s = s
        self.i = 0

    def peek(self):
        return self.s[self.i] if self.i < len(self.s) else None

    def skipws(self):
        while self.peek() == " ":
            self.i += 1

    def cmd(self):
        # at backslash
        self.i += 1
        c = self.peek()
        if c is not None and not c.isalpha():
            self.i += 1
            return c
        j = self.i
        while self.i < len(self.s) and self.s[self.i].isalpha():
            self.i += 1
        return self.s[j:self.i]

    def group(self):
        self.skipws()
        if self.peek() == "{":
            self.i += 1
            items = self.seq("}")
            self.i += 1
            return join(items)
        return join([self.atom()])

    def atom(self):
        """returns ('t', text, plain) or ('x', xml)"""
        self.skipws()
        c = self.peek()
        if c == "{":
            return ("x", self.group())
        if c == "\\":
            name = self.cmd()
            if name in ("frac", "tfrac"):
                n = self.group()
                d = self.group()
                return ("x", "<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>" % (n, d))
            if name == "sqrt":
                return ("x", '<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>%s</m:e></m:rad>' % self.group())
            if name == "boldsymbol":
                return ("x", self.group())
            if name in ("bar", "tilde", "hat", "dot", "ddot"):
                chm = {"bar": "\u0305", "tilde": "\u0303", "hat": "\u0302", "dot": "\u0307", "ddot": "\u0308"}[name]
                return ("x", '<m:acc><m:accPr><m:chr m:val="%s"/></m:accPr><m:e>%s</m:e></m:acc>' % (chm, self.group()))
            if name in ("mathrm", "text", "mathbf"):
                self.skipws()
                self.i += 1
                j = self.s.index("}", self.i)
                t = self.s[self.i:j]
                self.i = j + 1
                return ("t", t, True)
            if name == "mathcal":
                g = self.group()
                return ("t", {"R": "ℛ", "L": "ℒ", "H": "ℋ"}.get(re_strip(g), "ℒ"), True)
            if name in ("sum", "int"):
                sub = sup = ""
                for _ in range(2):
                    self.skipws()
                    if self.peek() == "_":
                        self.i += 1
                        sub = self.group()
                    elif self.peek() == "^":
                        self.i += 1
                        sup = self.group()
                body = self.group()
                chr_ = '<m:chr m:val="∑"/><m:limLoc m:val="undOvr"/>' if name == "sum" else '<m:limLoc m:val="subSup"/>'
                hide = ("" if sub else '<m:subHide m:val="1"/>') + ("" if sup else '<m:supHide m:val="1"/>')
                return ("x", "<m:nary><m:naryPr>%s%s</m:naryPr><m:sub>%s</m:sub><m:sup>%s</m:sup><m:e>%s</m:e></m:nary>"
                        % (chr_, hide, sub, sup, body))
            if name == "left":
                self.skipws()
                b = self.s[self.i]
                self.i += 1
                if b == "\\":
                    b = self.s[self.i]
                    self.i += 1
                items = self.seq("\\right")
                self.i += len("\\right")
                e = self.s[self.i]
                self.i += 1
                if e == "\\":
                    e = self.s[self.i]
                    self.i += 1
                if e == ".":
                    e = ""
                if b == ".":
                    b = ""
                return ("x", '<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr><m:e>%s</m:e></m:d>'
                        % (escape(b), escape(e), join(items)))
            if name in FUNCS:
                return ("t", name, True)
            if name in SYM:
                return ("t", SYM[name], name in (",", ";", "quad", "qquad"))
            raise ValueError("unknown command \\" + name)
        self.i += 1
        if c.isdigit() or c in "()[]=+-<>,.|/!:;'":
            return ("t", c.replace("-", "−").replace("'", "′"), True)
        return ("t", c, False)

    def seq(self, until=None):
        items = []
        while self.i < len(self.s):
            self.skipws()
            if until and self.s.startswith(until, self.i):
                break
            if self.i >= len(self.s):
                break
            a = self.atom()
            # scripts
            sub = sup = None
            for _ in range(2):
                self.skipws()
                if self.peek() == "_":
                    self.i += 1
                    sub = self.group()
                elif self.peek() == "^":
                    self.i += 1
                    sup = self.group()
            if sub is None and sup is None:
                items.append(a)
                continue
            base = join([a])
            if sub is not None and sup is not None:
                x = "<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>" % (base, sub, sup)
            elif sub is not None:
                x = "<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>" % (base, sub)
            else:
                x = "<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>" % (base, sup)
            items.append(("x", x))
        return items


import re


def re_strip(x):
    return re.sub(r'<[^>]+>', '', x)


def join(items):
    out = []
    buf = ""
    bplain = None
    for it in items:
        if it[0] == "t":
            if bplain is not None and it[2] != bplain:
                out.append(run(buf, bplain))
                buf = ""
            buf += it[1]
            bplain = it[2]
        else:
            if buf:
                out.append(run(buf, bplain))
            buf = ""
            bplain = None
            out.append(it[1])
    if buf:
        out.append(run(buf, bplain))
    return "".join(out)


def omath(latex):
    p = P(latex)
    items = p.seq()
    return "<m:oMath>%s</m:oMath>" % join(items)
