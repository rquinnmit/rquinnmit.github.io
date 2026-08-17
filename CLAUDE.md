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

Ordering is robotics research papers first, then other research papers, then
posts and releases. The carousel splits across pages, so say which page a new
entry lands on and what it displaces.

Every entry needs a local `.webp` under `images/reading/`. That file cannot be
fabricated — name the exact filename the entry expects and leave the reference.

## DJ site (`/music/`)

Ryan performs as Diffusion. Sections are `#sets`, `#photos`, `#played`, and
`#booking` — there is deliberately no About section.

The centered title runs a noise-to-clarity diffusion animation built by clipping
noise to the letterforms and revealing three states through their own masks.
`music/music.css:724` has a `@media (prefers-reduced-motion: reduce)` block, and
that OS setting has twice been mistaken for the animation being broken. Check it
before debugging any animation here.

## Ignored on purpose

`docs/` and `.superpowers/` are gitignored, both currently untracked. Pages serves
whatever is in the branch, so tracking them would publish planning artifacts at
rquinnmit.github.io/docs/.
