#!/usr/bin/env python3
"""
Build a single, properly formatted Word (.docx) document that compiles all the
"Call for Book Chapters" flyers.

No third-party dependencies: a .docx is a ZIP of OOXML parts, so we build the
XML by hand. Supports Title, Heading 1/2/3, normal paragraphs, bold/italic runs,
bullet and numbered lists, and page breaks.
"""

import zipfile
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------
# Low-level OOXML helpers
# --------------------------------------------------------------------------

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def _esc(text):
    return escape(str(text))


def _runs_xml(segments):
    """segments: list of (text, {bold, italic, color}) tuples -> run XML."""
    out = []
    for text, props in segments:
        rpr = []
        if props.get('bold'):
            rpr.append('<w:b/>')
        if props.get('italic'):
            rpr.append('<w:i/>')
        if props.get('color'):
            rpr.append('<w:color w:val="%s"/>' % props['color'])
        if props.get('size'):
            # size in half-points
            rpr.append('<w:sz w:val="%d"/>' % props['size'])
        rpr_xml = '<w:rPr>%s</w:rPr>' % ''.join(rpr) if rpr else ''
        out.append(
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
            % (rpr_xml, _esc(text))
        )
    return ''.join(out)


class Doc:
    def __init__(self):
        self.body = []

    def _p(self, runs_xml, style=None, numpr=None, spacing_after=None):
        ppr = []
        if style:
            ppr.append('<w:pStyle w:val="%s"/>' % style)
        if numpr:
            ilvl, numid = numpr
            ppr.append(
                '<w:numPr><w:ilvl w:val="%d"/><w:numId w:val="%d"/></w:numPr>'
                % (ilvl, numid)
            )
        if spacing_after is not None:
            ppr.append('<w:spacing w:after="%d"/>' % spacing_after)
        ppr_xml = '<w:pPr>%s</w:pPr>' % ''.join(ppr) if ppr else ''
        self.body.append('<w:p>%s%s</w:p>' % (ppr_xml, runs_xml))

    def title(self, text):
        self._p(_runs_xml([(text, {})]), style='Title')

    def subtitle(self, text):
        self._p(_runs_xml([(text, {'italic': True})]), style='Subtitle')

    def h1(self, text):
        self._p(_runs_xml([(text, {})]), style='Heading1')

    def h2(self, text):
        self._p(_runs_xml([(text, {})]), style='Heading2')

    def h3(self, text):
        self._p(_runs_xml([(text, {})]), style='Heading3')

    def para(self, segments):
        """segments may be a plain string or a list of (text, props)."""
        if isinstance(segments, str):
            segments = [(segments, {})]
        self._p(_runs_xml(segments))

    def label(self, label, value):
        """A 'Label: value' paragraph with bold label."""
        self._p(_runs_xml([(label + ': ', {'bold': True}), (value, {})]))

    def bullet(self, text, level=0):
        self._p(_runs_xml([(text, {})]), numpr=(level, 1))

    def number(self, text, level=0):
        self._p(_runs_xml([(text, {})]), numpr=(level, 2))

    def spacer(self):
        self._p('')

    def page_break(self):
        self.body.append(
            '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'
        )

    # ------------------------------------------------------------------
    def document_xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:document xmlns:w="%s">'
            '<w:body>%s'
            '<w:sectPr>'
            '<w:pgSz w:w="12240" w:h="15840"/>'
            '<w:pgMar w:top="1440" w:right="1440" w:bottom="1440" '
            'w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>'
            '</w:sectPr>'
            '</w:body></w:document>'
        ) % (W, ''.join(self.body))


