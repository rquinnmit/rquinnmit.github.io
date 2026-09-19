# rquinnmit.github.io

Ryan Quinn's professional site: header, About, Experience, Projects and a
reading list. Hand-written HTML, CSS and JavaScript, no build step, served by
GitHub Pages straight from `main`.

This file explains how the pieces fit and how to make the routine edits.
`.claude/CLAUDE.md` records the design decisions and the rules behind them.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The page. Content lives here, with a template for each repeating block in an HTML comment beside it. |
| `styles.css` | The one stylesheet, in page order. Each component's phone rules sit right after its desktop rules. |
| `carousel.js` | Pages the reading list; reads how many cards make a page from the stylesheet. |
| `fonts/` | Self-hosted latin subsets of Lato 400, 700 and 900 (SIL Open Font License). |
| `images/` | Profile photo, employer logos, project thumbnails, `reading/` card images, the share card and favicon. |
| `papers/` | PDFs linked from Projects. |
| `resumes/resume.pdf` | The CV linked from the header. A copy; the source of truth is the resumes repo. See Resume below. |
| `music/index.html` | Redirect stub to diffusiondj.com that carries the show hash across. Never delete it. |
| `tools/check.py` | Checks the invariants below. Standard library only. |
| `tools/sync-resume.py` | Refreshes `resumes/resume.pdf` from the resumes repo. Standard library only. |

## Preview

```
python3 -m http.server 8000
```

## Check

```
python3 tools/check.py
```

Prints `ok`, or one line per problem with a file and line, and exits 1. The
rules it checks are listed in its docstring. Run it after any edit to
`index.html` or `styles.css`. A GitHub Action runs it on every push as well
and marks the commit, though it cannot stop Pages publishing a commit that
fails.

## Resume

The CV is authored in `~/Personal/Resumes` (github.com/rquinnmit/resumes) and
only served from here, so `resumes/resume.pdf` is a build artifact, not a
source. Refresh it and commit the result:

```
python3 tools/sync-resume.py
```

`--check` reports without copying and exits 1 when the two have drifted; run
it before publishing anything that mentions the CV. A symlink would express
this better but does not survive deployment: Pages builds from a checkout of
this repo alone, so a link pointing outside it dangles on the runner and
Jekyll skips symlinks anyway. The copy drifted a month once already.

## Routine edits

Every repeating block in `index.html` has a template in an HTML comment
directly above the real entries. Copy the template, fill it in, then run the
checker.

**Add a role.** Add an `li.exp` at the top of the Experience list with a
200x200 WebP logo in `images/`. Dates read `Mon YYYY – Mon YYYY`.

**Add a project.** Add a `pub-entry` at the top of Projects with an 800px-wide
WebP thumbnail, the PDF under `papers/`, and the date as `Month YYYY`.

**Add a reading-list entry.** The `/paper` command drafts one from a URL or
PDF in the house style. Place it by topic, not by tag, and put the image at
the exact path the card names under `images/reading/`. The checker fails on a
missing image.

Encode WebP with `cwebp -q 85 -m 6 -metadata none in.jpg -o out.webp`.

## Deploy

Push to `main`. GitHub Pages runs its Jekyll pass, which is what keeps
`.claude/` off the site, and takes about a minute. Confirm the deploy with:

```
gh api repos/rquinnmit/rquinnmit.github.io/pages/builds/latest --jq '{status,created_at,error}'
```
