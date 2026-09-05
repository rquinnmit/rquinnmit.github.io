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

## Stack

Hand-written HTML, CSS, and vanilla JS. **No package.json, no bundler, no build
step, no test suite.** There is nothing to run before shipping, and claiming
"tests pass" here would be meaningless — say so plainly instead.

Because every file is hand-authored, never reformat HTML or CSS wholesale. Match
the surrounding indentation and leave untouched lines untouched.

Layout: `index.html` and `styles.css` at the root with `carousel.js`; the
redirect stub at `music/index.html`; assets under `images/`, `papers/`, and
`resumes/`.

To look at a page in Playwright, serve the repo over HTTP first (`python3 -m
http.server`); the Playwright MCP refuses `file:` URLs. Navigating from a URL to
the same URL plus a hash is a fragment navigation and does not reload the
document, so add a throwaway query string when a reload is the point.

## Reading list

Nine entries currently, in `index.html` as `<a class="carousel-card">` blocks. Each
wraps a `carousel-img` div whose `background-image` points at
`images/reading/<name>.webp`, then a `carousel-body` holding a `carousel-tag`, an
`<h3>` title, a one-sentence `<p>`, and a `carousel-meta` reading `Read More`.

Tags in use: `Paper` (4), `Post` (4), `Release` (1).

Descriptions are one sentence saying what the work does and what is novel.
Present tense, no hedging, no "this paper argues", no multi-sentence summaries.
Read three existing entries and match their register before writing a new one.

Ordering is **thematic, not grouped by tag** — verified 2026-08-17, the sequence
is Paper, Paper, Paper, Post, Post, Post, Paper, Post, Release. Ryan once asked
for robotics research first, then other research, then posts and releases, and
the list only loosely reflects that. Do not assume strict type-grouping; read the
current order and place a new entry by topic, asking him if the right slot is
ambiguous.

There is no page markup. All nine cards live in one `carousel-track`, and
`carousel.js` paginates client-side at 3, 2, or 1 cards per page depending on
viewport width (>900px, 601–900px, ≤600px). "Which page" is a function of window
size, not of the HTML.

Every entry needs a local `.webp` under `images/reading/`. That file cannot be
fabricated — name the exact filename the entry expects and leave the reference.

## Ignored on purpose

`docs/` and `.superpowers/` are gitignored, both currently untracked. Pages serves
whatever is in the branch, so tracking them would publish planning artifacts at
rquinnmit.github.io/docs/.
