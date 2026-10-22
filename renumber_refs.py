#!/usr/bin/env python3
"""Renumber citations in the Chapter 3 markdown so references appear in strict
serial (first-appearance) order. Updates in-text [n] citations and reorders the
reference-list entries accordingly."""

import re

PATH = '/projects/sandbox/AMMAN/Chapter_3_EV_Battery_Charging_AI.md'

with open(PATH, encoding='utf-8') as f:
    text = f.read()

marker = '## References'
idx = text.index(marker)
body = text[:idx]
refs_section = text[idx:]

# 1. First-appearance order in body
order = []
seen = set()
for m in re.finditer(r'\[(\d+)\]', body):
    n = int(m.group(1))
    if n not in seen:
        seen.add(n)
        order.append(n)

assert len(order) == 53, f"expected 53 unique refs, got {len(order)}: {order}"

# old number -> new number (1-based by first appearance)
remap = {old: i + 1 for i, old in enumerate(order)}
assert sorted(remap.values()) == list(range(1, 54))

# 2. Remap body citations in a single pass
def repl_body(m):
    return '[' + str(remap[int(m.group(1))]) + ']'

new_body = re.sub(r'\[(\d+)\]', repl_body, body)

# 3. Parse and remap reference entries
ref_lines = refs_section.split('\n')
header = ref_lines[0]  # '## References'
entries = {}
for line in ref_lines:
    m = re.match(r'^\[(\d+)\]\s*(.*)$', line.strip())
    if m:
        old = int(m.group(1))
        entries[remap[old]] = m.group(2)

assert len(entries) == 53, f"expected 53 ref entries, got {len(entries)}"

# 4. Rebuild references section sorted by new number
new_refs = [header, '']
for n in range(1, 54):
    new_refs.append(f'[{n}] {entries[n]}')
    new_refs.append('')
new_refs_section = '\n'.join(new_refs).rstrip() + '\n'

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(new_body + new_refs_section)

# 5. Verify strict order in the new file
with open(PATH, encoding='utf-8') as f:
    check = f.read()
cbody = check[:check.index(marker)]
fa = []
cs = set()
for m in re.finditer(r'\[(\d+)\]', cbody):
    n = int(m.group(1))
    if n not in cs:
        cs.add(n)
        fa.append(n)
print("First-appearance order now:", fa)
print("Strictly ascending:", fa == sorted(fa) == list(range(1, 54)))
