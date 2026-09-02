#!/usr/bin/env python3
"""Convert Chapter_Economic_Analysis_HRES.md to a Word .docx using only the
Python standard library (no python-docx / pandoc required).

A .docx is a ZIP container of Open XML parts. We emit a minimal but valid
WordprocessingML document that Microsoft Word, LibreOffice, and Google Docs
open cleanly. Supported Markdown: headings (#..######), paragraphs, bold
(**..**), italic (*..*), inline code (`..`), block equations ($$..$$),
GitHub-style tables, image lines (rendered as an italic placeholder), and
horizontal rules.
"""

import html
import re
import zipfile
from pathlib import Path

SRC = Path(__file__).parent / "Chapter_Economic_Analysis_HRES.md"
OUT = Path(__file__).parent / "HRES_Economic_Analysis_Chapter.docx"

# ----------------------------------------------------------------------------
# Inline run generation
# ----------------------------------------------------------------------------

def xml_escape(text: str) -> str:
    return html.escape(text, quote=False)


def make_run(text: str, *, bold=False, italic=False, mono=False) -> str:
    if text == "":
        return ""
    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if mono:
        rpr.append('<w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>')
    rpr_xml = f"<w:rPr>{''.join(rpr)}</w:rPr>" if rpr else ""
    # xml:space=preserve keeps leading/trailing spaces in runs
    return (
        f"<w:r>{rpr_xml}"
        f'<w:t xml:space="preserve">{xml_escape(text)}</w:t></w:r>'
    )


# Tokenize inline markdown into styled runs.
INLINE_RE = re.compile(
    r"(\*\*.+?\*\*)"       # bold
    r"|(`[^`]+`)"          # inline code
    r"|(\*[^*]+?\*)"       # italic
)


def inline_runs(text: str) -> str:
    out = []
    pos = 0
    for m in INLINE_RE.finditer(text):
        if m.start() > pos:
            out.append(make_run(text[pos:m.start()]))
        tok = m.group(0)
        if tok.startswith("**"):
            out.append(make_run(tok[2:-2], bold=True))
        elif tok.startswith("`"):
            out.append(make_run(tok[1:-1], mono=True))
        else:  # *italic*
            out.append(make_run(tok[1:-1], italic=True))
        pos = m.end()
    if pos < len(text):
        out.append(make_run(text[pos:]))
    return "".join(out)


# ----------------------------------------------------------------------------
# Block-level paragraph builders
# ----------------------------------------------------------------------------

def para(runs_xml: str, *, style=None, jc=None, spacing_after=120) -> str:
    ppr = []
    if style:
        ppr.append(f'<w:pStyle w:val="{style}"/>')
    if jc:
        ppr.append(f'<w:jc w:val="{jc}"/>')
    ppr.append(f'<w:spacing w:after="{spacing_after}"/>')
    ppr_xml = f"<w:pPr>{''.join(ppr)}</w:pPr>"
    return f"<w:p>{ppr_xml}{runs_xml}</w:p>"


def heading(text: str, level: int) -> str:
    sizes = {1: 36, 2: 30, 3: 26, 4: 23, 5: 21, 6: 20}
    sz = sizes.get(level, 22)
    run = (
        f"<w:r><w:rPr><w:b/><w:sz w:val='{sz}'/>"
        f"<w:color w:val='1F3864'/></w:rPr>"
        f"<w:t xml:space='preserve'>{xml_escape(text)}</w:t></w:r>"
    )
    return (
        f"<w:p><w:pPr><w:spacing w:before='240' w:after='120'/>"
        f"<w:keepNext/></w:pPr>{run}</w:p>"
    )


def equation_para(eq: str) -> str:
    # Render LaTeX-ish block equation centered in monospace as a faithful,
    # editable placeholder (true OMML conversion is out of scope for stdlib).
    run = (
        f"<w:r><w:rPr><w:rFonts w:ascii='Cambria Math' w:hAnsi='Cambria Math'/>"
        f"<w:i/></w:rPr>"
        f"<w:t xml:space='preserve'>{xml_escape(eq)}</w:t></w:r>"
    )
    return (
        f"<w:p><w:pPr><w:jc w:val='center'/>"
        f"<w:spacing w:before='120' w:after='120'/></w:pPr>{run}</w:p>"
    )


def hr_para() -> str:
    return (
        "<w:p><w:pPr><w:pBdr>"
        "<w:bottom w:val='single' w:sz='6' w:space='1' w:color='auto'/>"
        "</w:pBdr></w:pPr></w:p>"
    )


