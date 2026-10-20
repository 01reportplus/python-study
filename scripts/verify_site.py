"""Check generated HTML, local links and project-path deployment using stdlib."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.ids = set()
        self.links = []
        self.canonical = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonical = attrs.get("href")
        for key in ("href", "src"):
            if attrs.get(key):
                self.links.append(attrs[key])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-dir", type=Path, default=ROOT / "site")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/")
    args = parser.parse_args()
    site = args.site_dir.resolve()
    base = args.base_url.rstrip("/") + "/"
    base_parts = urlsplit(base)
    prefix = base_parts.path
    failures = []
    pages = {p: Page(p) for p in site.rglob("*.html")}
    chapters = list((site / "tutorial").glob("*/index.html"))
    expected = list((ROOT / "docs" / "tutorial").glob("[0-9][0-9]-*.md"))
    if len(chapters) != len(expected) or not chapters:
        failures.append(f"chapters: expected {len(expected)}, got {len(chapters)}")
    for required in ("index.html", "404.html", ".nojekyll", "sitemap.xml", "search/search_index.json",
                     "assets/stylesheets/extra.css", "downloads/Python完整教程.txt"):
        if not (site / required).is_file():
            failures.append(f"missing artifact: {required}")
    for directory in ("examples", "scripts"):
        for source in (ROOT / directory).glob("*.py"):
            output = site / source.relative_to(ROOT)
            if not output.is_file() or output.read_bytes() != source.read_bytes():
                failures.append(f"source download differs: {source.relative_to(ROOT)}")
    checked = 0
    for path, page in pages.items():
        relative = path.relative_to(site).as_posix()
        page_url = urljoin(base, relative.removesuffix("index.html"))
        if relative != "404.html" and unquote(page.canonical or "") != page_url:
            failures.append(f"{relative}: canonical {page.canonical!r} != {page_url!r}")
        for href in page.links:
            if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
                continue
            target = urlsplit(urljoin(page_url, href))
            if target.netloc != base_parts.netloc:
                continue
            if not target.path.startswith(prefix):
                failures.append(f"{relative}: link escapes Pages prefix: {href}")
                continue
            output = (site / unquote(target.path[len(prefix):])).resolve()
            if not output.is_relative_to(site):
                failures.append(f"{relative}: link escapes site: {href}")
                continue
            if output.is_dir():
                output /= "index.html"
            checked += 1
            if not output.is_file():
                failures.append(f"{relative}: missing target: {href}")
            elif target.fragment and output in pages:
                if unquote(target.fragment) not in pages[output].ids:
                    failures.append(f"{relative}: missing anchor: {href}")
    search_path = site / "search" / "search_index.json"
    if search_path.is_file():
        search = json.loads(search_path.read_text(encoding="utf-8"))
        if not search.get("docs"):
            failures.append("search index is empty")
        locations = {unquote(item["location"]) for item in search.get("docs", [])}
        for chapter in expected:
            if f"tutorial/{chapter.stem}/" not in locations:
                failures.append(f"chapter missing from search: {chapter.name}")
    print(f"html_pages={len(pages)} chapters={len(chapters)} local_targets={checked} failures={len(failures)}")
    for failure in failures:
        print(failure)
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
