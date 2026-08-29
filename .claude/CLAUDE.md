# Website — rquinnmit.github.io

Ryan's personal site. Origin `rquinnmit/rquinnmit.github.io`, public, default
branch `main`, served by GitHub Pages on push. Two sites in one repo: the
professional site at `/` and the DJ site at `/music/`. Each links to the other.

## Stack

Hand-written HTML, CSS, and vanilla JS. **No package.json, no bundler, no build
step, no test suite.** There is nothing to run before shipping, and claiming
"tests pass" here would be meaningless — say so plainly instead.

Because every file is hand-authored, never reformat HTML or CSS wholesale. Match
the surrounding indentation and leave untouched lines untouched.

Layout: `index.html` and `styles.css` at the root with `carousel.js`;
`music/index.html` and `music/music.css` for the DJ site; assets under `images/`,
`papers/`, and `resumes/`.

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

## DJ site (`/music/`)

Ryan performs as Diffusion. Sections are `#upcoming`, `#sets`, `#photos`,
`#played`, and `#booking` — there is deliberately no About section.

`#upcoming` and `#played` share one grid, so a show moves between them by
editing its date and dropping `gig--next`. Upcoming rows are links to the ticket
page and carry a day-level date (`Aug 29`); played rows carry month and year
(`May 2026`). The row template lives in an HTML comment above the rows.

The centered title runs a noise-to-clarity diffusion animation built by clipping
noise to the letterforms and revealing three states through their own masks.
`music/music.css:748` has a `@media (prefers-reduced-motion: reduce)` block, and
that OS setting has twice been mistaken for the animation being broken. Check it
before debugging any animation here.

The entrance plays on phones too. Until 2026-08-28 the `@media (max-width: 600px)`
block at `music/music.css:716` hid it outright; it now swaps the middle layer to
`#mark-noise-mid-sm` in `music/index.html`, a twin of `#mark-noise-mid` with every
absolute length halved so the tearing stays proportionate to 50px glyphs. If the
two filters ever diverge, change both. Verified at 375px and 320px in Playwright
only, never on phone hardware. To see a phone width, use Playwright's
`browser_resize`: the Chrome MCP's `resize_window` reports success but leaves
`innerWidth` unchanged on a maximized window.

## Ignored on purpose

`docs/` and `.superpowers/` are gitignored, both currently untracked. Pages serves
whatever is in the branch, so tracking them would publish planning artifacts at
rquinnmit.github.io/docs/.
