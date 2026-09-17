#!/usr/bin/env python3
"""Validate a production Hugo output directory without network access."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


DEFAULT_BASE_URL = "https://padonma.net/"
URL_ATTRIBUTES = {"a": "href", "img": "src", "link": "href", "script": "src", "source": "srcset"}


class References(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[tuple[str, str]] = []
        self.canonicals: list[str] = []
        self.is_redirect = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        attribute = URL_ATTRIBUTES.get(tag)
        if attribute and values.get(attribute):
            value = values[attribute] or ""
            if attribute == "srcset":
                for candidate in value.split(","):
                    self.urls.append((tag, candidate.strip().split()[0]))
            else:
                self.urls.append((tag, value))
        if tag == "link" and values.get("rel") == "canonical" and values.get("href"):
            self.canonicals.append(values["href"] or "")
        if tag == "meta" and (values.get("http-equiv") or "").lower() == "refresh":
            self.is_redirect = True


def output_path(build_dir: Path, url_path: str) -> Path:
    path = unquote(url_path).lstrip("/")
    candidate = build_dir / path
    if not path or url_path.endswith("/"):
        return candidate / "index.html"
    return candidate


def validate(build_dir: Path, base_url: str) -> list[str]:
    errors: list[str] = []
    base = urlsplit(base_url)
    html_files = sorted(build_dir.rglob("*.html"))
    if not html_files:
        return [f"no HTML files found under {build_dir}"]

    unwanted = [p for p in build_dir.rglob("*") if p.name in {".DS_Store", "Thumbs.db"}]
    errors.extend(f"unwanted generated file: {p.relative_to(build_dir)}" for p in unwanted)

    for html_file in html_files:
        relative = html_file.relative_to(build_dir)
        page_path = "/" if relative == Path("index.html") else "/" + relative.as_posix().removesuffix("index.html")
        page_url = urljoin(base_url, page_path)
        parser = References()
        try:
            parser.feed(html_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{relative}: cannot read HTML: {exc}")
            continue

        if len(parser.canonicals) != 1:
            errors.append(f"{relative}: expected one canonical URL, found {len(parser.canonicals)}")
        elif not parser.is_redirect and parser.canonicals[0] != page_url:
            errors.append(f"{relative}: canonical {parser.canonicals[0]!r} should be {page_url!r}")

        for tag, raw_url in parser.urls:
            if raw_url.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
                continue
            resolved = urlsplit(urljoin(page_url, raw_url))
            if resolved.hostname != base.hostname:
                continue
            if resolved.scheme != "https":
                errors.append(f"{relative}: internal {tag} URL is not HTTPS: {raw_url}")
                continue
            target = output_path(build_dir, resolved.path)
            if not target.is_file():
                errors.append(f"{relative}: missing internal target {resolved.path} (from {raw_url!r})")

    sitemap = build_dir / "sitemap.xml"
    if not sitemap.is_file():
        errors.append("missing sitemap.xml")
    else:
        text = sitemap.read_text(encoding="utf-8")
        foreign = [url for url in re.findall(r"<loc>(.*?)</loc>", text) if not url.startswith(base_url)]
        errors.extend(f"sitemap URL is outside {base_url}: {url}" for url in foreign)
    if not (build_dir / "robots.txt").is_file():
        errors.append("missing robots.txt")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("build_dir", type=Path)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    args = parser.parse_args()
    errors = validate(args.build_dir.resolve(), args.base_url)
    if errors:
        print(f"Build validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1
    count = sum(1 for path in args.build_dir.rglob("*") if path.is_file())
    print(f"Validated {count} generated files and all internal HTML references for {args.base_url}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
