"""Builds the certificate pages under certificates/ from the case-study page shell.

Each page shows the certificate, its details and a PDF download, so a recruiter can
check it. Run from the repo root: python tools/make_certificate_pages.py
"""
import io
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
src = io.open(os.path.join(ROOT, "work/surgeguard/index.html"), encoding="utf-8").read()
HEAD = src[: src.index('  <main id="main">')]
FOOT = src[src.index('  <footer class="footer">') :]

CERTS = [
    {
        "slug": "genlab-internship",
        "title": "Internship completion: MERN Stack Development",
        "short": "GenLab internship certificate",
        "issuer": "GenLab Pvt. Ltd., Nagercoil",
        "logo": "/assets/logos/genlab.svg",
        "rows": [
            ("Awarded to", "Haven Leno J"),
            ("Internship", "MERN Stack Development, on-site"),
            ("Dates", "15 June to 14 August 2026"),
            ("Certificate", "GL/INT/26/183"),
            ("Signed by", "Henrich P, CEO, GenLab Pvt. Ltd."),
        ],
        "note": 'To confirm it, contact GenLab through <a href="https://www.genlab.cc" rel="noopener">genlab.cc</a> and quote certificate GL/INT/26/183.',
        "pdf": "Haven-Leno-J-GenLab-Internship-Certificate.pdf",
        "verify": None,
        "alt": "Certificate of completion from GenLab presented to Haven Leno J for a MERN Stack Development internship, June 15 to August 14, 2026, ID GL/INT/26/183, signed by Henrich P, CEO.",
    },
    {
        "slug": "sensora-2",
        "title": "Winner, Implementation Category, Sensora 2.0",
        "short": "Sensora 2.0 certificate of achievement",
        "issuer": "graVITas '26, VIT Vellore",
        "logo": "/assets/logos/gravitas.webp",
        "rows": [
            ("Awarded to", "Haven Leno J"),
            ("Result", "Winner, Implementation Category"),
            ("Event", "Sensora 2.0 at graVITas '26, the annual techno-management fest of VIT Vellore"),
            ("Date", "September 2026"),
            ("Certificate", "GR2026003761"),
            ("Project", '<a href="/work/surgeguard/">SurgeGuard</a>'),
        ],
        "note": "Signed by Dr. Sudhakar N, Convenor, graVITas '26, and Dr. Partha Sharathi Mallick, Pro-Vice Chancellor, VIT.",
        "pdf": "Haven-Leno-J-Sensora-2.0-Certificate.pdf",
        "verify": None,
        "alt": "Certificate of achievement from graVITas '26 at VIT Vellore presented to Haven Leno J, GR2026003761, for securing the winner position in the Implementation Category at Sensora 2.0, September 2026.",
    },
    {
        "slug": "scholarhat-cpp",
        "title": "C++ Programming Course for Beginners",
        "short": "ScholarHat C++ certificate",
        "issuer": "ScholarHat",
        "logo": "/assets/logos/scholarhat.webp",
        "rows": [
            ("Awarded to", "Haven Leno"),
            ("Course", "C++ Programming Course for Beginners"),
            ("Date", "24 April 2025"),
            ("Certificate", "WD1C240425"),
        ],
        "note": "ScholarHat checks certificates by ID: enter WD1C240425 on its verification page.",
        "pdf": "Haven-Leno-J-ScholarHat-Cpp-Certificate.pdf",
        "verify": ("Verify on ScholarHat", "https://www.scholarhat.com/certificate/verify"),
        "alt": "Certificate of completion from ScholarHat awarded to Haven Leno for the C++ Programming Course for Beginners, 24 April 2025, certificate ID WD1C240425.",
    },
]


def page(c):
    url = "/certificates/%s/" % c["slug"]
    h = HEAD.replace("SurgeGuard, a case study by Haven Leno J", "%s, Haven Leno J" % c["short"])
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="%s, awarded to Haven Leno J by %s.">' % (c["title"], c["issuer"]), h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">',
               '<meta property="og:title" content="%s, Haven Leno J">' % c["short"], h)
    h = re.sub(r'<meta property="og:description" content="[^"]*">',
               '<meta property="og:description" content="%s, %s.">' % (c["title"], c["issuer"]), h)
    h = h.replace("/work/surgeguard/", url).replace('content="article"', 'content="website"')

    rows = "\n".join(
        '          <div><dt>%s</dt><dd>%s</dd></div>' % (k, v) for k, v in c["rows"]
    )
    actions = '          <a class="btn btn--solid" href="%s%s" download>Download the PDF</a>' % (url, c["pdf"])
    if c["verify"]:
        actions += '\n          <a class="btn" href="%s" rel="noopener">%s</a>' % (c["verify"][1], c["verify"][0])

    main = '''  <main id="main">
    <section class="case-hero cert-hero" aria-labelledby="title">
      <div class="wrap grid">
        <p class="crumb"><a href="/#recognition">All certificates and awards</a></p>
        <div class="cert-hero__id">
          <span class="logo"><img src="%(logo)s" width="48" height="48" alt=""></span>
          <p class="cert-hero__issuer">%(issuer)s</p>
        </div>
        <h1 id="title" class="cert-hero__title">%(title)s</h1>
        <dl class="facts">
%(rows)s
        </dl>
        <div class="links">
%(actions)s
        </div>
      </div>
    </section>

    <section class="wrap cert-view" aria-label="Certificate">
      <figure>
        <img src="%(url)scertificate.webp" width="1800" height="1272" alt="%(alt)s" fetchpriority="high">
        <figcaption>%(note)s</figcaption>
      </figure>
    </section>
  </main>

''' % {**c, "rows": rows, "actions": actions, "url": url}
    out = os.path.join(ROOT, "certificates", c["slug"], "index.html")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(h + main + FOOT)
    print("Wrote", os.path.relpath(out, ROOT))


for c in CERTS:
    page(c)
