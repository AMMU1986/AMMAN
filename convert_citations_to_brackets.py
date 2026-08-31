#!/usr/bin/env python3
"""
Convert Chapter 5 in-text citations from APA (Author, Year) style to numbered
square-bracket [n] style (IEEE / Vancouver), numbered by order of first
appearance, and rebuild the reference list as a numbered [n] list.

Strategy
--------
Each unique source is given a canonical KEY (author-token + year, e.g.
"sharma&chhibber2019a"). We assign numbers in order of first appearance while
scanning the body text. Both narrative citations ("Kumar and Chhibber (2022)")
and parenthetical citations ("(Kumar & Chhibber, 2022)") map to the same KEY.

The reference-list block (after the "## References" heading) is used to build
the KEY -> full-reference-text map, so the renumbered list preserves the exact
wording of every entry.
"""

import re
import os

SRC = '/projects/sandbox/AMMAN/Chapter_5_Results_and_Discussion.md'


# ---------------------------------------------------------------------------
# 1.  KEY builder: normalize an author string + year into a canonical key.
# ---------------------------------------------------------------------------
STOP = {'and', 'the', 'a', 'of', 'j', 'l', 'r', 'k', 's', 'p', 't', 'h', 'b',
        'c', 'd', 'e', 'f', 'g', 'i', 'm', 'n', 'o', 'u', 'v', 'w', 'x', 'y', 'z'}


def norm_authors(auth):
    """Reduce an author string to the FIRST surname token only.

    This is applied identically to narrative citations ("Kim et al."), grouped
    parentheticals ("Kim et al., 2015"), and reference-list author strings
    ("Kim, J. B., Choi, J. K., Han, I. W., & Sohn, I."), so all three forms map
    to the same key. First surname + year (with APA disambiguation letters) is
    sufficient to uniquely identify every source in this chapter.
    """
    a = auth.lower()
    a = a.replace('&', ' ')
    a = re.sub(r'\bet al\.?\b', '', a)
    # Reference-list form is "Surname, Initials, ..." -> take text before 1st comma
    a = a.split(',')[0]
    a = re.sub(r'[^a-zà-ÿ ]', ' ', a)       # drop punctuation/initials
    toks = [t for t in a.split() if t not in STOP and len(t) > 1]
    return toks[0] if toks else ''


def make_key(auth, year):
    return f'{norm_authors(auth)}|{year}'


# ---------------------------------------------------------------------------
# 2.  Parse the reference list into ordered (key, full_text) records.
# ---------------------------------------------------------------------------
def parse_reference_list(ref_block):
    """Return list of (key, plain_key_variants, full_markdown_text)."""
    entries = []
    for line in ref_block.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Extract authors (up to the year in parens) and the year token.
        m = re.match(r'^(.*?)\((\d{4}[a-z]?)\)\.', line)
        if not m:
            continue
        authors_raw = m.group(1).strip().rstrip('(').strip()
        year = m.group(2)
        key = make_key(authors_raw, year)
        entries.append((key, authors_raw, year, line))
    return entries


# ---------------------------------------------------------------------------
# 3.  Citation replacement.
# ---------------------------------------------------------------------------
class Numberer:
    def __init__(self):
        self.order = []          # keys in first-appearance order
        self.num = {}            # key -> number

    def get(self, key):
        if key not in self.num:
            self.order.append(key)
            self.num[key] = len(self.order)
        return self.num[key]


