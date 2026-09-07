#!/usr/bin/env python3
"""Check the invariants that keep rquinnmit.github.io consistent.

The site has no build and no test suite; what it has is a handful of rules
that hold the hand-written files together. This script reads index.html and
styles.css with the standard library only and reports every rule it finds
broken, with a line number where one exists. It exits 1 on any finding so a
shell can gate on it.

Run from anywhere::

    python3 tools/check.py

Rules checked
-------------
- Every id is unique.
- Every local file the page or stylesheet references exists, and every file
  under fonts/, images/, papers/ and resumes/ is referenced (no orphans).
- Every img has alt; every img outside the reading list has width and height.
- Every link that opens a new tab carries rel="noopener".
- Experience rows are dated ``Mon YYYY – Mon YYYY`` (or ``Present``) and run
  newest first; project entries are dated ``Month YYYY`` and run newest first.
- Every reading-list card has one tag (Paper, Post or Release), one title,
  one sentence and one Read More.
- The Open Graph image's declared width and height match the file.
- The stylesheet uses no hex colour outside the :root tokens and no
  !important, and defines --per-page for the carousel.
- music/index.html still redirects to diffusiondj.com; .nojekyll exists.
"""
from __future__ import annotations

import re
import struct
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://rquinnmit.github.io/"
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LONG_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
ASSET_DIRS = ("fonts", "images", "papers", "resumes")
TAGS = {"Paper", "Post", "Release"}

problems: list[str] = []


def flag(where: str, message: str) -> None:
    problems.append(f"{where}: {message}")


class Element:
    """One start tag: its name, attributes, line, and position in the tree."""

    def __init__(self, tag, attrs, line, parent):
        self.tag = tag
        self.attrs = dict(attrs)
        self.line = line
        self.parent = parent
        self.children: list[Element] = []
        self.text = ""

    def has_class(self, name):
        return name in self.attrs.get("class", "").split()

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()

    def find_all(self, tag=None, cls=None):
        for el in self.walk():
            if tag and el.tag != tag:
                continue
            if cls and not el.has_class(cls):
                continue
            yield el

    def all_text(self):
        return self.text + "".join(c.all_text() for c in self.children)


class Tree(HTMLParser):
    """Build an Element tree from the page, ignoring comments."""

    VOID = {"meta", "link", "img", "br", "hr", "input", "source"}

    def __init__(self):
        super().__init__()
        self.root = Element("#root", [], 0, None)
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        el = Element(tag, attrs, self.getpos()[0], self.stack[-1])
        self.stack[-1].children.append(el)
        if tag not in self.VOID:
            self.stack.append(el)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].text += data


def load_tree(path: Path) -> Element:
    parser = Tree()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.root


