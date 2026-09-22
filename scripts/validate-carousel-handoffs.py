#!/usr/bin/env python3
"""Validate image-preserving links between Hugo carousels."""

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


def page_url(carousel: Path, content: Path) -> str:
    for name in ("index.md", "_index.md"):
        index = carousel.parent / name
        if not index.is_file():
            continue
        front_matter = index.read_text(encoding="utf-8").split("---", 2)
        if len(front_matter) == 3:
            match = re.search(r"(?m)^url:\s*(.+?)\s*$", front_matter[1])
            if match:
                return normalize_url_path(scalar(match.group(1)))
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


class Handoff(NamedTuple):
    source_url: str
    source_hash: str
    destination_url: str
    destination_hash: str
    link: str


def validate_content(root: Path) -> tuple[list[Handoff], list[str]]:
    content = root / "content"
    carousels = sorted(content.rglob("carousel.yaml"))
    by_url = {page_url(path, content): (path, load_carousel(path)) for path in carousels}
    errors: list[str] = []
    handoffs: list[Handoff] = []

    for source_url, (source_path, slides) in by_url.items():
        for position, slide in enumerate(slides, 1):
            link = slide.get("link", "").strip()
            if not link.startswith("/") or link.startswith("//"):
                continue
            parsed = urlsplit(link)
            destination_url = normalize_url_path(parsed.path)
            destination = by_url.get(destination_url)
            source_image = image_identity(slide.get("image", ""), source_path, content)

            if parsed.fragment:
                if destination is None:
                    errors.append(f"{source_path}:{position}: {link!r} has no destination carousel")
                    continue
            elif destination is None:
                continue  # Ordinary navigation to a page without a carousel.
            else:
                destination_path, destination_slides = destination
                shared = [item for item in destination_slides if image_identity(
                    item.get("image", ""), destination_path, content) == source_image]
                if not shared:
                    continue  # Ordinary navigation, even though the page has a carousel.
                errors.append(f"{source_path}:{position}: carousel handoff {link!r} needs a fragment")
                if len(shared) == 1 and slide.get("hash") != shared[0].get("hash"):
                    errors.append(
                        f"{source_path}:{position}: shared image hashes differ: "
                        f"{slide.get('hash')!r} != {shared[0].get('hash')!r}"
                    )
                continue

            destination_path, destination_slides = destination
            matches = [item for item in destination_slides if item.get("hash") == parsed.fragment]
            if len(matches) != 1:
                errors.append(
                    f"{source_path}:{position}: {link!r} matches {len(matches)} destination slides; expected 1"
                )
                continue
            destination_image = image_identity(matches[0].get("image", ""), destination_path, content)
            if source_image != destination_image:
                errors.append(f"{source_path}:{position}: {link!r} does not select the linked source image")
            if slide.get("hash") != parsed.fragment:
                errors.append(
                    f"{source_path}:{position}: source hash {slide.get('hash')!r} "
                    f"does not equal destination hash {parsed.fragment!r}"
                )
            if source_image == destination_image and slide.get("hash") == parsed.fragment:
                handoffs.append(Handoff(source_url, slide["hash"], destination_url, parsed.fragment, link))

    return handoffs, errors


class CarouselHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.slides: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        classes = values.get("class", "").split()
        if tag in {"a", "button"} and "hero-carousel-slide" in classes:
            self.slides.append(values)


def rendered_slides(rendered: Path, url: str) -> list[dict[str, str]]:
    path = rendered / url.lstrip("/") / "index.html"
    parser = CarouselHTMLParser()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValidationError(f"rendered page is missing: {path}") from None
    return parser.slides


def validate_rendered(rendered: Path, handoffs: list[Handoff]) -> list[str]:
    errors: list[str] = []
    cache: dict[str, list[dict[str, str]]] = {}
    for handoff in handoffs:
        source = cache.setdefault(handoff.source_url, rendered_slides(rendered, handoff.source_url))
        destination = cache.setdefault(
            handoff.destination_url, rendered_slides(rendered, handoff.destination_url)
        )
        anchors = [
            slide for slide in source
            if slide.get("data-hash") == handoff.source_hash and slide.get("href") == handoff.link
        ]
        if len(anchors) != 1:
            errors.append(
                f"rendered {handoff.source_url} does not contain one {handoff.source_hash!r} "
                f"anchor with href {handoff.link!r}"
            )
        matches = [slide for slide in destination if slide.get("data-hash") == handoff.destination_hash]
        if len(matches) != 1:
            errors.append(
                f"rendered {handoff.destination_url} contains {len(matches)} slides with "
                f"data-hash {handoff.destination_hash!r}; expected 1"
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
