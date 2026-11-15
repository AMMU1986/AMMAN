"""Convert the LaTeX subset used in the manuscript to Office Math Markup (OMML).

Supported: \\frac/\\dfrac, sub/superscripts, \\sqrt, \\left...\\right, cases,
\\sum/\\prod/\\bigcup with limits, \\min/\\max limits, accents (\\hat, \\bar,
\\tilde, \\widehat), font commands (\\mathrm, \\text, \\mathbf, \\boldsymbol,
\\mathcal, \\mathbb), Greek letters and the operators used in Eqs. (1)-(45).
"""

from xml.sax.saxutils import escape

GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ϵ", "varepsilon": "ε",
    "zeta": "ζ", "eta": "η", "theta": "θ", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν",
    "xi": "ξ", "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "phi": "ϕ", "varphi": "φ",
    "chi": "χ", "psi": "ψ", "omega": "ω", "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ",
    "Lambda": "Λ", "Xi": "Ξ", "Pi": "Π", "Sigma": "Σ", "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
    "ell": "ℓ",
}
SYMBOLS = {
    "cdot": "·", "times": "×", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥", "neq": "≠",
    "ne": "≠", "in": "∈", "sim": "∼", "pm": "±", "mp": "∓", "odot": "⊙", "top": "⊤",
    "setminus": "∖", "subseteq": "⊆", "subset": "⊂", "infty": "∞", "lVert": "‖", "rVert": "‖",
    "mid": "|", "ldots": "…", "dots": "…", "cdots": "⋯", "to": "→", "rightarrow": "→",
    "prime": "′", "partial": "∂", "nabla": "∇", "lfloor": "⌊", "rfloor": "⌋", "lceil": "⌈",
    "rceil": "⌉", "cup": "∪", "cap": "∩", "propto": "∝", "approx": "≈", "star": "⋆",
    "ast": "∗", "forall": "∀", "exists": "∃", "langle": "⟨", "rangle": "⟩", "vert": "|",
}
SPACES = {"quad": "\u2003", "qquad": "\u2003\u2003", ",": "\u2009", ";": "\u2005", ":": "\u2005",
          "!": "", " ": " "}
NARY = {"sum": "∑", "prod": "∏", "bigcup": "⋃", "bigcap": "⋂", "int": "∫"}
FUNCS = {"ln", "exp", "tanh", "log", "arg", "det", "tr", "sin", "cos", "lim"}
LIMFUNCS = {"min", "max", "sup", "inf"}
ACCENTS = {"hat": "\u0302", "widehat": "\u0302", "bar": "\u0305", "overline": "\u0305",
           "tilde": "\u0303", "widetilde": "\u0303", "dot": "\u0307"}
STYLE_CMDS = {"mathrm": "p", "operatorname": "p", "text": "text", "mathbf": "b",
              "boldsymbol": "bi", "mathit": "i", "mathcal": "script", "mathbb": "double-struck"}
NARY_STOP_CHARS = set("+-=,<>≤≥")


class Node:
    def __init__(self, kind, **kw):
        self.kind = kind
        self.__dict__.update(kw)


