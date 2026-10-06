/* Haven Leno J — site behaviour: theme, 30-second view, command palette,
   Chennai clock and copy-email. No dependencies. */
(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var EMAIL = "havenleno2006@gmail.com";
  var RESUME = "/portfolio-swiss/resume/Haven-Leno-J-Resume.pdf";
  var onHome = location.pathname === "/portfolio-swiss/" || location.pathname === "/portfolio-swiss/index.html";

  /* ---------- storage that never throws ---------- */
  function load(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function save(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* private mode */ }
  }

  /* ---------- toast ---------- */
  var toast = document.createElement("div");
  toast.className = "toast";
  toast.setAttribute("role", "status");
  document.body.appendChild(toast);
  var toastTimer;
  function say(text) {
    toast.textContent = text;
    toast.classList.add("is-on");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove("is-on"); }, 2200);
  }

  /* ---------- theme (light first) ---------- */
  function setTheme(theme, announce) {
    root.dataset.theme = theme;
    save("theme", theme);
    var bar = document.querySelector('meta[name="theme-color"]');
    if (bar) bar.setAttribute("content", theme === "dark" ? "#0a0f1e" : "#fcfcfb");
    document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
      b.setAttribute("aria-label", theme === "dark" ? "Switch to light theme" : "Switch to dark theme");
    });
    if (announce) say(theme === "dark" ? "Dark theme on" : "Light theme on");
  }
  function toggleTheme() { setTheme(root.dataset.theme === "dark" ? "light" : "dark", true); }
  setTheme(root.dataset.theme === "dark" ? "dark" : "light", false);
  document.querySelectorAll("[data-theme-toggle]").forEach(function (b) {
    b.addEventListener("click", toggleTheme);
  });

  /* ---------- copy email ---------- */
  function copyEmail() {
    var done = function () { say("Email copied: " + EMAIL); };
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(EMAIL).then(done, function () { location.href = "mailto:" + EMAIL; });
    } else {
      location.href = "mailto:" + EMAIL;
    }
  }
  document.querySelectorAll("[data-copy-email]").forEach(function (b) {
    b.addEventListener("click", copyEmail);
  });

  /* ---------- masthead border and current section ---------- */
  var masthead = document.querySelector(".masthead");
  function onScroll() {
    if (masthead) masthead.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var navLinks = document.querySelectorAll(".nav a[href^='#']");
  if (navLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    navLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        navLinks.forEach(function (a) { a.removeAttribute("aria-current"); });
        var link = byId[entry.target.id];
        if (link) link.setAttribute("aria-current", "true");
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(byId).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) io.observe(el);
    });
  }

  /* ---------- Chennai clock ---------- */
  var clocks = document.querySelectorAll("[data-clock]");
  if (clocks.length) {
    var fmt;
    try {
      fmt = new Intl.DateTimeFormat("en-IN", { timeZone: "Asia/Kolkata", hour: "numeric", minute: "2-digit", hour12: true });
    } catch (e) { fmt = null; }
    var tick = function () {
      if (!fmt) return;
      var t = fmt.format(new Date()).replace(/\s?(am|pm)$/i, function (m) { return " " + m.trim().toLowerCase(); });
      clocks.forEach(function (c) { c.textContent = t; });
    };
    tick();
    setInterval(tick, 20000);
  }

  /* ---------- dialogs ---------- */
  var lastFocus = null;
  function openDialog(d) {
    lastFocus = document.activeElement;
    if (typeof d.showModal === "function") d.showModal(); else d.setAttribute("open", "");
  }
  function closeDialog(d) {
    if (typeof d.close === "function") d.close(); else d.removeAttribute("open");
  }
  function wireDialog(d) {
    d.addEventListener("close", function () {
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    });
    d.addEventListener("click", function (e) {
      if (e.target === d) closeDialog(d); // backdrop click
    });
  }

  /* ---------- 30-second view ---------- */
  var brief = document.createElement("dialog");
  brief.className = "brief";
  brief.setAttribute("aria-labelledby", "brief-title");
  brief.innerHTML =
    '<div class="brief__inner">' +
      '<div class="brief__top">' +
        '<div><h2 id="brief-title">Haven Leno J</h2>' +
        '<p class="brief__role">Full-stack developer, looking for a software engineering internship</p></div>' +
        '<button class="btn btn--icon" type="button" data-close aria-label="Close the 30-second view">' +
          '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.6" fill="none"/></svg>' +
        '</button>' +
      '</div>' +
      '<dl class="brief__grid">' +
        '<div><dt>Internship</dt><dd>MERN Stack Developer Intern, GenLab, Jun to Aug 2026<span class="small">Certificate GL/INT/26/183</span></dd></div>' +
        '<div><dt>Education</dt><dd>B.Tech Computer Science and Engineering, SRM IST Ramapuram, 2024 to 2028<span class="small">CGPA 7.78</span></dd></div>' +
        '<div><dt>Award</dt><dd>Winner, Implementation Category, Sensora 2.0 at VIT Vellore, 2026</dd></div>' +
        '<div class="brief__work"><dt>Best work</dt><dd><ul>' +
          '<li><a href="/portfolio-swiss/work/surgeguard/">SurgeGuard</a><span>Real-time crowd-safety platform: computer vision, FastAPI, React, Arduino</span></li>' +
          '<li><a href="/portfolio-swiss/work/repx/">RepX</a><span>Live 1v1 fitness battles with in-browser rep counting and ELO ratings</span></li>' +
          '<li><a href="/portfolio-swiss/work/translator/">Translator</a><span>Gemini translation, Morse code and voice input in one app</span></li>' +
        '</ul></dd></div>' +
        '<div><dt>Stack</dt><dd>React, Node.js, Express, Java, Spring Boot, Python, FastAPI, MongoDB</dd></div>' +
        '<div><dt>Based in</dt><dd>Chennai, India<span class="small">IST, UTC+5:30</span></dd></div>' +
        '<div><dt>Contact</dt><dd><a href="mailto:' + EMAIL + '">' + EMAIL + '</a></dd></div>' +
      '</dl>' +
      '<div class="brief__actions">' +
        '<a class="btn btn--solid" href="' + RESUME + '" download>Download resume (PDF)</a>' +
        '<button class="btn" type="button" data-brief-copy>Copy email</button>' +
        '<a class="btn" href="https://www.linkedin.com/in/havenleno" rel="noopener">LinkedIn</a>' +
        '<a class="btn" href="https://github.com/HavenLeno22" rel="noopener">GitHub</a>' +
      '</div>' +
    '</div>';
  document.body.appendChild(brief);
  wireDialog(brief);
  brief.querySelector("[data-close]").addEventListener("click", function () { closeDialog(brief); });
  brief.querySelector("[data-brief-copy]").addEventListener("click", copyEmail);
  brief.addEventListener("close", function () {
    if (location.hash === "#30-seconds") history.replaceState(null, "", location.pathname);
  });
  function openBrief() { openDialog(brief); }
  document.querySelectorAll("[data-open-brief]").forEach(function (b) {
    b.addEventListener("click", openBrief);
  });
  if (location.hash === "#30-seconds") openBrief();

  /* ---------- command palette ---------- */
  function go(url) { return function () { location.href = url; }; }
  function section(id) { return onHome ? go("#" + id) : go("/portfolio-swiss/#" + id); }
  var commands = [
    { group: "Go to", label: "Experience", hint: "MERN internship at GenLab", run: section("experience") },
    { group: "Go to", label: "Selected work", run: section("work") },
    { group: "Go to", label: "Hackathons and awards", run: section("recognition") },
    { group: "Go to", label: "Skills", run: section("skills") },
    { group: "Go to", label: "Education", run: section("education") },
    { group: "Go to", label: "About", run: section("about") },
    { group: "Go to", label: "Contact", run: section("contact") },
    { group: "Projects", label: "SurgeGuard", hint: "Case study", run: go("/portfolio-swiss/work/surgeguard/") },
    { group: "Projects", label: "RepX", hint: "Case study", run: go("/portfolio-swiss/work/repx/") },
    { group: "Projects", label: "Multi-Mode AI Translator", hint: "Case study", run: go("/portfolio-swiss/work/translator/") },
    { group: "Projects", label: "Anatomix AI", hint: "Live demo", run: go("https://havenleno22.github.io/anatomix-ai/") },
    { group: "Projects", label: "HealthSys EMR", hint: "Live demo", run: go("https://havenleno22.github.io/healthsys-emr/") },
    { group: "Projects", label: "StaffSync", hint: "GitHub", run: go("https://github.com/HavenLeno22/staff-sync") },
    { group: "Projects", label: "AgriTrace", hint: "GitHub", run: go("https://github.com/HavenLeno22/agritrace") },
    { group: "Projects", label: "Student Expense Tracker", hint: "GitHub", run: go("https://github.com/HavenLeno22/student-expense-tracker") },
    { group: "Actions", label: "Open the 30-second view", run: openBrief },
    { group: "Actions", label: "Download resume (PDF)", run: go(RESUME) },
    { group: "Actions", label: "View internship certificate", hint: "GenLab", run: go("/portfolio-swiss/certificates/genlab-internship/") },
    { group: "Actions", label: "View Sensora 2.0 certificate", hint: "Winner", run: go("/portfolio-swiss/certificates/sensora-2/") },
    { group: "Actions", label: "Copy email address", hint: EMAIL, run: copyEmail },
    { group: "Actions", label: "Switch theme", hint: "Light or dark", run: toggleTheme },
    { group: "Elsewhere", label: "GitHub", hint: "HavenLeno22", run: go("https://github.com/HavenLeno22") },
    { group: "Elsewhere", label: "LinkedIn", hint: "havenleno", run: go("https://www.linkedin.com/in/havenleno") }
  ];

  var palette = document.createElement("dialog");
  palette.className = "palette";
  palette.setAttribute("aria-label", "Quick jump");
  palette.innerHTML =
    '<input class="palette__input" type="text" role="combobox" aria-expanded="true" aria-controls="palette-list" ' +
      'aria-autocomplete="list" autocomplete="off" spellcheck="false" placeholder="Jump to a section, project or action" aria-label="Search">' +
    '<div class="palette__list" id="palette-list" role="listbox" aria-label="Results"></div>' +
    '<div class="palette__foot"><span>Up and down to move</span><span>Enter to open</span><span>Esc to close</span></div>';
  document.body.appendChild(palette);
  wireDialog(palette);

  var input = palette.querySelector("input");
  var list = palette.querySelector(".palette__list");
  var shown = [];
  var active = 0;

  function matches(cmd, q) {
    if (!q) return true;
    var hay = (cmd.label + " " + (cmd.hint || "") + " " + cmd.group).toLowerCase();
    return q.toLowerCase().split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
  }
  function render() {
    var q = input.value.trim();
    shown = commands.filter(function (c) { return matches(c, q); });
    if (active >= shown.length) active = 0;
    list.innerHTML = "";
    if (!shown.length) {
      var empty = document.createElement("p");
      empty.className = "palette__empty";
      empty.textContent = 'Nothing matches "' + q + '". Try "resume", "projects" or "email".';
      list.appendChild(empty);
      input.removeAttribute("aria-activedescendant");
      return;
    }
    var group = null;
    shown.forEach(function (c, i) {
      if (c.group !== group) {
        group = c.group;
        var g = document.createElement("div");
        g.className = "palette__group";
        g.setAttribute("role", "presentation");
        g.textContent = group;
        list.appendChild(g);
      }
      var item = document.createElement("div");
      item.className = "palette__item";
      item.id = "palette-item-" + i;
      item.setAttribute("role", "option");
      item.setAttribute("aria-selected", i === active ? "true" : "false");
      item.innerHTML = "<span></span>" + (c.hint ? "<small></small>" : "");
      item.firstChild.textContent = c.label;
      if (c.hint) item.lastChild.textContent = c.hint;
      item.addEventListener("mousemove", function () { if (active !== i) { active = i; mark(); } });
      item.addEventListener("click", function () { choose(i); });
      list.appendChild(item);
    });
    mark();
  }
  function mark() {
    list.querySelectorAll(".palette__item").forEach(function (el, i) {
      el.setAttribute("aria-selected", i === active ? "true" : "false");
    });
    var cur = document.getElementById("palette-item-" + active);
    if (cur) {
      input.setAttribute("aria-activedescendant", cur.id);
      cur.scrollIntoView({ block: "nearest" });
    }
  }
  function choose(i) {
    var cmd = shown[i];
    if (!cmd) return;
    closeDialog(palette);
    cmd.run();
  }
  function openPalette() {
    if (palette.open) return;
    input.value = "";
    active = 0;
    render();
    openDialog(palette);
    input.focus();
  }
  input.addEventListener("input", function () { active = 0; render(); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); if (shown.length) { active = (active + 1) % shown.length; mark(); } }
    else if (e.key === "ArrowUp") { e.preventDefault(); if (shown.length) { active = (active - 1 + shown.length) % shown.length; mark(); } }
    else if (e.key === "Enter") { e.preventDefault(); choose(active); }
  });
  document.querySelectorAll("[data-open-palette]").forEach(function (b) {
    b.addEventListener("click", openPalette);
  });
  document.addEventListener("keydown", function (e) {
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((e.target && e.target.tagName) || "") || (e.target && e.target.isContentEditable);
    if ((e.key === "k" || e.key === "K") && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (palette.open) closeDialog(palette); else openPalette();
    } else if (e.key === "/" && !typing && !palette.open && !brief.open) {
      e.preventDefault();
      openPalette();
    }
  });

  /* Show the right shortcut label on Macs. */
  if (/Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent)) {
    document.querySelectorAll(".kbd-hint").forEach(function (k) { k.textContent = "⌘K"; });
  }
})();
