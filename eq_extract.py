#!/usr/bin/env python3
"""
Extract all display equations from the manuscript and emit them in Word
equation-editor LaTeX (linear) form, one copy-paste block per equation.

Usage in Word: Insert > Equation > (Equation Tools) set 'LaTeX' > paste the
line > press Enter/Space to convert to a professional (2-D) equation.
"""
import os, re

HERE = os.path.dirname(__file__)
MD = os.path.join(HERE, "FXTS_Delayed_CGBAM_Manuscript.md")
OUT = os.path.join(HERE, "FXTS_Equations_WordLaTeX.md")

text = open(MD, encoding="utf-8").read()

# grab display-math blocks ($$ ... $$)
blocks = re.findall(r"\$\$(.*?)\$\$", text, flags=re.DOTALL)


def convert_system(s):
    """Convert \\left\\{ \\begin{aligned}...\\end{aligned} \\right. to \\begin{cases}."""
    if "\\begin{aligned}" not in s:
        return s
    inner = s.split("\\begin{aligned}", 1)[1].split("\\end{aligned}", 1)[0]
    rows = [r.strip() for r in inner.split("\\\\") if r.strip()]
    out = []
    for r in rows:
        r = r.replace("&=", "=", 1)   # drop the alignment ampersand
        r = r.strip().rstrip(",").strip()
        out.append(r)
    return "\\begin{cases} " + " \\\\ ".join(out) + " \\end{cases}"


def sanitize(s):
    """Rewrite constructs the Word 365 LaTeX converter does not accept."""
    # protect row separators (\\) used by cases/matrices from the space cleanup
    s = s.replace("\\\\", "\x00")
    # thin/med spaces and explicit spaces -> normal space
    for t in ("\\!", "\\,", "\\;", "\\:"):
        s = s.replace(t, "")
    s = s.replace("\\ ", " ")
    # display fractions -> plain fraction
    s = s.replace("\\dfrac", "\\frac").replace("\\tfrac", "\\frac")
    # style hints Word does not need
    s = s.replace("\\textstyle", "").replace("\\displaystyle", "")
    # operatorname -> mathrm (sign function)
    s = s.replace("\\operatorname{sign}", "\\mathrm{sign}")
    # drop manual delimiter sizing (\big \Big \bigg \Bigg + optional l/r/m),
    # keeping the delimiter that follows
    s = re.sub(r"\\[Bb]igg?[lrm]?", "", s)
    # wide spacers -> spaces
    s = s.replace("\\qquad", "  ").replace("\\quad", " ")
    # tidy underbrace style leftovers
    s = s.replace("_{ T_1}", "_{T_1}").replace("_{ T_2}", "_{T_2}")
    # restore protected row separators
    s = s.replace("\x00", "\\\\")
    return s


def clean(block):
    s = block
    m = re.search(r"\\tag\{(\d+)\}", s)
    num = m.group(1) if m else "?"
    s = re.sub(r"\\tag\{\d+\}", "", s)
    s = s.replace("\\\\[2pt]", "\\\\")
    s = re.sub(r"\s+", " ", s).strip()
    s = convert_system(s)
    s = sanitize(s)
    s = re.sub(r"\s+", " ", s).strip()
    return int(num) if num.isdigit() else num, s


eqs = [clean(b) for b in blocks]
eqs = [e for e in eqs if e[0] != "?"]
eqs.sort(key=lambda e: e[0])

lines = [
    "# Equations in Word Equation-Editor LaTeX (linear) form",
    "",
    "All 120 display equations from **FXTS_Delayed_CGBAM_Manuscript**, each ready to",
    "paste into Microsoft Word's equation editor.",
    "",
    "**How to use in Word (Microsoft 365 / 2016+):**",
    "1. Insert tab → *Equation* (or press `Alt` `=`).",
    "2. In *Equation Tools → Conversions*, set the input mode to **{} LaTeX**.",
    "3. Paste one equation line below, then press **Enter** (or Space) to render it as a 2-D equation.",
    "",
    "> Multi-line systems use `\\begin{cases} ... \\end{cases}`; coefficient matrices use",
    "> `\\begin{bmatrix} ... \\end{bmatrix}`. Both are supported by the Word 365 LaTeX converter.",
    "> If your Word build rejects `\\mathbb{R}`, replace it with `ℝ` (it renders identically).",
    "",
    "---",
    "",
]

for num, eq in eqs:
    lines.append("**Equation (%d)**" % num)
    lines.append("")
    lines.append("```latex")
    lines.append(eq)
    lines.append("```")
    lines.append("")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("wrote", OUT, "with", len(eqs), "equations")
# sanity preview of a couple
for n in (1, 16, 19, 38, 64, 120):
    for num, eq in eqs:
        if num == n:
            print("\n(%d) %s" % (num, eq[:180]))
            break