def table_block(rows):
    # rows: list[list[str]]; first row is header.
    def cell(text, header=False):
        runs = inline_runs(text.strip()) or make_run("")
        shd = "<w:shd w:val='clear' w:fill='D9E2F3'/>" if header else ""
        return (
            "<w:tc><w:tcPr>"
            "<w:tcBorders>"
            "<w:top w:val='single' w:sz='4' w:color='808080'/>"
            "<w:left w:val='single' w:sz='4' w:color='808080'/>"
            "<w:bottom w:val='single' w:sz='4' w:color='808080'/>"
            "<w:right w:val='single' w:sz='4' w:color='808080'/>"
            "</w:tcBorders>"
            f"{shd}</w:tcPr>"
            f"<w:p><w:pPr><w:spacing w:after='40'/></w:pPr>{runs}</w:p></w:tc>"
        )

    body = []
    for i, r in enumerate(rows):
        cells = "".join(cell(c, header=(i == 0)) for c in r)
        body.append(f"<w:tr>{cells}</w:tr>")
    return (
        "<w:tbl><w:tblPr>"
        "<w:tblW w:w='5000' w:type='pct'/>"
        "<w:tblBorders>"
        "<w:top w:val='single' w:sz='4' w:color='808080'/>"
        "<w:bottom w:val='single' w:sz='4' w:color='808080'/>"
        "</w:tblBorders>"
        "</w:tblPr>" + "".join(body) + "</w:tbl>"
        "<w:p><w:pPr><w:spacing w:after='120'/></w:pPr></w:p>"
    )


# ----------------------------------------------------------------------------
# Markdown parser (line-oriented, block-aware)
# ----------------------------------------------------------------------------

def parse_markdown(md: str):
    lines = md.split("\n")
    body = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Blank line
        if stripped == "":
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"-{3,}", stripped):
            body.append(hr_para())
            i += 1
            continue

        # Heading
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            body.append(heading(m.group(2).strip(), len(m.group(1))))
            i += 1
            continue

        # Block equation $$ ... $$ (possibly multi-line)
        if stripped.startswith("$$"):
            eq_lines = []
            content = stripped
            if content.count("$$") >= 2:
                eq = content.strip("$").strip()
                body.append(equation_para(eq))
                i += 1
                continue
            eq_lines.append(content.lstrip("$"))
            i += 1
            while i < n and "$$" not in lines[i]:
                eq_lines.append(lines[i])
                i += 1
            if i < n:
                eq_lines.append(lines[i].split("$$")[0])
                i += 1
            body.append(equation_para(" ".join(s.strip() for s in eq_lines).strip()))
            continue

        # Table (line with pipes followed by separator row)
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", lines[i + 1]):
            rows = []
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(header)
            i += 2  # skip header + separator
            while i < n and "|" in lines[i] and lines[i].strip():
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                rows.append(cells)
                i += 1
            body.append(table_block(rows))
            continue

        # Image line: ![alt](path)
        mimg = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", stripped)
        if mimg:
            alt = mimg.group(1) or "Figure"
            path = mimg.group(2)
            run = make_run(f"[Image: {alt} — {path}]", italic=True)
            body.append(para(run, jc="center"))
            i += 1
            continue

        # Bullet list item
        mb = re.match(r"^\s*[-*]\s+(.*)$", line)
        if mb:
            run = make_run("•  ") + inline_runs(mb.group(1).strip())
            body.append(para(run, spacing_after=60))
            i += 1
            continue

        # Numbered list item
        mn = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
        if mn:
            run = make_run(f"{mn.group(1)}.  ") + inline_runs(mn.group(2).strip())
            body.append(para(run, spacing_after=60))
            i += 1
            continue

        # Regular paragraph (accumulate wrapped lines until blank/block)
        buf = [line]
        i += 1
        while i < n and lines[i].strip() != "" and not re.match(
            r"^(#{1,6}\s|-{3,}$|\$\$|\s*[-*]\s|\s*\d+\.\s|!\[)", lines[i]
        ) and "|" not in lines[i]:
            buf.append(lines[i])
            i += 1
        text = " ".join(s.strip() for s in buf)
        body.append(para(inline_runs(text)))

    return "".join(body)


# ----------------------------------------------------------------------------
# DOCX packaging
# ----------------------------------------------------------------------------

CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>"""

ROOT_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""


def build_document_xml(body_xml: str) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        "<w:body>"
        + body_xml
        + '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
        '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440"'
        ' w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>'
        "</w:body></w:document>"
    )


def main():
    md = SRC.read_text(encoding="utf-8")
    body_xml = parse_markdown(md)
    document_xml = build_document_xml(body_xml)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("word/document.xml", document_xml)

    print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
