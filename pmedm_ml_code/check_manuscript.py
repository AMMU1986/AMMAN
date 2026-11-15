#!/usr/bin/env python3
"""Check the manuscript against the brief: word counts, 45 equations, 43 references from
2016-2026 cited in serial order."""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(ROOT, "Manuscript_PMEDM_ML_Reanalysis.md")
text = open(MD, encoding="utf-8").read()

main, refs = text.split("\n## References\n")
sections = re.split(r"\n(?=## )", main)


def prose_words(s):
    s = re.sub(r"\$\$.*?\$\$", " ", s, flags=re.S)          # display equations
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", s)               # figure lines
    lines = [ln for ln in s.splitlines() if not ln.lstrip().startswith("|")]  # tables
    s = "\n".join(lines)
    s = re.sub(r"^#+ .*$", " ", s, flags=re.M)               # headings
    s = re.sub(r"\$[^$]*\$", " x ", s)                        # inline math counts as a word
    return len(re.findall(r"[A-Za-z0-9µ²³⁻⁶\u00C0-\u024F][^\s]*", s))


counts = {}
for sec in sections:
    title = sec.strip().splitlines()[0]
    counts[title] = prose_words(sec)
for k, v in counts.items():
    print("%5d  %s" % (v, k[:80]))
body_titles = [k for k in counts if k.startswith("## ") and not k.startswith("## Data and code")]
total_body = sum(counts[k] for k in body_titles)
print("Words, abstract to conclusions (prose only, excl. equations/tables/figures/references): %d"
      % total_body)
intro = [v for k, v in counts.items() if k.startswith("## 1. Introduction")][0]
print("Introduction words: %d" % intro)

tags = [int(t) for t in re.findall(r"\\tag\{(\d+)\}", main)]
print("Equations: %d, sequential 1..N: %s" % (len(tags), tags == list(range(1, len(tags) + 1))))

# citations in the body (exclude reference list)
cites = []
for m in re.finditer(r"\[(\d+(?:\s*[–,-]\s*\d+)*)\]", main):
    for part in re.split(r"\s*,\s*", m.group(1)):
        if re.search(r"[–-]", part):
            a, b = [int(x) for x in re.split(r"\s*[–-]\s*", part)]
            cites.extend(range(a, b + 1))
        else:
            cites.append(int(part))
first = []
for c in cites:
    if c not in first:
        first.append(c)
print("Distinct references cited: %d; first-appearance order serial: %s"
      % (len(first), first == list(range(1, len(first) + 1))))
if first != list(range(1, len(first) + 1)):
    print("  order:", first)

ref_lines = [ln for ln in refs.splitlines() if re.match(r"^\d+\. ", ln)]
nums = [int(ln.split(".")[0]) for ln in ref_lines]
years = []
for ln in ref_lines:
    ys = re.findall(r"\((\d{4})\)", ln)
    years.append(int(ys[-1]) if ys else None)
print("Reference list entries: %d, numbered 1..N: %s" % (len(nums), nums == list(range(1, len(nums) + 1))))
bad = [(n, y) for n, y in zip(nums, years) if y is None or not 2016 <= y <= 2026]
print("References outside 2016-2026 or without year: %s" % (bad or "none"))
uncited = sorted(set(nums) - set(first))
print("Uncited references: %s" % (uncited or "none"))
sys.exit(0)
