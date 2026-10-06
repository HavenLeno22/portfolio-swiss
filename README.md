# Portfolio, Swiss edition

The portfolio of Haven Leno J, a full-stack developer in Chennai. Live at
**https://havenleno22.github.io/portfolio-swiss/**

It's a static site: plain HTML, one stylesheet and one small script, with no build step and no
framework. GitHub Pages serves this repository as it is.

## What's in it

- **Home page:** selected work, experience, hackathons and awards, skills, education, about and
  contact.
- **Case studies:** `work/surgeguard/`, `work/repx/` and `work/translator/`.
- **30-second view:** a one-screen summary for recruiters. Open it from the header, or link
  straight to it with `/#30-seconds`.
- **Quick jump:** press `Ctrl K` (or `Cmd K`, or `/`) to jump to any section, project or action.
- **Light and dark themes,** remembered per browser.
- **Certificates:** `certificates/` has a page for each certificate, with the image, its details
  and a PDF, so anyone can check it. Rebuild them with `python tools/make_certificate_pages.py`.
- **Resume:** `resume/Haven-Leno-J-Resume.pdf`, printed from `tools/resume.html`.

## Run it locally

```bash
python tools/serve.py
```

Then open http://127.0.0.1:5600. The server turns caching off and serves `404.html` for unknown
paths, like GitHub Pages does.

## Add the portrait

Save a square photo (at least 800 x 800) as `assets/img/haven.webp`, then in `index.html`
remove the comment markers around the `hero__photo` figure. It appears at the top of the blue
panel in the hero.

## Update the resume

Edit `tools/resume.html`, then:

```bash
python tools/build_resume.py
```

This needs Chrome or Edge installed. The public PDF has no phone number. For a private copy with
one, pass `--phone` and an `--out` path outside this repository; the script refuses to write it
inside the repo.

## Design

One typeface (Schibsted Grotesk, self-hosted), one accent colour (cobalt `#1238d6`) and a
12-column grid. The name is set to fill the width of the page; the cobalt field holds the call to
action.

## Licence

The code is MIT licensed (see `LICENSE`). The writing, resume and images are © Haven Leno J.
