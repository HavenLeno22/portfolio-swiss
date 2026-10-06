"""Prints tools/resume.html to PDF with headless Chrome.

    python tools/build_resume.py
        -> resume/Haven-Leno-J-Resume.pdf (public: no phone number)

    python tools/build_resume.py --phone "+91 ..." --out "C:/path/outside/the/repo.pdf"
        -> a private copy with the phone number, for direct applications.
           Never write the private copy inside this repo: everything here is public.
"""
import argparse
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCE = os.path.join(ROOT, "tools", "resume.html")
PUBLIC = os.path.join(ROOT, "resume", "Haven-Leno-J-Resume.pdf")
CHROMES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "google-chrome",
    "chromium",
]


def chrome():
    for c in CHROMES:
        if os.path.isabs(c) and os.path.exists(c):
            return c
        if not os.path.isabs(c) and shutil.which(c):
            return shutil.which(c)
    raise SystemExit("Chrome or Edge not found")


def render(html_path, pdf_path):
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    subprocess.run(
        [
            chrome(),
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            "--virtual-time-budget=4000",
            "--print-to-pdf=" + pdf_path,
            "file:///" + html_path.replace("\\", "/"),
        ],
        check=True,
        capture_output=True,
    )
    print("Wrote", pdf_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--phone")
    ap.add_argument("--out")
    args = ap.parse_args()

    if not args.phone:
        render(SOURCE, PUBLIC)
        return

    if not args.out:
        raise SystemExit("--out is required with --phone")
    out = os.path.abspath(args.out)
    if out.startswith(ROOT):
        raise SystemExit("Refusing to write the private resume inside the public repo")
    html = open(SOURCE, encoding="utf-8").read().replace(
        "<!--PHONE-->", " &nbsp; <strong>" + args.phone + "</strong>"
    )
    # Write next to the source so the relative font paths still resolve, then remove it.
    fd, tmp = tempfile.mkstemp(suffix=".html", dir=os.path.dirname(SOURCE))
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(html)
    try:
        render(tmp, out)
    finally:
        os.remove(tmp)


if __name__ == "__main__":
    main()
