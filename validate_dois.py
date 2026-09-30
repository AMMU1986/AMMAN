#!/usr/bin/env python3
"""
Structural / consistency validation of the publication DOIs.

This does NOT resolve DOIs over the network (not possible in this sandbox).
It checks:
  1. DOI syntax  (must match ^10\.\d{4,9}/\S+$)
  2. Registrant prefix vs. the stated journal/venue (does the prefix belong to
     the expected publisher?). Flags mismatches for human review.
"""
import json, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(BASE, "publications_full_data.json")))

# venue (lowercased substring) -> expected DOI prefix(es) and label
# Known registrant prefixes:
#   10.1007  Springer         10.1515  De Gruyter      10.3390 MDPI
#   10.1038  Nature/Springer  10.1109  IEEE            10.1063 AIP
#   10.1016  Elsevier         10.1186  Springer(BMC)   10.1002 Wiley
#   10.1049  IET/Wiley        10.1108  Emerald         10.1088 IOP
#   10.1134  Pleiades/Springer 10.5269 BSPM(SPM-UEM)  10.13005 Biomed&Pharm J
#   10.3233  IOS Press        10.1201  CRC/Taylor&Francis
#   10.52209 (Karaganda/MMET) 10.35377 Sakarya Univ   10.26782 JMCMS
#   10.23919 IEEE(INDIACom)
EXPECT = {
    "journal of optical communications": (["10.1515"], "De Gruyter"),
    "material and mechanical engineering technology": (["10.52209"], "MMET (Karaganda)"),
    "lecture notes in networks and systems": (["10.1007"], "Springer"),
    "iccccm": (["10.1109"], "IEEE"),
    "archives of computational methods": (["10.1007"], "Springer"),
    "international journal of materials research": (["10.1515"], "De Gruyter"),
    "main group chemistry": (["10.3233"], "IOS Press"),
    "iran journal of computer science": (["10.1007"], "Springer"),
    "biomedical and pharmacology journal": (["10.13005"], "Biomed & Pharm J"),
    "aip conference proceedings": (["10.1063"], "AIP"),
    "icdsis": (["10.1109"], "IEEE"),
    "national academy science letters": (["10.1007"], "Springer"),
    "indiacom": (["10.23919", "10.1109"], "IEEE"),
    "eaic": (["10.1109"], "IEEE"),
    "micromachines": (["10.3390"], "MDPI"),
    "next materials": (["10.1016"], "Elsevier"),
    "springer proceedings in physics": (["10.1007"], "Springer"),
    "iccmc": (["10.1109"], "IEEE"),
    "eurasip journal": (["10.1186"], "Springer"),
    "icimia": (["10.1109"], "IEEE"),
    "lecture notes in mechanical engineering": (["10.1007"], "Springer"),
    "wireless personal communications": (["10.1007"], "Springer"),
    "palestine journal of mathematics": (["10.5269"], "SPM/BSPM"),
    "incsst": (["10.1109"], "IEEE"),
    "iccds": (["10.1109"], "IEEE"),
    "lecture notes in electrical engineering": (["10.1007"], "Springer"),
    "ic2e3": (["10.1109"], "IEEE"),
    "smart materials and applications": (["10.1201"], "CRC/Taylor&Francis"),
    "chatbots and beyond": (["10.1002"], "Wiley"),
    "network modeling analysis": (["10.1007"], "Springer"),
    "chemical physics": (["10.1016"], "Elsevier"),
    "trends in mathematics": (["10.1007"], "Springer"),
    "scientific reports": (["10.1038"], "Nature"),
    "journal of physics: conference series": (["10.1088"], "IOP"),
    "boletim da sociedade paranaense": (["10.5269"], "SPM/BSPM"),
    "icccnp": (["10.1109"], "IEEE"),
    "iccams": (["10.1109"], "IEEE"),
    "energy reports": (["10.1016"], "Elsevier"),
    "world journal of engineering": (["10.1108"], "Emerald"),
    "engineering materials": (["10.1007"], "Springer"),
    "journal of materials science": (["10.1007"], "Springer"),
    "journal of mechanics of continua": (["10.26782"], "JMCMS"),
    "bioenergy research": (["10.1007"], "Springer"),
    "cises": (["10.1109"], "IEEE"),
    "iet intelligent transport": (["10.1049"], "IET/Wiley"),
    "sakarya university": (["10.35377"], "Sakarya Univ"),
    "arabian journal for science": (["10.1007"], "Springer"),
    "proceedings of the indian national science academy": (["10.1007"], "Springer"),
    "mechanics of solids": (["10.1134"], "Pleiades/Springer"),
    "giest": (["10.1109"], "IEEE"),
    "iot-siu": (["10.1109"], "IEEE"),
    "gitcon": (["10.1109"], "IEEE"),
    "aece": (["10.1109"], "IEEE"),
    "iceca": (["10.1109"], "IEEE"),
    "discover computing": (["10.1007"], "Springer"),
    "iatmsi": (["10.1109"], "IEEE"),
    "ietacs": (["10.1109"], "IEEE"),
    "iceteg": (["10.1109"], "IEEE"),
    "upwiecon": (["10.1109"], "IEEE"),
    "incowoco": (["10.1109"], "IEEE"),
    "icoiics": (["10.1109"], "IEEE"),
    "icosec": (["10.1109"], "IEEE"),
    "materials today communications": (["10.1016"], "Elsevier"),
    "franklin open": (["10.1016"], "Elsevier"),
    "journal of bio- and tribo-corrosion": (["10.1007"], "Springer"),
    "esci": (["10.1109"], "IEEE"),
    "results in optics": (["10.1016"], "Elsevier"),
    "mpcon": (["10.1109"], "IEEE"),
    "cipher": (["10.1109"], "IEEE"),
    "iitcee": (["10.1109"], "IEEE"),
    "icitiit": (["10.1109"], "IEEE"),
    "aimlcps": (["10.1109"], "IEEE"),
    "ic-eeta": (["10.1109"], "IEEE"),
    "vascular and endovascular review": (["10.15420", "10.15420/ver"], "Radcliffe/VER"),
    "optoelectronics and advanced materials": (["10."], "INOE/OAM-RC"),
}

