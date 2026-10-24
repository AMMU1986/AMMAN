#!/usr/bin/env python3
"""Build a Word .docx (no external deps) with the Staff Graded Assignment solutions."""
import zipfile
from xml.sax.saxutils import escape

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def run(text, bold=False, italic=False, size=None):
    rpr = ""
    props = ""
    if bold: props += '<w:b/>'
    if italic: props += '<w:i/>'
    if size: props += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
    if props:
        rpr = f'<w:rPr>{props}</w:rPr>'
    return (f'<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r>')

def para(runs, align=None, space_after=120):
    ppr = f'<w:spacing w:after="{space_after}"/>'
    if align:
        ppr += f'<w:jc w:val="{align}"/>'
    return f'<w:p><w:pPr>{ppr}</w:pPr>{"".join(runs)}</w:p>'

def h1(text):
    return para([run(text, bold=True, size=32)], space_after=160)

def h2(text):
    return para([run(text, bold=True, size=26)], space_after=120)

def body(text):
    return para([run(text, size=22)])

def bodyruns(runs):
    return para(runs)

paras = []
paras.append(para([run("Computer Architecture — Staff Graded Assignment", bold=True, size=36)], align="center", space_after=80))
paras.append(para([run("Solution Document", italic=True, size=24)], align="center", space_after=80))
paras.append(para([run("Student ID: <your_student_ID_here>", bold=True, size=22)], align="center", space_after=240))

# ---- Q1 ----
paras.append(h1("1. Performance and Amdahl's Law (8 points)"))
paras.append(body("Time fractions: Memory = 0.40, ALU = 0.30, Branches = 0.30."))
paras.append(body("Amdahl's Law:  Speedup = 1 / [ (1 - f) + f/s ],  where f = fraction enhanced and s = local speedup of that fraction."))
paras.append(h2("(a) Only one enhancement"))
paras.append(body("Enhancement 1 — memory x2:"))
paras.append(body("   S1 = 1 / [ (1 - 0.40) + 0.40/2 ] = 1 / (0.60 + 0.20) = 1 / 0.80 = 1.25"))
paras.append(body("Enhancement 2 — ALU x3:"))
paras.append(body("   S2 = 1 / [ (1 - 0.30) + 0.30/3 ] = 1 / (0.70 + 0.10) = 1 / 0.80 = 1.25"))
paras.append(bodyruns([run("Result: both enhancements give the same overall speedup of 1.25x.", bold=True, size=22)]))
paras.append(body("Memory has the larger time share (0.40) but smaller local speedup (2); ALU has the smaller share (0.30) but larger local speedup (3). The two effects cancel, so neither is preferable on speedup alone."))
paras.append(h2("(b) Both enhancements applied together"))
paras.append(body("Each enhanced fraction shrinks independently; the un-enhanced branch fraction stays:"))
paras.append(body("   T_new = 0.30 (branch) + 0.40/2 (mem) + 0.30/3 (ALU) = 0.30 + 0.20 + 0.10 = 0.60"))
paras.append(bodyruns([run("   Overall Speedup = 1 / 0.60 = 1.667x  (approximately 1.67x)", bold=True, size=22)]))

