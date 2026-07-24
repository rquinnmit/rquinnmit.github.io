# Diffusion — DJ page design

**Date:** 2026-07-24
**Status:** Approved design, ready for implementation plan

## Purpose

A second page on the personal website dedicated to Ryan Quinn's DJ work under the name
**Diffusion**. Two jobs, in order:

1. Let promoters and venues hear a set and get in touch.
2. Showcase recorded mixes and performance photography.

The page carries no research, academic, or technical content. The two audiences are
separate and neither has to see the other's page.

## Visual direction

Dark, restrained, warehouse-leaning. Structurally it borrows the console logic of
moskomusic.com — monospace utility labels, indexed rows, an artwork grid — but keeps it
as an organizing principle rather than a hardware skeuomorph. The name is treated as a
name only. No conceptual framing around diffusion as a process; nothing on the page
alludes to machine learning, physics, or mathematics.

Text is kept to a minimum throughout so the imagery carries the page.

### Tokens

| Role | Value |
|---|---|
| Background | `#08070C` |
| Panel | `#12111A` |
| Hairline | `#1D1B26` |
| Text | `#E8E4DC` |
| Secondary text | `#7E7A88` |
| Accent | `#6E64FF` |

**Contrast:** text `16:1`, secondary text `4.79:1`, accent `4.68:1` — all pass WCAG AA.
`#4A4757` appeared in early mockups at `2.2:1` and is **banned as a text color**; it may
be used only for borders. The accent is not used for small body text.

**Type:** Archivo variable (wordmark at `font-stretch: 110%`, weight 800) and JetBrains
Mono (all labels, dates, durations, metadata). Two families, no third.

The accent appears at most twice per viewport — a faint radial behind the wordmark and
hover states. On a page this quiet it becomes the subject if used more.

## Page structure

Header nav order matches document order exactly, top to bottom:

```
Hero → Sets → Photos → Played → Booking → Footer
```

The page carries no prose. There is no About section and no body copy anywhere — the
only words are the wordmark, section labels, set titles, dates, venues, and the booking
address. `MIT | Boston, MA` in the hero is the entire self-description.

### Hero

Centered and nearly empty. Wordmark `DIFFUSION` at 92px on desktop, scaling fluidly
down to roughly 40px at 375px via `clamp()`. One monospace line reading
`MIT | Boston, MA`, and three social icons (SoundCloud, Instagram, email). No photo,
no button, no scroll cue.

### Sets

Three-column grid of square tiles. Each tile is the set's SoundCloud artwork; the whole
tile links to that set on SoundCloud. Caption below each tile: title on one line,
`MMM YYYY · MM:SS` in monospace beneath.

Six sets ship, newest first:

| Title (display) | SoundCloud path | Date | Duration |
|---|---|---|---|
| Minimal House & Indie Dance — B2B Rinzler | `/rquinn1/diffusion-rinzler-minimal` | Jul 2026 | 51:29 |
| Late Night Mix — Hip Hop, R&B, Pop | `/rquinn1/rq-late-night-mix-hip-hip-r-b` | Apr 2026 | 40:35 |
| Tech House Mix | `/rquinn1/rq-house-mix` | Feb 2026 | 46:58 |
| R&B Mix | `/rquinn1/rq-rb-mix` | Jan 2026 | 39:48 |
| Trap Mix | `/rquinn1/rq-trap-mix` | Jun 2025 | 55:11 |
| Party Set | `/rquinn1/dj-party-set` | May 2025 | 53:11 |

Editorial decisions on titles:

- The `RQ - ` prefix is stripped from display captions. The page is already entirely his.
- `Hip Hip` is a typo in the SoundCloud title; the page reads `Hip Hop`.
- **MIT Lax 2026 Pregame Mix is excluded.** Its artwork is a daylight sports photo that
  does not fit the page. The set stays on SoundCloud, it just is not surfaced here.

Six sets fill the three-column grid exactly, with no orphan row.