def webp_size(path: Path):
    """Return (width, height) of a WebP file, or None if it is not one."""
    data = path.read_bytes()
    if data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    kind = data[12:16]
    if kind == b"VP8 ":
        w, h = struct.unpack("<HH", data[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if kind == b"VP8L":
        bits = struct.unpack("<I", data[21:25])[0]
        return 1 + (bits & 0x3FFF), 1 + ((bits >> 14) & 0x3FFF)
    if kind == b"VP8X":
        w = int.from_bytes(data[24:27], "little") + 1
        h = int.from_bytes(data[27:30], "little") + 1
        return w, h
    return None


# ── html checks ──


def check_ids(root: Element) -> None:
    seen: dict[str, int] = {}
    for el in root.walk():
        el_id = el.attrs.get("id")
        if el_id:
            if el_id in seen:
                flag(f"index.html:{el.line}", f"duplicate id {el_id!r} (first at line {seen[el_id]})")
            seen[el_id] = el.line


def check_images(root: Element) -> None:
    for img in root.find_all("img"):
        where = f"index.html:{img.line}"
        if "alt" not in img.attrs:
            flag(where, "img without alt")
        if img.has_class("carousel-img"):
            continue
        if not ("width" in img.attrs and "height" in img.attrs):
            flag(where, "img needs width and height")


def check_links(root: Element) -> None:
    for a in root.find_all("a"):
        if a.attrs.get("target") == "_blank" and "noopener" not in a.attrs.get("rel", ""):
            flag(f"index.html:{a.line}", 'target="_blank" without rel="noopener"')


def month_index(text: str, names: list[str]):
    parts = text.strip().split()
    if len(parts) != 2 or parts[0] not in names or not parts[1].isdigit():
        return None
    return int(parts[1]) * 12 + names.index(parts[0])


def check_experience(root: Element) -> None:
    previous = None
    for row in root.find_all("li", cls="exp"):
        where = f"index.html:{row.line}"
        date = next(row.find_all(cls="exp-date"), None)
        text = date.all_text().strip() if date else ""
        halves = [h.strip() for h in text.replace("–", "-").split("-")]
        start = month_index(halves[0], MONTHS) if halves else None
        end_ok = len(halves) == 2 and (halves[1] == "Present" or month_index(halves[1], MONTHS) is not None)
        if start is None or not end_ok:
            flag(where, f"experience date {text!r} must be 'Mon YYYY – Mon YYYY' or '– Present'")
            continue
        if previous is not None and start > previous:
            flag(where, f"experience rows must run newest first; {text!r} is out of order")
        previous = start
        for cls in ("exp-logo", "exp-org", "exp-team"):
            if next(row.find_all(cls=cls), None) is None:
                flag(where, f"experience row has no .{cls}")


def check_projects(root: Element) -> None:
    previous = None
    for entry in root.find_all(cls="pub-entry"):
        where = f"index.html:{entry.line}"
        venue = next(entry.find_all(cls="pub-venue"), None)
        text = venue.all_text().strip() if venue else ""
        value = month_index(text, LONG_MONTHS)
        if value is None:
            flag(where, f"project date {text!r} must be 'Month YYYY'")
            continue
        if previous is not None and value > previous:
            flag(where, f"projects must run newest first; {text!r} is out of order")
        previous = value


def check_cards(root: Element) -> None:
    for card in root.find_all(cls="carousel-card"):
        where = f"index.html:{card.line}"
        tags = [t.all_text().strip() for t in card.find_all(cls="carousel-tag")]
        if len(tags) != 1 or tags[0] not in TAGS:
            flag(where, f"card needs one tag from {sorted(TAGS)}, has {tags}")
        for label, tag, cls in (("h3", "h3", None), ("p", "p", None), (".carousel-meta", None, "carousel-meta"), ("img.carousel-img", "img", "carousel-img")):
            found = len(list(card.find_all(tag, cls)))
            if found != 1:
                flag(where, f"card needs one {label}, has {found}")


def local_refs(root: Element, css_text: str):
    for el in root.walk():
        for attr in ("src", "href", "content"):
            value = el.attrs.get(attr)
            if not value:
                continue
            value = value.replace(SITE, "").replace("%20", " ")
            if value.startswith(ASSET_DIRS) and "://" not in value:
                yield value, f"index.html:{el.line}"
    for match in re.finditer(r"url\((?:'|\")?([^'\")]+)", css_text):
        line = css_text.count("\n", 0, match.start()) + 1
        yield match.group(1), f"styles.css:{line}"


def check_files(root: Element, css_text: str) -> None:
    referenced = set()
    for rel, where in local_refs(root, css_text):
        referenced.add(rel)
        if not (ROOT / rel).is_file():
            flag(where, f"references missing file {rel}")
    on_disk = {
        str(p.relative_to(ROOT))
        for d in ASSET_DIRS
        for p in (ROOT / d).rglob("*")
        if p.is_file() and not p.name.startswith(".")
    }
    for rel in sorted(on_disk - referenced):
        flag(rel, "not referenced from index.html or styles.css")


def check_og_image(root: Element) -> None:
    metas = {m.attrs.get("property"): m for m in root.find_all("meta") if m.attrs.get("property")}
    image = metas.get("og:image")
    if image is None:
        flag("index.html", "no og:image")
        return
    path = ROOT / image.attrs["content"].replace(SITE, "")
    size = webp_size(path) if path.is_file() else None
    if size is None:
        flag(f"index.html:{image.line}", f"og:image {path.name} is not a readable WebP")
        return
    width, height = metas.get("og:image:width"), metas.get("og:image:height")
    if width is None or height is None:
        flag(f"index.html:{image.line}", "og:image needs og:image:width and og:image:height")
        return
    got = (int(width.attrs["content"]), int(height.attrs["content"]))
    if got != size:
        flag(f"index.html:{width.line}", f"og:image is {size[0]}x{size[1]}, declared {got[0]}x{got[1]}")


# ── css and repo checks ──


def check_css(css_text: str) -> None:
    hexes = set(re.findall(r"#[0-9A-Fa-f]{3,8}\b", css_text))
    tokens = set(re.findall(r"--\w+:\s*(#[0-9A-Fa-f]{3,8})", css_text))
    for h in sorted(hexes - tokens):
        line = css_text.count("\n", 0, css_text.find(h)) + 1
        flag(f"styles.css:{line}", f"hex colour {h} is not a palette token")
    for match in re.finditer(r"!important", css_text):
        flag(f"styles.css:{css_text.count(chr(10), 0, match.start()) + 1}", "!important; fix the specificity instead")
    if "--per-page" not in css_text:
        flag("styles.css", "the carousel track must define --per-page")


def check_repo_files() -> None:
    stub = ROOT / "music" / "index.html"
    if not stub.is_file() or "https://diffusiondj.com/" not in stub.read_text():
        flag("music/index.html", "the redirect stub to diffusiondj.com must stay")
    if not (ROOT / ".nojekyll").is_file():
        flag(".nojekyll", "missing; Pages would run Jekyll over the branch")


def main() -> int:
    root = load_tree(ROOT / "index.html")
    css_text = (ROOT / "styles.css").read_text(encoding="utf-8")
    check_ids(root)
    check_images(root)
    check_links(root)
    check_experience(root)
    check_projects(root)
    check_cards(root)
    check_files(root, css_text)
    check_og_image(root)
    check_css(css_text)
    check_repo_files()
    if problems:
        print("\n".join(problems))
        print(f"{len(problems)} problem(s)")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
