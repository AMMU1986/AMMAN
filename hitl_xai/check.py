#!/usr/bin/env python3
import re, sys

md = open('chapter.md', encoding='utf-8').read()

# split body vs references
idx = md.index('## References')
body = md[:idx]
refs_block = md[idx:]

# ---- citations in body ----
cites = re.findall(r'\[(\d+)\]', body)
cites = [int(c) for c in cites]
first_seen = []
seen = set()
for c in cites:
    if c not in seen:
        seen.add(c)
        first_seen.append(c)
print('distinct cited in body:', sorted(set(cites)))
print('first-appearance order:', first_seen)
ascending = first_seen == sorted(first_seen)
print('SERIAL ORDER (first appearance ascending)?', ascending)
missing = [n for n in range(1, 47) if n not in seen]
print('cited count:', len(seen), 'missing from body:', missing)

# per-citation total counts
from collections import Counter
cnt = Counter(cites)

# ---- references list ----
ref_nums = re.findall(r'^\[(\d+)\]', refs_block, re.M)
ref_nums = [int(x) for x in ref_nums]
print('reference entries:', len(ref_nums), 'range ok?', ref_nums == list(range(1,47)))
years = re.findall(r'(19|20)(\d{2})', refs_block)
yrs = [int(a+b) for a,b in years]
bad_years = [y for y in yrs if y < 2019 or y > 2026]
print('years found:', sorted(set(yrs)), 'OUT OF RANGE:', sorted(set(bad_years)))

# ---- figure / table citations (exclude the placeholder + caption definition lines) ----
def count_refs(label):
    # count "Figure 5.x" / "Table 5.x" mentions in body prose
    return len(re.findall(label, body))

for n in range(1,5):
    figc = len(re.findall(r'Figure 5\.%d' % n, body))
    print('Figure 5.%d mentions in body (incl caption):' % n, figc)
for n in range(1,5):
    tabc = len(re.findall(r'Table 5\.%d' % n, body))
    print('Table 5.%d mentions in body (incl caption):' % n, tabc)

# ---- abstract word count ----
m = re.search(r'## Abstract\s+(.*?)\n\*\*Keywords', md, re.S)
abstract = m.group(1)
aw = len(abstract.split())
print('abstract words:', aw)

# keywords count
kw = re.search(r'\*\*Keywords:\*\*(.*)', md)
kwl = [k.strip() for k in kw.group(1).split(',') if k.strip()]
print('keywords:', len(kwl))

# ---- total word count (body prose, excluding tables/markup roughly) ----
words = re.findall(r"[A-Za-z][A-Za-z'-]*", md)
print('approx total words (whole doc):', len(words))
# body only, excluding references
bwords = re.findall(r"[A-Za-z][A-Za-z'-]*", body)
print('approx body words (excl refs):', len(bwords))