def build():
    with open(SRC, encoding='utf-8') as f:
        text = f.read()

    body, ref_block = text.split('## References', 1)
    ref_entries = parse_reference_list(ref_block)

    # Map from canonical key -> full text (last wins if dup, but keys are unique)
    key_to_full = {k: full for (k, _a, _y, full) in ref_entries}

    numb = Numberer()

    def emit(keys):
        nums = sorted({numb.get(k) for k in keys})
        return '[' + ', '.join(str(n) for n in nums) + ']'

    # Helper to resolve an author+year(-with-optional-letter) to a key that
    # exists in the reference list; falls back to a constructed key.
    def resolve(auth, year):
        k = make_key(auth, year)
        if k in key_to_full:
            return k
        # Fall back: same first surname, same 4-digit year ignoring a/b/c letter
        base_year = year[:4]
        first = norm_authors(auth)
        for cand in key_to_full:
            ca, cy = cand.split('|')
            if ca == first and cy[:4] == base_year:
                return cand
        return k  # constructed (will surface as missing if truly absent)

    # A single author-year unit inside a parenthetical, e.g.
    #   "Sharma & Chhibber, 2019a", "Kim et al., 2015", "Kou, 2003"
    # Author part: a first surname optionally followed by additional surnames
    # joined by ", ", " & ", " and ", and optionally terminated by " et al.".
    author = (r'[A-Z][A-Za-zÀ-ÿ.\'\-]+'
              r'(?:, [A-Z][A-Za-zÀ-ÿ.\'\-]+)*'
              r'(?:,? (?:&|and) [A-Z][A-Za-zÀ-ÿ.\'\-]+)?'
              r'(?: et al\.)?')
    unit_re = re.compile(
        r'(' + author + r'),\s*'
        r'((?:19|20)\d{2}[a-z]?(?:\s*,\s*(?:19|20)\d{2}[a-z]?)*)'
    )

    # Parenthetical citation group: (...) containing >= 1 four-digit year.
    paren_re = re.compile(r'\(([^()]*?\b(?:19|20)\d{2}[a-z]?[^()]*?)\)')

    # Narrative citation: "Author(s) (Year[, Year...])".
    narr_re = re.compile(
        r'([A-Z][A-Za-zÀ-ÿ.\'\-]+'
        r'(?:,? (?:&|and) [A-Z][A-Za-zÀ-ÿ.\'\-]+'
        r'|, [A-Z][A-Za-zÀ-ÿ.\'\-]+'
        r'| et al\.)*)'
        r'\s\(((?:19|20)\d{2}[a-z]?(?:\s*,\s*(?:19|20)\d{2}[a-z]?)*)\)'
    )

    # ------------------------------------------------------------------
    # Single left-to-right pass: collect every citation match (narrative
    # and parenthetical) with its span, then process them in reading order
    # so reference numbers follow true text position (IEEE convention).
    # ------------------------------------------------------------------
    matches = []  # (start, end, kind, match_obj)

    for m in narr_re.finditer(body):
        matches.append((m.start(), m.end(), 'narr', m))

    for m in paren_re.finditer(body):
        inner = m.group(1)
        chunks = [c.strip() for c in inner.split(';')]
        cite_chunks = [c for c in chunks if unit_re.fullmatch(c)]
        if not cite_chunks:
            continue
        if len(cite_chunks) == len(chunks):
            matches.append((m.start(), m.end(), 'paren', m))       # pure citation group
        else:
            matches.append((m.start(), m.end(), 'paren_mixed', m))  # figure/text + citations

    # Sort by start position; drop parenthetical matches that overlap a
    # narrative match (they won't here, but guard anyway) and de-overlap.
    matches.sort(key=lambda t: (t[0], -(t[1] - t[0])))
    selected = []
    last_end = -1
    for start, end, kind, m in matches:
        if start < last_end:
            continue  # overlaps a previously selected match
        selected.append((start, end, kind, m))
        last_end = end

    # Assign numbers in reading order and build replacement strings.
    pieces = []
    cursor = 0
    for start, end, kind, m in selected:
        pieces.append(body[cursor:start])
        if kind == 'narr':
            auth = m.group(1).strip()
            years = re.findall(r'(?:19|20)\d{2}[a-z]?', m.group(2))
            keys = [resolve(auth, y) for y in years]
            pieces.append(f'{auth} {emit(keys)}')
        elif kind == 'paren':  # pure citation parenthetical
            inner = m.group(1)
            keys = []
            for c in (x.strip() for x in inner.split(';')):
                um = unit_re.fullmatch(c)
                auth = um.group(1).strip()
                for y in re.findall(r'(?:19|20)\d{2}[a-z]?', um.group(2)):
                    keys.append(resolve(auth, y))
            pieces.append(emit(keys))
        else:  # paren_mixed: keep non-citation chunks, convert citation chunks
            inner = m.group(1)
            kept = []
            keys = []
            for c in (x.strip() for x in inner.split(';')):
                um = unit_re.fullmatch(c)
                if um:
                    auth = um.group(1).strip()
                    for y in re.findall(r'(?:19|20)\d{2}[a-z]?', um.group(2)):
                        keys.append(resolve(auth, y))
                else:
                    kept.append(c)
            pieces.append('(' + '; '.join(kept) + ' ' + emit(keys) + ')')
        cursor = end
    pieces.append(body[cursor:])
    body = ''.join(pieces)

    # ----- 4. Rebuild the reference list in citation order ------------------
    lines_out = ['## References', '']
    used = set()
    for idx, key in enumerate(numb.order, start=1):
        full = key_to_full.get(key)
        if full is None:
            lines_out.append(f'[{idx}] (MISSING REFERENCE for key: {key})')
            continue
        # strip the leading author/year? No - keep full APA text, just prefix [n].
        lines_out.append(f'[{idx}] {full}')
        lines_out.append('')
        used.add(key)

    new_text = body.rstrip() + '\n\n' + '\n'.join(lines_out) + '\n'

    with open(SRC, 'w', encoding='utf-8') as f:
        f.write(new_text)

    # ----- 5. Report --------------------------------------------------------
    print(f'Assigned {len(numb.order)} numbered references (by first appearance).')
    missing = [k for k in numb.order if k not in key_to_full]
    if missing:
        print('WARNING: keys with no matching reference entry:')
        for k in missing:
            print('   ', k)
    # remaining in-text APA-looking citations?
    leftover = re.findall(r'\([A-Z][A-Za-z.\'\-]+,?\s+(?:19|20)\d{2}', body)
    print(f'Leftover APA-style parentheticals: {len(leftover)}')
    for l in leftover[:15]:
        print('   ', l)


if __name__ == '__main__':
    build()
