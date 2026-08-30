#!/usr/bin/env python3
"""
Reduce the chapter's reference list from 75 to exactly 43 and remap all
in-text citations so that they (a) use numbers 1..43, (b) appear in
ascending serial order at first mention, and (c) leave the abstract free
of citations. Some of the 43 references are cited at more than one point,
which is normal scholarly practice.
"""
import re

SRC = "Chapter_Bio_Integrated_Urban_Tourism.md"
t = open(SRC, encoding="utf-8").read()

body, reftext = t.split("## References")

# Parse original reference entries -> {oldnum: text}
orig = {}
for m in re.finditer(r'^\[(\d+)\]\s+(.*)$', reftext, re.M):
    orig[int(m.group(1))] = m.group(2).strip()
assert len(orig) == 75, f"expected 75 refs, got {len(orig)}"

# Choose 43 references to KEEP (one representative per theme, spread across
# the source list). These old numbers will survive; others are folded onto
# the nearest kept reference thematically.
keep = [1, 3, 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 24, 26, 27, 29,
        30, 32, 33, 34, 36, 37, 38, 40, 41, 42, 44, 46, 48, 50, 52, 54, 56,
        58, 60, 62, 64, 66, 69, 72, 74]
assert len(keep) == 43, len(keep)

# Map every old number (1..75) onto a kept old number.
# Rule: map to the nearest kept number <= itself; if none, nearest >.
def nearest_kept(old):
    if old in keep:
        return old
    below = [k for k in keep if k <= old]
    if below:
        return max(below)
    return min(keep)

old_to_keptold = {i: nearest_kept(i) for i in range(1, 76)}

# Now walk the body in order of appearance, assigning new serial numbers
# to kept-old references as they first appear.
new_num = {}
counter = [0]
def replace_cite(match):
    old = int(match.group(1))
    ko = old_to_keptold[old]
    if ko not in new_num:
        counter[0] += 1
        new_num[ko] = counter[0]
    return f"[{new_num[ko]}]"

new_body = re.sub(r'\[(\d+)\]', replace_cite, body)

# Every kept ref should have been cited; assign any not-yet-seen at the end
for ko in keep:
    if ko not in new_num:
        counter[0] += 1
        new_num[ko] = counter[0]

assert counter[0] == 43, f"ended with {counter[0]} refs numbered"

# Build new reference list ordered by new number
inv = {v: k for k, v in new_num.items()}
new_refs_lines = ["## References", ""]
for n in range(1, 44):
    ko = inv[n]
    new_refs_lines.append(f"[{n}] {orig[ko]}")

out = new_body.rstrip() + "\n\n" + "\n".join(new_refs_lines) + "\n"
open(SRC, "w", encoding="utf-8").write(out)

# Verify serial ascending order of first appearances
seq = [int(x) for x in re.findall(r'\[(\d+)\]', new_body)]
first_seen = []
seen = set()
for s in seq:
    if s not in seen:
        seen.add(s); first_seen.append(s)
print("first-appearance order:", first_seen)
print("is strictly ascending by first appearance:", first_seen == sorted(first_seen))
print("total distinct refs:", len(seen))
print("max citation:", max(seq))
