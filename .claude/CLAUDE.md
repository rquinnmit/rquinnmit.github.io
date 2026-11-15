# Website — rquinnmit.github.io

Ryan's professional site. Origin `rquinnmit/rquinnmit.github.io`, public, default
branch `main`, served by GitHub Pages on push. The DJ site he performs under as
Diffusion has its own repo, `rquinnmit/diffusion` at
`/Users/rquinn1/Personal/Diffusion`, served at `https://diffusiondj.com`. All
that remains of it here is `music/index.html`, a redirect stub that forwards to
the domain and carries the `#show/<slug>` hash across. Keep that stub in place;
never delete it, because shared show links resolve through it. The two Music
links on the front page point straight at the domain, and the DJ site
deliberately does not link back.

`README.md` explains the layout and the routine edits. This file holds the
decisions and the rules behind them.

## Stack

Hand-written HTML, CSS, and vanilla JS. There is no package.json, no bundler,
no build step, and no test suite. The one thing to run is
`python3 tools/check.py`, a standard-library script that verifies the
invariants listed in its docstring. Run it after editing `index.html` or
`styles.css`, and say plainly that it is a lint, not a test suite, when
reporting.

Because every file is hand-authored, match the surrounding indentation and
leave untouched lines untouched; never reformat HTML or CSS wholesale.

Fonts are self-hosted because a stylesheet link to fonts.googleapis.com is
render-blocking and cross-origin, and was the largest cost in front of first
paint. Keep the fonts loading from `fonts/`; never reintroduce a googleapis or
gstatic link.

To look at a page in Playwright, serve the repo over HTTP first (`python3 -m
http.server`); the Playwright MCP refuses `file:` URLs. Navigating from a URL to
the same URL plus a hash is a fragment navigation and does not reload the
document, so add a throwaway query string when a reload is the point.

## Stylesheet

The header comment of `styles.css` says how it is organised. The rules: a new
rule's phone block goes beside its component, not at the end of the file;
colour is a token from `:root`, never a new hex, and every text token passes
WCAG AA on white; a rule wins through its selector or its position in the
file, never through `!important`. The checker enforces the hex rule and the
`!important` rule.

The reading-list breakpoints live in one place, the track's `--per-page`
custom property in `styles.css`; `carousel.js` reads it rather than carrying
its own copy.

## Reading list

Entries live in `index.html` as `<a class="carousel-card">` blocks. The
template comment above the track shows the shape.

Descriptions are one sentence saying what the work does and what is novel.
Present tense, no hedging, no "this paper argues", no multi-sentence summaries.
Read three existing entries and match their register before writing a new one.

Ordering is by release date, newest first, regardless of tag or topic (Ryan's
decision, replacing an earlier thematic order). The date is
that of the page the card links to: a lab's blog post counts from its own
date, even when an arXiv preprint came out earlier. After moving cards, keep the first
three without `loading="lazy"` and the rest with it.

There is no page markup. All cards live in one `carousel-track`, and
`carousel.js` paginates client-side at 3, 2, or 1 cards per page depending on
viewport width. "Which page" is a function of window size, not of the HTML.

Every entry needs a local `.webp` under `images/reading/`. When that file is
not on disk, name the exact filename the entry expects and leave the reference
in place; never fabricate the image. The checker fails on a missing file.

## Ignored on purpose

`docs/`, `.playwright-mcp/`, `/CLAUDE.md` and `/AGENTS.md` are
gitignored. Pages serves whatever is in the branch, so tracking them would
publish planning artifacts and agent instructions at the site root.

Keep the repository without a `.nojekyll` file; never add one. Jekyll is what
keeps dot-directories off the site; verified 2026-09-07 that with `.nojekyll`
present Pages served `.claude/CLAUDE.md` at the site root (only `.github/`
stays withheld). The checker fails if the file appears.