# Map each row number to its venue string (from the manuscript list)
VENUE = {
 1:"journal of optical communications",2:"material and mechanical engineering technology",
 3:"lecture notes in networks and systems",4:"lecture notes in networks and systems",
 5:"lecture notes in networks and systems",6:"lecture notes in networks and systems",
 7:"lecture notes in networks and systems",8:"lecture notes in networks and systems",
 9:"iccccm",10:"lecture notes in networks and systems",11:"archives of computational methods",
 12:"international journal of materials research",13:"main group chemistry",
 14:"optoelectronics and advanced materials",15:"journal of optical communications",
 16:"iran journal of computer science",17:"biomedical and pharmacology journal",
 18:"aip conference proceedings",19:"aip conference proceedings",20:"aip conference proceedings",
 21:"aip conference proceedings",22:"aip conference proceedings",23:"aip conference proceedings",
 24:"aip conference proceedings",25:"aip conference proceedings",26:"aip conference proceedings",
 27:"otcon",28:"icdsis",29:"national academy science letters",30:"indiacom",31:"eaic",32:"eaic",
 33:"eaic",34:"archives of computational methods",35:"archives of computational methods",
 36:"micromachines",37:"national academy science letters",38:"next materials",
 39:"springer proceedings in physics",40:"iccmc",41:"eurasip journal",
 42:"national academy science letters",43:"vascular and endovascular review",44:"icimia",
 45:"lecture notes in mechanical engineering",46:"icimia",47:"archives of computational methods",
 48:"wireless personal communications",49:"journal of optical communications",
 50:"palestine journal of mathematics",51:"incsst",52:"incsst",53:"incsst",54:"iccds",
 55:"lecture notes in electrical engineering",56:"ic2e3",57:"smart materials and applications",
 58:"smart materials and applications",59:"smart materials and applications",60:"chatbots and beyond",
 61:"network modeling analysis",62:"chemical physics",63:"trends in mathematics",64:"scientific reports",
 65:"journal of physics: conference series",66:"boletim da sociedade paranaense",67:"icccnp",
 68:"iccams",69:"iccams",70:"iccams",71:"energy reports",72:"world journal of engineering",
 73:"microwave processing",74:"engineering materials",75:"journal of materials science",
 76:"national academy science letters",77:"journal of mechanics of continua",78:"bioenergy research",
 79:"lecture notes in electrical engineering",80:"cises",81:"cises",82:"cises",83:"cises",84:"cises",
 85:"cises",86:"cises",87:"cises",88:"lecture notes in electrical engineering",
 89:"iet intelligent transport",90:"lecture notes in electrical engineering",
 91:"aip conference proceedings",92:"aip conference proceedings",93:"sakarya university",
 94:"boletim da sociedade paranaense",95:"aip conference proceedings",96:"arabian journal for science",
 97:"national academy science letters",98:"archives of computational methods",
 99:"proceedings of the indian national science academy",100:"boletim da sociedade paranaense",
 101:"mechanics of solids",102:"giest",103:"iot-siu",104:"gitcon",105:"gitcon",106:"aece",
 107:"gitcon",108:"gitcon",109:"gitcon",110:"aece",111:"gitcon",112:"isssc",113:"ice2cpt",
 114:"iceca",115:"journal of mechanics of continua",116:"discover computing",
 117:"lecture notes in networks and systems",118:"iatmsi",119:"iatmsi",120:"iatmsi",121:"ietacs",
 122:"iceteg",123:"upwiecon",124:"incowoco",125:"icoiics",126:"icosec",
 127:"materials today communications",128:"franklin open",129:"franklin open",
 130:"journal of bio- and tribo-corrosion",131:"esci",132:"results in optics",133:"mpcon",
 134:"engineering materials",135:"cipher",136:"cipher",137:"cipher",138:"iitcee",139:"icitiit",
 140:"icitiit",141:"archives of computational methods",142:"ietacs",143:"ietacs",144:"aimlcps",
 145:"aimlcps",146:"aimlcps",147:"ic-eeta",148:"ic-eeta",149:"ic-eeta",150:"ic-eeta",
}

DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")

syntax_bad, prefix_mismatch, ok, blank = [], [], 0, []
for i in range(1, 151):
    rec = data.get(str(i), {})
    doi = rec.get("doi", "").strip()
    if not doi:
        blank.append(i); continue
    if not DOI_RE.match(doi):
        syntax_bad.append((i, doi)); continue
    prefix = doi.split("/")[0]
    venue = VENUE.get(i, "")
    exp = EXPECT.get(venue)
    if exp:
        prefixes, label = exp
        if not any(prefix == p or p == "10." for p in prefixes):
            prefix_mismatch.append((i, doi, prefix, label, venue))
        else:
            ok += 1
    else:
        ok += 1  # venue prefix rule unknown; syntax already OK

print(f"Total rows: 150")
print(f"DOIs present: {150 - len(blank)}  |  Blank (link-only / none): {len(blank)} -> {blank}")
print(f"Syntax OK & prefix consistent: {ok}")
print(f"\nSYNTAX PROBLEMS ({len(syntax_bad)}):")
for i, d in syntax_bad: print(f"  #{i}: {d}")
print(f"\nPREFIX MISMATCHES to review ({len(prefix_mismatch)}):")
for i, d, p, label, v in prefix_mismatch:
    print(f"  #{i}: {d}  (prefix {p}; venue '{v}' usually -> {label})")
