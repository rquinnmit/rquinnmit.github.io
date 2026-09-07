# Website — rquinnmit.github.io

Ryan's professional site. Origin `rquinnmit/rquinnmit.github.io`, public, default
branch `main`, served by GitHub Pages on push. The DJ site he performs under as
Diffusion lived here at `/music/` until 2026-09-05 and now has its own repo,
`rquinnmit/diffusion` at `/Users/rquinn1/Personal/Diffusion`, served at
`https://diffusiondj.com`. All that remains of it here is `music/index.html`, a
redirect stub that forwards to the domain and carries the `#show/<slug>` hash
across so shared show links keep working. Never delete that stub. The two Music
links on the front page point straight at the domain, and the DJ site
deliberately does not link back.

`README.md` explains the layout and the routine edits. This file holds the
decisions and the rules behind them.

## Stack

Hand-written HTML, CSS, and vanilla JS. **No package.json, no bundler, no build
step, no test suite.** The one thing to run is `python3 tools/check.py`, a
standard-library script that verifies the invariants listed in its docstring.
Run it after editing `index.html` or `styles.css`, and say plainly that it is a
lint, not a test suite, when reporting. A GitHub Action runs it on every push.

Because every file is hand-authored, never reformat HTML or CSS wholesale. Match
the surrounding indentation and leave untouched lines untouched.

Layout: `index.html`, `styles.css` and `carousel.js` at the root; the redirect
stub at `music/index.html`; self-hosted Lato in `fonts/`; assets under
`images/`, `papers/`, and `resumes/`.

Never add a `.nojekyll` file here. Jekyll is what keeps dot-directories off
the site; verified 2026-09-07 that with `.nojekyll` present Pages served
`.claude/CLAUDE.md` at the site root (only `.github/` stays withheld). The
checker fails if the file appears. The build takes about a minute for the
same reason.

Fonts are self-hosted (latin subsets of Google's Lato woff2 builds, SIL Open
Font License) because a stylesheet link to fonts.googleapis.com is
render-blocking and cross-origin, and was the largest cost in front of first
paint. Do not reintroduce a googleapis or gstatic link.

To look at a page in Playwright, serve the repo over HTTP first (`python3 -m
http.server`); the Playwright MCP refuses `file:` URLs. Navigating from a URL to
the same URL plus a hash is a fragment navigation and does not reload the
document, so add a throwaway query string when a reload is the point.

## Stylesheet

The header comment of `styles.css` says how it is organised. The rules: a new
rule's phone block goes beside its component, not at the end of the file;
colour is a token from `:root`, never a new hex, and every text token passes
WCAG AA on white; no `!important`. The checker enforces the hex rule.

The reading-list breakpoints live in one place, the track's `--per-page`
custom property in `styles.css`; `carousel.js` reads it rather than carrying
its own copy.

## Experience and projects

Experience is a `<ul class="experience">` of `li.exp` rows, newest first, laid
out with grid on desktop and restacked on phones; the template comment above
the list shows the shape. Projects are `pub-entry` blocks, newest first.

## Reading list

Entries live in `index.html` as `<a class="carousel-card">` blocks.
Each holds an `<img class="carousel-img">` pointing at
`images/reading/<name>.webp`, then a `carousel-body` holding a `carousel-tag`,
an `<h3>` title, a one-sentence `<p>`, and a `carousel-meta` reading `Read
More`. Cards past the first three take `loading="lazy"`. The template comment
above the track shows the shape.

Tags in use: `Paper`, `Post`, `Release`.

Descriptions are one sentence saying what the work does and what is novel.
Present tense, no hedging, no "this paper argues", no multi-sentence summaries.
Read three existing entries and match their register before writing a new one.

Ordering is **thematic, not grouped by tag**. Ryan once asked
for robotics research first, then other research, then posts and releases, and
the list only loosely reflects that. Do not assume strict type-grouping; read the
current order and place a new entry by topic, asking him if the right slot is
ambiguous.

There is no page markup. All cards live in one `carousel-track`, and
`carousel.js` paginates client-side at 3, 2, or 1 cards per page depending on
viewport width (>900px, 601–900px, ≤600px). "Which page" is a function of window
size, not of the HTML.

Every entry needs a local `.webp` under `images/reading/`. That file cannot be
fabricated — name the exact filename the entry expects and leave the reference.
The checker fails on a missing file.

## Ignored on purpose

`docs/`, `.superpowers/`, `.playwright-mcp/`, `/CLAUDE.md` and `/AGENTS.md` are
gitignored. Pages serves whatever is in the branch, so tracking them would
publish planning artifacts and agent instructions at the site root.