class Parser:
    def __init__(self, s):
        self.s = s
        self.i = 0
        self.tag = None

    def peek(self):
        self.skip_ws()
        return self.s[self.i] if self.i < len(self.s) else ""

    def skip_ws(self):
        while self.i < len(self.s) and self.s[self.i] in " \t\n\r":
            self.i += 1

    def read_cmd(self):
        assert self.s[self.i] == "\\"
        j = self.i + 1
        if j < len(self.s) and self.s[j].isalpha():
            while j < len(self.s) and self.s[j].isalpha():
                j += 1
            name = self.s[self.i + 1:j]
        else:
            name = self.s[j] if j < len(self.s) else ""
            j += 1
        self.i = j
        return name

    def lookahead_cmd(self):
        self.skip_ws()
        if self.i < len(self.s) and self.s[self.i] == "\\":
            save = self.i
            name = self.read_cmd()
            self.i = save
            return name
        return None

    def read_braced_raw(self):
        self.skip_ws()
        if self.s[self.i] != "{":
            c = self.s[self.i]
            self.i += 1
            return c
        depth, j = 0, self.i
        while j < len(self.s):
            if self.s[j] == "{":
                depth += 1
            elif self.s[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        raw = self.s[self.i + 1:j]
        self.i = j + 1
        return raw

    def parse(self):
        nodes = self.parse_seq(stops=())
        return nodes

    def parse_arg(self):
        self.skip_ws()
        if self.peek() == "{":
            self.i += 1
            nodes = self.parse_seq(stops=("}",))
            self.i += 1  # consume }
            return nodes
        atom = self.parse_atom()
        return [atom] if atom is not None else []

    def at_stop(self, stops):
        self.skip_ws()
        if self.i >= len(self.s):
            return True
        c = self.s[self.i]
        if c in stops:
            return True
        if c == "&" and "&" in stops:
            return True
        if c == "\\":
            name = self.lookahead_cmd()
            if name in ("right", "end") and "cmdstop" in stops:
                return True
            if name == "\\" and "rowstop" in stops:
                return True
        return False

    def parse_seq(self, stops):
        out = []
        while not self.at_stop(stops):
            atom = self.parse_atom()
            if atom is None:
                continue
            atom = self.parse_scripts(atom)
            if atom.kind == "nary":
                atom.body = self.collect_operand(stops)
            out.append(atom)
        return out

    def parse_scripts(self, base):
        sub = sup = None
        while True:
            c = self.peek()
            if c == "_":
                self.i += 1
                sub = self.parse_arg()
            elif c == "^":
                self.i += 1
                sup = self.parse_arg()
            else:
                break
        if base.kind == "nary" or base.kind == "limfunc":
            base.sub, base.sup = sub, sup
            return base
        if sub is None and sup is None:
            return base
        return Node("script", base=base, sub=sub, sup=sup)

    def collect_operand(self, stops):
        body, depth = [], 0
        while not self.at_stop(stops):
            c = self.s[self.i]
            if depth == 0 and c in NARY_STOP_CHARS:
                break
            if c == "\\":
                name = self.lookahead_cmd()
                if depth == 0 and name in ("quad", "qquad", "le", "ge", "leq", "geq", "neq", "in",
                                           "approx", "sim"):
                    break
            if c in "([":
                depth += 1
            elif c in ")]":
                if depth == 0:
                    break
                depth -= 1
            atom = self.parse_atom()
            if atom is None:
                continue
            atom = self.parse_scripts(atom)
            if atom.kind == "nary":
                atom.body = self.collect_operand(stops)
            body.append(atom)
        return body

    def parse_delim_char(self):
        self.skip_ws()
        c = self.s[self.i]
        if c == "\\":
            name = self.read_cmd()
            return {"{": "{", "}": "}", "lVert": "‖", "rVert": "‖", "|": "‖", "langle": "⟨",
                    "rangle": "⟩", "lfloor": "⌊", "rfloor": "⌋", "lceil": "⌈", "rceil": "⌉",
                    "vert": "|"}.get(name, "")
        self.i += 1
        return "" if c == "." else c

    def parse_atom(self):
        self.skip_ws()
        if self.i >= len(self.s):
            return None
        c = self.s[self.i]
        if c == "{":
            self.i += 1
            nodes = self.parse_seq(stops=("}",))
            self.i += 1
            return Node("group", items=nodes)
        if c == "\\":
            name = self.read_cmd()
            if name in ("frac", "dfrac", "tfrac"):
                num = self.parse_arg()
                den = self.parse_arg()
                return Node("frac", num=num, den=den)
            if name == "sqrt":
                return Node("rad", arg=self.parse_arg())
            if name == "left":
                open_c = self.parse_delim_char()
                content = self.parse_seq(stops=("cmdstop",))
                self.skip_ws()
                self.read_cmd()  # right
                close_c = self.parse_delim_char()
                return Node("delim", open=open_c, close=close_c, items=content)
            if name == "begin":
                env = self.read_braced_raw()
                rows, row = [], []
                while True:
                    cell = self.parse_seq(stops=("&", "rowstop", "cmdstop"))
                    row.append(cell)
                    self.skip_ws()
                    if self.i < len(self.s) and self.s[self.i] == "&":
                        self.i += 1
                        continue
                    name2 = self.lookahead_cmd()
                    if name2 == "\\":
                        self.read_cmd()
                        rows.append(row)
                        row = []
                        continue
                    if name2 == "end":
                        self.read_cmd()
                        self.read_braced_raw()
                        rows.append(row)
                        break
                    raise ValueError("bad environment " + env)
                return Node("cases", rows=rows)
            if name in STYLE_CMDS:
                style = STYLE_CMDS[name]
                if style == "text":
                    return Node("text", text=self.read_braced_raw(), style="text")
                inner = self.parse_arg()
                return Node("styled", items=inner, style=style)
            if name in ACCENTS:
                return Node("acc", chr=ACCENTS[name], arg=self.parse_arg())
            if name in NARY:
                return Node("nary", chr=NARY[name], sub=None, sup=None, body=[])
            if name in LIMFUNCS:
                return Node("limfunc", name=name, sub=None, sup=None)
            if name in FUNCS:
                return Node("text", text=name, style="p")
            if name in GREEK:
                return Node("char", text=GREEK[name])
            if name in SYMBOLS:
                return Node("char", text=SYMBOLS[name])
            if name in SPACES:
                return Node("char", text=SPACES[name]) if SPACES[name] else None
            if name in ("{", "}", "|", "%", "#", "&", "_"):
                return Node("char", text={"|": "‖"}.get(name, name))
            if name == "tag":
                self.tag = self.read_braced_raw()
                return None
            if name in ("limits", "nolimits", "displaystyle", "textstyle"):
                return None
            raise ValueError("unsupported command \\" + name)
        if c in "^_":
            # script without base: attach to an empty base
            return Node("char", text="")
        self.i += 1
        if c == "'":
            return Node("char", text="′")
        if c == "*":
            return Node("char", text="∗")
        if c == "-":
            return Node("char", text="−")
        if c == "~":
            return Node("char", text=" ")
        return Node("char", text=c)


def _run(text, style=None):
    rpr = ""
    if style == "p":
        rpr = '<m:rPr><m:sty m:val="p"/></m:rPr>'
    elif style == "b":
        rpr = '<m:rPr><m:sty m:val="b"/></m:rPr>'
    elif style == "bi":
        rpr = '<m:rPr><m:sty m:val="bi"/></m:rPr>'
    elif style == "i":
        rpr = '<m:rPr><m:sty m:val="i"/></m:rPr>'
    elif style in ("script", "double-struck"):
        rpr = '<m:rPr><m:scr m:val="%s"/><m:sty m:val="p"/></m:rPr>' % style
    elif style == "text":
        rpr = '<m:rPr><m:nor/></m:rPr>'
    wrpr = '<w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/></w:rPr>'
    return '<m:r>%s%s<m:t xml:space="preserve">%s</m:t></m:r>' % (rpr, wrpr, escape(text))


def emit(nodes, style=None, display=True):
    out = []
    for n in nodes:
        out.append(emit_node(n, style, display))
    return "".join(out)


def emit_node(n, style=None, display=True):
    k = n.kind
    if k == "char":
        if not n.text:
            return ""
        st = style
        if st is None and (n.text.isdigit() or not n.text.isalpha()):
            st = None
        return _run(n.text, st)
    if k == "text":
        return _run(n.text, n.style if style is None or n.style == "text" else style)
    if k == "styled":
        return emit(n.items, n.style, display)
    if k == "group":
        return emit(n.items, style, display)
    if k == "frac":
        return "<m:f><m:num>%s</m:num><m:den>%s</m:den></m:f>" % (
            emit(n.num, style, display), emit(n.den, style, display))
    if k == "rad":
        return ('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr><m:deg/><m:e>%s</m:e></m:rad>'
                % emit(n.arg, style, display))
    if k == "delim":
        return ('<m:d><m:dPr><m:begChr m:val="%s"/><m:endChr m:val="%s"/></m:dPr><m:e>%s</m:e></m:d>'
                % (escape(n.open, {'"': "&quot;"}), escape(n.close, {'"': "&quot;"}),
                   emit(n.items, style, display)))
    if k == "cases":
        rows = []
        for row in n.rows:
            cells = [emit(cell, style, display) for cell in row]
            rows.append("<m:e>%s</m:e>" % _run("\u2003").join(cells))
        return ('<m:d><m:dPr><m:begChr m:val="{"/><m:endChr m:val=""/></m:dPr><m:e><m:eqArr>%s'
                '</m:eqArr></m:e></m:d>' % "".join(rows))
    if k == "acc":
        return ('<m:acc><m:accPr><m:chr m:val="%s"/></m:accPr><m:e>%s</m:e></m:acc>'
                % (n.chr, emit(n.arg, style, display)))
    if k == "script":
        base = emit_node(n.base, style, display)
        if n.sub is not None and n.sup is not None:
            return ("<m:sSubSup><m:e>%s</m:e><m:sub>%s</m:sub><m:sup>%s</m:sup></m:sSubSup>"
                    % (base, emit(n.sub, style, display), emit(n.sup, style, display)))
        if n.sub is not None:
            return "<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>" % (base, emit(n.sub, style, display))
        return "<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>" % (base, emit(n.sup, style, display))
    if k == "nary":
        pr = '<m:chr m:val="%s"/><m:limLoc m:val="%s"/>' % (n.chr, "undOvr" if display else "subSup")
        if n.sub is None:
            pr += '<m:subHide m:val="1"/>'
        if n.sup is None:
            pr += '<m:supHide m:val="1"/>'
        return ("<m:nary><m:naryPr>%s</m:naryPr><m:sub>%s</m:sub><m:sup>%s</m:sup><m:e>%s</m:e></m:nary>"
                % (pr, emit(n.sub or [], style, display), emit(n.sup or [], style, display),
                   emit(n.body, style, display)))
    if k == "limfunc":
        name = _run(n.name, "p")
        if n.sub is None:
            return name
        if display:
            return "<m:limLow><m:e>%s</m:e><m:lim>%s</m:lim></m:limLow>" % (
                name, emit(n.sub, style, display))
        return "<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>" % (name, emit(n.sub, style, display))
    raise ValueError(k)


def latex_to_omml(latex, display=True):
    """Return (omml_inner_xml, tag)."""
    p = Parser(latex)
    nodes = p.parse()
    return emit(nodes, None, display), p.tag
