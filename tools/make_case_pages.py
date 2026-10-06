"""Builds the RepX and translator case-study pages from the SurgeGuard page's shell.

The head, masthead and footer come from work/surgeguard/index.html, so all case
studies share one chrome. Run from the repo root: python tools/make_case_pages.py
"""
import io
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
src = io.open(os.path.join(ROOT, "work/surgeguard/index.html"), encoding="utf-8").read()
HEAD = src[: src.index('  <main id="main">')]
FOOT = src[src.index('  <footer class="footer">') :]


def page(slug, title, desc, ogdesc, main):
    h = HEAD.replace("SurgeGuard, a case study by Haven Leno J", title)
    h = h.replace(
        "SurgeGuard turns ordinary camera feeds into an explainable Crowd Stability Index. "
        "Winner, Implementation Category, Sensora 2.0 at VIT Vellore.",
        desc,
    )
    h = h.replace("A real-time crowd-safety platform. Winner, Implementation Category, Sensora 2.0.", ogdesc)
    h = h.replace("/work/surgeguard/", "/work/%s/" % slug)
    os.makedirs(os.path.join(ROOT, "work", slug), exist_ok=True)
    with io.open(os.path.join(ROOT, "work", slug, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(h + main + FOOT)


REPX = """  <main id="main">
    <section class="case-hero" aria-labelledby="title">
      <div class="wrap grid">
        <p class="crumb"><a href="/#work">All work</a></p>
        <h1 id="title">RepX</h1>
        <p class="lede">Bodyweight fitness as a competitive online sport: live 60-second battles where the camera counts only valid reps.</p>
        <dl class="facts">
          <div><dt>Year</dt><dd>2026</dd></div>
          <div><dt>Type</dt><dd>Full-stack web app, installable as a PWA</dd></div>
          <div><dt>Built with</dt><dd>React, TypeScript, NestJS, Socket.IO, Prisma, MediaPipe</dd></div>
          <div><dt>Status</dt><dd>Playable end to end; not yet deployed publicly</dd></div>
        </dl>
        <div class="links">
          <a class="btn btn--solid" href="https://github.com/HavenLeno22/RepX" rel="noopener">Code on GitHub</a>
        </div>
      </div>
    </section>

    <section class="wrap" aria-label="Screens">
      <div class="shots">
        <figure class="shot--wide">
          <img src="/assets/img/repx-onboarding.webp" width="1600" height="928" alt="RepX onboarding: Push-ups, but it counts for something. A battle card shows Rookie 14 against Opponent 11, with 60 seconds and most verified reps wins." fetchpriority="high">
          <figcaption>Onboarding explains the whole game in one screen.</figcaption>
        </figure>
        <figure class="shot--wide">
          <img src="/assets/img/repx-home.webp" width="1600" height="928" alt="The RepX home screen with a 1198 rating, Silver rank, level progress, missions and the current season." loading="lazy">
          <figcaption>Home, shown with a seeded demo account: rating, rank, progress, missions and the current season.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section" aria-labelledby="idea">
      <div class="wrap grid">
        <header class="section__head"><h2 id="idea">The idea</h2></header>
        <div class="section__body case-body">
          <p>Home workouts are easy to skip and impossible to compare, because rep counts are self-reported. RepX makes every rep count by checking it, then turns the result into a rating you can climb.</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="match">
      <div class="wrap grid">
        <header class="section__head"><h2 id="match">How a match works</h2></header>
        <div class="section__body case-body">
          <ol class="steps">
            <li>Sign in and pick one of seven exercises: push-ups, pull-ups, squats, burpees, planks, sit-ups or jumping jacks.</li>
            <li>Matchmaking pairs you with a real player near your rating.</li>
            <li>For 60 seconds, pose estimation runs in each browser and counts only reps with valid form.</li>
            <li>The player with more verified reps wins, and both ELO ratings move, just like in chess.</li>
          </ol>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="built">
      <div class="wrap grid">
        <header class="section__head"><h2 id="built">What's built</h2></header>
        <div class="section__body case-body">
          <ul>
            <li>Matchmaking, live camera matches, ELO settlement and leaderboards.</li>
            <li>Tournaments with bracket logic, direct challenges, private rooms and friends.</li>
            <li>Progression: XP, levels, missions, achievements and seasons.</li>
            <li>Anti-cheat: voided matches don't count toward wins and losses.</li>
            <li>Accounts with email verification, password reset, Google and Apple sign-in, refresh-token rotation with replay detection, and account deletion.</li>
            <li>An installable PWA with an offline banner, packaged for Android as a Trusted Web Activity.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="stack">
      <div class="wrap grid">
        <header class="section__head"><h2 id="stack">How it's built</h2></header>
        <div class="section__body case-body">
          <p>A TypeScript monorepo in three packages. The React front end is a PWA. The NestJS API handles accounts and matches, with Socket.IO for live play, and Prisma over SQLite in development and PostgreSQL in production.</p>
          <p>A shared package holds the logic both sides must agree on: the exercise engine, where each exercise is a plugin, plus progression and tournament brackets.</p>
          <div class="figures">
            <div><strong>7</strong><span>exercises, each a plugin</span></div>
            <div><strong>64</strong><span>tests on the shared logic</span></div>
            <div><strong>60s</strong><span>per battle</span></div>
          </div>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="next">
      <div class="wrap grid">
        <header class="section__head"><h2 id="next">What's next</h2></header>
        <div class="section__body case-body">
          <p>Deploy the API and the PWA publicly, then release the Android build. The deployment guide, environment checks and health probes are already in the repo.</p>
        </div>
      </div>
    </section>

    <div class="wrap">
      <a class="next" href="/work/translator/"><span>Next project</span><strong>Multi-Mode AI Translator</strong></a>
    </div>
  </main>

"""

TRANSLATOR = """  <main id="main">
    <section class="case-hero" aria-labelledby="title">
      <div class="wrap grid">
        <p class="crumb"><a href="/#work">All work</a></p>
        <h1 id="title">Multi-Mode AI Translator</h1>
        <p class="lede">One app for three kinds of translation: between languages with the Gemini API, to and from Morse code, and by voice.</p>
        <dl class="facts">
          <div><dt>Year</dt><dd>2025</dd></div>
          <div><dt>Type</dt><dd>Team project</dd></div>
          <div><dt>Built with</dt><dd>Python, Flask, Gemini API, Web Speech API, Web Audio API, Tailwind CSS</dd></div>
        </dl>
        <div class="links">
          <a class="btn btn--solid" href="https://github.com/HavenLeno22/multi-mode-ai-translator" rel="noopener">Code on GitHub</a>
        </div>
      </div>
    </section>

    <section class="wrap" aria-label="Screens">
      <div class="shots">
        <figure class="shot--wide">
          <img src="/assets/img/translator-morse.webp" width="1600" height="756" alt="The translator in English to Morse mode, converting Hello from Chennai into Morse code." fetchpriority="high">
          <figcaption>English to Morse: "Hello from Chennai", converted by the Flask backend.</figcaption>
        </figure>
      </div>
    </section>

    <section class="section" aria-labelledby="does">
      <div class="wrap grid">
        <header class="section__head"><h2 id="does">What it does</h2></header>
        <div class="section__body case-body">
          <ul>
            <li>Translates between 21 languages, including Tamil, Telugu, Hindi, Spanish and Japanese, with the Gemini API, and can detect the input language.</li>
            <li>Encodes English into Morse code and decodes Morse back, typed or tapped on a tap pad.</li>
            <li>Takes voice input through the Web Speech API, and reads results aloud.</li>
            <li>Translates whole .txt files, keeps a history of past translations, and has light and dark themes.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="built">
      <div class="wrap grid">
        <header class="section__head"><h2 id="built">How it's built</h2></header>
        <div class="section__body case-body">
          <p>A Flask backend exposes small endpoints for translation, language detection and both Morse directions. The Gemini key stays on the server in an environment file and never reaches the browser.</p>
          <p>The front end is HTML, Tailwind CSS and JavaScript. It calls the backend with fetch and uses the browser's own speech and audio APIs for voice in and out.</p>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="next">
      <div class="wrap grid">
        <header class="section__head"><h2 id="next">What I'd improve next</h2></header>
        <div class="section__body case-body">
          <ul>
            <li>Move to Google's newer google-genai SDK; the library it uses today is deprecated.</li>
            <li>Host a public demo, with rate limiting so the API key can't be abused.</li>
          </ul>
        </div>
      </div>
    </section>

    <div class="wrap">
      <a class="next" href="/work/surgeguard/"><span>Next project</span><strong>SurgeGuard</strong></a>
    </div>
  </main>

"""

page(
    "repx",
    "RepX, a case study by Haven Leno J",
    "RepX turns bodyweight fitness into a ranked online sport: live 60-second battles where pose estimation in the browser counts only valid reps.",
    "Live 60-second fitness battles where the camera counts only valid reps.",
    REPX,
)
page(
    "translator",
    "Multi-Mode AI Translator, a case study by Haven Leno J",
    "A translator for languages, Morse code and speech, built with Flask and the Gemini API.",
    "Languages, Morse code and voice in one translator, built with Flask and Gemini.",
    TRANSLATOR,
)
print("Wrote work/repx/ and work/translator/")
