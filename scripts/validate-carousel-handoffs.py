#!/usr/bin/env python3
"""Validate image-preserving links from Hugo carousels."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import NamedTuple
from urllib.parse import unquote, urlsplit


class ValidationError(Exception):
    pass


IMAGE_SUFFIXES = {".bmp", ".gif", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}


def scalar(text: str) -> str:
    value = text.strip()
    if value.startswith('"'):
        return str(json.loads(value))
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def load_carousel(path: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        match = re.fullmatch(r"-\s+([A-Za-z][\w-]*):\s*(.*)", raw)
        if match:
            current = {match.group(1): scalar(match.group(2))}
            entries.append(current)
            continue
        match = re.fullmatch(r"  ([A-Za-z][\w-]*):\s*(.*)", raw)
        if match and current is not None:
            current[match.group(1)] = scalar(match.group(2))
        elif not raw.startswith("    "):
            raise ValidationError(f"{path}:{number}: unsupported carousel YAML structure")
    return entries


def front_matter(index: Path) -> str:
    parts = index.read_text(encoding="utf-8").split("---", 2)
    return parts[1] if len(parts) == 3 else ""


def page_url_from_index(index: Path, content: Path) -> str:
    match = re.search(r"(?m)^url:\s*(.+?)\s*$", front_matter(index))
    if match:
        return normalize_url_path(scalar(match.group(1)))
    relative = index.parent.relative_to(content).as_posix()
    return "/" if relative == "." else f"/{relative}/"


def page_url(carousel: Path, content: Path) -> str:
    for name in ("index.md", "_index.md"):
        index = carousel.parent / name
        if index.is_file():
            return page_url_from_index(index, content)
    relative = carousel.parent.relative_to(content).as_posix()
    return "/" if relative == "." else f"/{relative}/"


def normalize_url_path(value: str) -> str:
    path = unquote(value)
    return "/" if path == "/" else f"/{path.strip('/')}/"


def image_identity(image: str, carousel: Path, content: Path) -> Path | None:
    parts = urlsplit(image)
    if parts.scheme or parts.netloc:
        return None
    if image.startswith("/"):
        return (content / unquote(parts.path).lstrip("/")).resolve()
    return (carousel.parent / unquote(parts.path)).resolve()


def hero_image_identity(index: Path) -> Path | None:
    metadata = front_matter(index)
    hero = re.search(r"(?ms)^hero:\s*(?:#.*)?\n(?P<body>(?:^[ \t]+.*(?:\n|$))*)", metadata)
    if hero:
        image = re.search(r"(?m)^\s{2,}image:\s*(.+?)\s*$", hero.group("body"))
        if image:
            candidate = (index.parent / scalar(image.group(1))).resolve()
            if candidate.is_file() and candidate.suffix.lower() in IMAGE_SUFFIXES:
                return candidate
            return None
    images = sorted(
        path.resolve()
        for path in index.parent.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )
    return images[0] if images else None


class Page(NamedTuple):
    index: Path
    carousel: Path | None
    slides: list[dict[str, str]]
    hero_image: Path | None


class Handoff(NamedTuple):
    source_url: str
    source_hash: str
    destination_url: str
    destination_hash: str | None
    link: str
    destination_kind: str


def validate_content(root: Path) -> tuple[list[Handoff], list[str]]:
    content = root / "content"
    pages: dict[str, Page] = {}
    for index in sorted(path for path in content.rglob("*.md") if path.name in {"index.md", "_index.md"}):
        carousel = index.parent / "carousel.yaml"
        pages[page_url_from_index(index, content)] = Page(
            index,
            carousel if carousel.is_file() else None,
            load_carousel(carousel) if carousel.is_file() else [],
            hero_image_identity(index),
        )
    errors: list[str] = []
    handoffs: list[Handoff] = []

    for source_url, source in pages.items():
        if source.carousel is None:
            continue
        for position, slide in enumerate(source.slides, 1):
            link = slide.get("link", "").strip()
            if not link.startswith("/") or link.startswith("//"):
                continue
            parsed = urlsplit(link)
            destination_url = normalize_url_path(parsed.path)
            destination = pages.get(destination_url)
            source_image = image_identity(slide.get("image", ""), source.carousel, content)

            if destination is None:
                errors.append(f"{source.carousel}:{position}: {link!r} has no destination page")
                continue

            if destination.carousel is None:
                if parsed.fragment:
                    errors.append(
                        f"{source.carousel}:{position}: carousel-to-hero link {link!r} must not include a fragment"
                    )
                    continue
                if destination.hero_image is None:
                    errors.append(
                        f"{source.carousel}:{position}: {link!r} points to a page with neither "
                        "carousel.yaml nor a hero image"
                    )
                    continue
                if source_image != destination.hero_image:
                    errors.append(
                        f"{source.carousel}:{position}: {link!r} does not use the destination hero image"
                    )
                    continue
                handoffs.append(
                    Handoff(source_url, slide["hash"], destination_url, None, link, "hero")
                )
                continue

            if not parsed.fragment:
                shared = [item for item in destination.slides if image_identity(
                    item.get("image", ""), destination.carousel, content) == source_image]
                if not shared:
                    continue  # Ordinary navigation, even though the page has a carousel.
                errors.append(f"{source.carousel}:{position}: carousel handoff {link!r} needs a fragment")
                if len(shared) == 1 and slide.get("hash") != shared[0].get("hash"):
                    errors.append(
                        f"{source.carousel}:{position}: shared image hashes differ: "
                        f"{slide.get('hash')!r} != {shared[0].get('hash')!r}"
                    )
                continue

            matches = [item for item in destination.slides if item.get("hash") == parsed.fragment]
            if len(matches) != 1:
                errors.append(
                    f"{source.carousel}:{position}: {link!r} matches {len(matches)} destination slides; expected 1"
                )
                continue
            destination_image = image_identity(
                matches[0].get("image", ""), destination.carousel, content
            )
            if source_image != destination_image:
                errors.append(
                    f"{source.carousel}:{position}: {link!r} does not select the linked source image"
                )
            if slide.get("hash") != parsed.fragment:
                errors.append(
                    f"{source.carousel}:{position}: source hash {slide.get('hash')!r} "
                    f"does not equal destination hash {parsed.fragment!r}"
                )
            if source_image == destination_image and slide.get("hash") == parsed.fragment:
                handoffs.append(
                    Handoff(source_url, slide["hash"], destination_url, parsed.fragment, link, "carousel")
                )

    return handoffs, errors


class RenderedPage(NamedTuple):
    slides: list[dict[str, str]]
    detail_heroes: list[dict[str, str]]


class PageHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[dict[str, str]] = []
        self.detail_heroes: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        classes = values.get("class", "").split()
        if tag in {"a", "button"} and "hero-carousel-slide" in classes:
            self.slides.append(values)
        if tag == "img" and "hero-image--detail" in classes:
            self.detail_heroes.append(values)


def rendered_page(rendered: Path, url: str) -> RenderedPage:
    path = rendered / url.lstrip("/") / "index.html"
    parser = PageHTMLParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValidationError(f"rendered page is missing: {path}") from None
    return RenderedPage(parser.slides, parser.detail_heroes)


def style_transition_name(attributes: dict[str, str]) -> str:
    match = re.search(
        r"(?:^|;)\s*view-transition-name\s*:\s*([^;]+)", attributes.get("style", "")
    )
    return match.group(1).strip() if match else ""


def validate_rendered(rendered: Path, handoffs: list[Handoff]) -> list[str]:
    errors: list[str] = []
    cache: dict[str, RenderedPage] = {}
    for handoff in handoffs:
        source = cache.setdefault(handoff.source_url, rendered_page(rendered, handoff.source_url))
        destination = cache.setdefault(
            handoff.destination_url, rendered_page(rendered, handoff.destination_url)
        )
        anchors = [
            slide for slide in source.slides
            if slide.get("data-hash") == handoff.source_hash and slide.get("href") == handoff.link
        ]
        if len(anchors) != 1:
            errors.append(
                f"rendered {handoff.source_url} does not contain one {handoff.source_hash!r} "
                f"anchor with href {handoff.link!r}"
            )
            continue
        transition_name = anchors[0].get("data-view-transition-name", "")
        if handoff.destination_kind == "carousel":
            matches = [
                slide for slide in destination.slides
                if slide.get("data-hash") == handoff.destination_hash
            ]
            if len(matches) != 1:
                errors.append(
                    f"rendered {handoff.destination_url} contains {len(matches)} slides with "
                    f"data-hash {handoff.destination_hash!r}; expected 1"
                )
            if transition_name != "carousel-handoff":
                errors.append(
                    f"rendered carousel handoff {handoff.link!r} uses transition name "
                    f"{transition_name!r}; expected 'carousel-handoff'"
                )
        elif len(destination.detail_heroes) != 1:
            errors.append(
                f"rendered {handoff.destination_url} contains {len(destination.detail_heroes)} "
                "detail hero images; expected 1"
            )
        else:
            destination_name = style_transition_name(destination.detail_heroes[0])
            if not transition_name or transition_name != destination_name:
                errors.append(
                    f"rendered hero handoff {handoff.link!r} uses transition name "
                    f"{transition_name!r}, but its destination hero uses {destination_name!r}"
                )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--rendered-dir", type=Path)
    args = parser.parse_args(argv)
    try:
        handoffs, errors = validate_content(args.root.resolve())
        if args.rendered_dir:
            errors.extend(validate_rendered(args.rendered_dir.resolve(), handoffs))
    except (OSError, UnicodeError, ValidationError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
        handoffs = []
    if errors:
        print("Carousel handoff validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(handoffs)} carousel handoffs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