# --------------------------------------------------------------------------
# Static OOXML parts
# --------------------------------------------------------------------------

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/word/numbering.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/numbering" Target="numbering.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr>
<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal">
<w:name w:val="Normal"/><w:pPr><w:spacing w:after="120" w:line="276" w:lineRule="auto"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title">
<w:name w:val="Title"/><w:pPr><w:spacing w:after="120"/><w:jc w:val="center"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/><w:b/><w:color w:val="1F3864"/><w:sz w:val="52"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle">
<w:name w:val="Subtitle"/><w:pPr><w:spacing w:after="240"/><w:jc w:val="center"/></w:pPr>
<w:rPr><w:color w:val="595959"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1">
<w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:keepNext/><w:spacing w:before="360" w:after="120"/>
<w:pBdr><w:bottom w:val="single" w:sz="12" w:space="4" w:color="2E74B5"/></w:pBdr></w:pPr>
<w:rPr><w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/><w:b/><w:color w:val="1F3864"/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2">
<w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="60"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Calibri Light" w:hAnsi="Calibri Light"/><w:b/><w:color w:val="2E74B5"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3">
<w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/>
<w:pPr><w:keepNext/><w:spacing w:before="160" w:after="40"/></w:pPr>
<w:rPr><w:b/><w:color w:val="404040"/><w:sz w:val="23"/></w:rPr></w:style>
</w:styles>'''

# numId 1 = bullet, numId 2 = decimal (with sub-levels)
NUMBERING = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:abstractNum w:abstractNumId="0">
<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="&#8226;"/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Symbol" w:hAnsi="Symbol" w:hint="default"/></w:rPr></w:lvl>
<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="o"/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr>
<w:rPr><w:rFonts w:ascii="Courier New" w:hAnsi="Courier New" w:hint="default"/></w:rPr></w:lvl>
</w:abstractNum>
<w:abstractNum w:abstractNumId="1">
<w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl>
<w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="lowerLetter"/><w:lvlText w:val="%2."/><w:lvlJc w:val="left"/>
<w:pPr><w:ind w:left="1440" w:hanging="360"/></w:pPr></w:lvl>
</w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>'''

CORE = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:title>Call for Book Chapters - Consolidated Compilation</dc:title>
<dc:creator>Compilation</dc:creator>
</cp:coreProperties>'''

APP = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">
<Application>Python OOXML Builder</Application>
</Properties>'''


def write_docx(path, doc):
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', CONTENT_TYPES)
        z.writestr('_rels/.rels', RELS)
        z.writestr('word/_rels/document.xml.rels', DOC_RELS)
        z.writestr('word/document.xml', doc.document_xml())
        z.writestr('word/styles.xml', STYLES)
        z.writestr('word/numbering.xml', NUMBERING)
        z.writestr('docProps/core.xml', CORE)
        z.writestr('docProps/app.xml', APP)


# --------------------------------------------------------------------------
# Content: one entry helper per book call
# --------------------------------------------------------------------------

def add_book(doc, idx, title, publisher, about=None, editors=None,
             sections=None, chapters=None, topics_flat=None, dates=None,
             submission=None, guidelines=None, notes=None, indexing=None):
    doc.h1('%d. %s' % (idx, title))
    if publisher:
        doc.para([('Publisher: ', {'bold': True}), (publisher, {})])
    if indexing:
        doc.para([('Indexing / Series: ', {'bold': True}), (indexing, {})])
    if about:
        doc.h3('About the Book')
        doc.para(about)
    if editors:
        doc.h3('Editors')
        for e in editors:
            doc.bullet(e)
    if sections:
        doc.h3('Proposed Chapters')
        for sec_name, items in sections:
            doc.h3(sec_name) if False else doc.para([(sec_name, {'bold': True})])
            for it in items:
                doc.number(it)
    if chapters:
        doc.h3('Proposed / Tentative Chapters')
        for c in chapters:
            doc.number(c)
    if topics_flat:
        doc.h3('Suggested Topics')
        for t in topics_flat:
            doc.bullet(t)
    if guidelines:
        doc.h3('Submission Guidelines')
        for g in guidelines:
            doc.bullet(g)
    if dates:
        doc.h3('Important Dates')
        for label, val in dates:
            doc.para([(label + ': ', {'bold': True}), (val, {})])
    if submission:
        doc.h3('Submission')
        for label, val in submission:
            doc.para([(label + ': ', {'bold': True}), (val, {})])
    if notes:
        doc.h3('Notes')
        for n in notes:
            doc.bullet(n)


if __name__ == '__main__':
    from calls_data import build
    doc = Doc()
    build(doc, add_book)
    write_docx('/projects/sandbox/AMMAN/Call_for_Book_Chapters_Compilation.docx', doc)
    print('Wrote Call_for_Book_Chapters_Compilation.docx')