Artwork is **downloaded once and committed** to `images/music/sets/` rather than
hotlinked from `i1.sndcdn.com`, because hotlinks break silently when a set is
re-uploaded, and the existing site already commits its images. Cost: one manual step
when a new mix is posted.

### Photos

Full-bleed horizontal rail, native scroll with proximity snap. Shots are a fixed 330px
tall at mixed widths. Deliberately a different shape from the square set grid so the two
sections do not visually rhyme. Small monospace index in the corner of each shot.

No lightbox. Clicking a photo does nothing — this was accepted in exchange for the page
shipping with zero JavaScript.

### Played

Date / venue / city rows on hairline dividers. Sits immediately above Booking on
purpose: evidence directly before the ask.

**Content pending — the real gig list has not been supplied.** Ships with placeholder
rows that must be replaced before the page goes live.

### Booking

Centered, one monospace label and the address `djdiffusionmusic@gmail.com` at 30px as a
`mailto:` link. Nothing else.

### Footer

Copyright, location, and a subtle link back to the research site.

## Positioning note

The actual catalog is **open format**, not house/tech house: of the seven sets on
SoundCloud, two are house or tech house and the rest are hip hop, R&B, trap, and party
sets. An earlier draft carried a `House & Tech House` tagline that the grid beneath it
would have contradicted.

Resolved by removing every genre claim from the page. The hero reads `MIT | Boston, MA`
and nothing anywhere states a genre — individual set titles name their own. This matches
the SoundCloud bio, which reads only "MIT DJ."

## Cross-linking

Bidirectional and subtle.

- **Research → DJ:** one item appended to the links row in `index.html`, reading `Music`.
- **DJ → research:** a small `Ryan Quinn ↗` link in the DJ page footer.

## Architecture

No build step, no framework, no dependencies — matching the existing repository.

```
music/index.html          the page; clean URL at /music/
music/music.css           its own stylesheet; shares nothing with styles.css
images/music/sets/        SoundCloud artwork, committed
images/music/photos/      gallery photography
```

`music.css` is deliberately separate from `styles.css`. The two pages are different
design systems and sharing a stylesheet would force one to compromise. The DJ page
loads its own fonts (Archivo, JetBrains Mono); the research page keeps Lato.

Sets, gigs, and photos are hand-authored HTML, the same pattern as the existing reading
list carousel. No JSON, no templating. Adding a set means copying five lines.

**The page ships with no JavaScript.** The nav uses anchor links, the rail uses native
overflow scroll, and there is no lightbox.

### Metadata

Own `<title>`, description, canonical, and Open Graph tags pointing at a set artwork
image. The DJ page must not inherit the research page's social preview.

## Quality floor

- Responsive to 375px: set grid 3 → 2 → 1, rail scrolls at all widths, hero wordmark
  scales down with `clamp()`.
- Visible keyboard focus rings on every interactive element.
- Alt text on every image.
- `loading="lazy"` on everything below the fold.
- `prefers-reduced-motion` respected — hover transforms and transitions disabled.

## Verification

This repository has no test framework, and none is being added for a static page.
Verification is manual and must actually be performed:

1. Render at 375px, 768px, and 1440px.
2. Tab through the entire page; confirm focus is always visible and ordered correctly.
3. Confirm every outbound link resolves — six SoundCloud sets, Instagram, mailto,
   research site.
4. Confirm all six artwork images load from the local path, not SoundCloud.
5. Run the palette through a contrast checker; confirm no text sits on `#4A4757`.
6. Toggle `prefers-reduced-motion` and confirm transitions stop.

## Content still outstanding

These block go-live but not implementation. The page is built with clearly marked
placeholders:

1. Gallery photographs for the rail.
2. The real gig list for Played.

## Out of scope

- Releases or original productions — none exist yet.
- Demo submissions, EPK, merchandise, mailing list.
- A CMS, build step, or any content pipeline.
- Embedded audio playback. Sets link out to SoundCloud; no player is embedded, so no
  waveform is ever fabricated.