# ---- Q2 ----
paras.append(h1("2. MIPS Instruction Formats (10 points)"))
paras.append(body("Register numbers: $t0 = 8, $t1 = 9, $t2 = 10."))
paras.append(h2("(a) Instruction type and (b) fields"))
paras.append(body("add $t0, $t1, $t2  ->  R-type"))
paras.append(body("   op = 0, rs = 9 ($t1), rt = 10 ($t2), rd = 8 ($t0), shamt = 0, funct = 0x20"))
paras.append(body("lw $t0, 12($t1)  ->  I-type"))
paras.append(body("   op = 0x23, rs = 9 ($t1 base), rt = 8 ($t0 dest), immediate = 12"))
paras.append(body("beq $t0, $t1, Label  ->  I-type"))
paras.append(body("   op = 0x04, rs = 8 ($t0), rt = 9 ($t1), immediate = branch offset (in words)"))
paras.append(body("j Label  ->  J-type"))
paras.append(body("   op = 0x02, address = 26-bit word target"))
paras.append(h2("Field roles"))
paras.append(body("R-type (6+5+5+5+5+6): op selects R-format; rs, rt are source registers; rd is destination; shamt is shift amount; funct selects the exact ALU op (0x20 = add)."))
paras.append(body("I-type (6+5+5+16): op identifies the instruction; rs is base/first source; rt is destination (lw) or compare source (beq); the 16-bit immediate is a sign-extended offset."))
paras.append(body("J-type (6+26): op identifies the jump; the 26-bit field is shifted left 2 and joined with the top 4 bits of PC to form the target address."))
paras.append(h2("(c) Purpose of each instruction"))
paras.append(body("add  : integer addition, $t0 = $t1 + $t2."))
paras.append(body("lw   : load a word from memory at address ($t1 + 12) into $t0."))
paras.append(body("beq  : branch to Label if $t0 == $t1, else fall through."))
paras.append(body("j    : unconditional jump to Label."))

# ---- Q3 ----
paras.append(h1("3. Processor Addressing and IEEE-754 Floating Point (10 points)"))
paras.append(h2("(a) Decoder for a 4-KB byte-addressable memory"))
paras.append(body("4 KB = 4096 = 2^12 byte locations, so 12 bits are needed to address every location."))
paras.append(bodyruns([run("   Input lines  m = 12   (because 2^12 = 4096)", bold=True, size=22)]))
paras.append(bodyruns([run("   Output lines n = 4096 (one select line per location)", bold=True, size=22)]))
paras.append(body("It is a 12-to-4096 decoder. The processor's 8-bit data width does not affect the address decoder; address lines depend on the number of locations, not on word size."))
paras.append(h2("(b) IEEE-754 single precision"))
paras.append(body("Pattern: 1000 0000 0001 1111 0000 0000 0000 1111"))
paras.append(body("Regroup as Sign | Exponent(8) | Fraction(23):"))
paras.append(body("   1 | 0000 0000 | 001 1111 0000 0000 0000 1111"))
paras.append(body("Sign S = 1  ->  negative."))
paras.append(body("Exponent field E = 00000000 = 0."))
paras.append(body("Fraction F = 0011111000000000000 1111."))
paras.append(bodyruns([run("Key point: E = 0 with F != 0 means this is a SUBNORMAL (denormalized) number.", bold=True, size=22)]))
paras.append(body("For subnormals:  value = (-1)^S x 0.F x 2^(-126).  The implicit leading bit is 0 and the exponent is fixed at -126 (the bias of 127 only applies to normalized numbers, E = 1..254)."))
paras.append(body("Significand: set fraction bits = 2^20+2^19+2^18+2^17+2^16 + 2^3+2^2+2^1+2^0 = 2,031,616 + 15 = 2,031,631."))
paras.append(body("   0.F = 2,031,631 / 2^23 = 2,031,631 / 8,388,608 = 0.24219 (approx)."))
paras.append(bodyruns([run("   Value = -0.24219 x 2^(-126) = -2.85 x 10^-39 (approximately).", bold=True, size=22)]))
paras.append(body("How each part is read: the sign is the MSB; the bias is 127 but applies only to normalized numbers; since E = 0 here the number is subnormal, so the fixed exponent -126 is used with no implicit leading 1."))

body_xml = "".join(paras)
document = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    f'<w:document xmlns:w="{W}">'
    f'<w:body>{body_xml}'
    '<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
    '<w:pgMar w:top="1440" w:bottom="1440" w:left="1440" w:right="1440"/></w:sectPr>'
    '</w:body></w:document>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '</Types>'
)

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>'
)

out = "Staff_Graded_Assignment_Solutions.docx"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document)
print("wrote", out)
