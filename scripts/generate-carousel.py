#!/usr/bin/env python3
"""Generate deterministic carousel.yaml data for a Hugo leaf page bundle."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any


IMAGE_SUFFIXES = {".bmp", ".gif", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}
HASH_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")
HUGO_DERIVATIVE_RE = re.compile(r"_hu_[0-9a-f]{16,}\.[^.]+$", re.IGNORECASE)


class CarouselError(Exception):
    pass


def split_comment(value: str) -> str:
    quote = None
    escaped = False
    for index, char in enumerate(value):
        if escaped:
            escaped = False
        elif quote == '"' and char == "\\":
            escaped = True
        elif quote:
            if char == quote:
                quote = None
        elif char in "'\"":
            quote = char
        elif char == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    if quote:
        raise CarouselError("unterminated quoted YAML scalar")
    return value.rstrip()


def scalar(value: str) -> Any:
    value = split_comment(value).strip()
    if not value:
        return None
    if value.startswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise CarouselError(f"invalid double-quoted YAML scalar {value!r}: {exc.msg}") from exc
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            raise CarouselError(f"invalid single-quoted YAML scalar {value!r}")
        return value[1:-1].replace("''", "'")
    lowered = value.lower()
    if lowered in {"null", "~"}:
        return None
    if lowered in {"true", "false"}:
        return lowered == "true"
    if re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", value):
        return float(value) if any(char in value for char in ".eE") else int(value)
    if value[0] in "[{&*!|>":
        raise CarouselError(f"unsupported YAML syntax in scalar {value!r}; use a plain or quoted scalar")
    return value


def key_value(text: str, *, line: int) -> tuple[str, Any]:
    match = re.match(r'^("(?:[^"\\]|\\.)*"|\'[^\']*\'|[^:]+):(?:\s*(.*))?$', text)
    if not match:
        raise CarouselError(f"line {line}: expected a YAML key followed by ':'")
    raw_key, raw_value = match.groups()
    parsed_key = scalar(raw_key.strip())
    if not isinstance(parsed_key, (str, bool)):
        raise CarouselError(f"line {line}: invalid YAML mapping key {raw_key!r}")
    # YAML 1.1 treats an unquoted y as boolean true. Preserve that repository behavior.
    key = "y" if parsed_key is True or (isinstance(parsed_key, str) and parsed_key == "y") else str(parsed_key)
    return key, scalar(raw_value or "")


def parse_front_matter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise CarouselError(f"cannot read {path}: {exc}") from exc
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise CarouselError(f"{path}: expected YAML front matter beginning with ---")
    try:
        end = next(index for index in range(1, len(lines)) if lines[index].strip() == "---")
    except StopIteration as exc:
        raise CarouselError(f"{path}: YAML front matter has no closing ---") from exc

    data: dict[str, Any] = {}
    current: str | None = None
    image: dict[str, Any] | None = None
    image_subsection: str | None = None
    for offset, raw in enumerate(lines[1:end], start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if "\t" in raw[:indent]:
            raise CarouselError(f"{path}: line {offset}: tabs are not supported in YAML indentation")
        text_line = raw.strip()
        if indent == 0:
            key, value = key_value(text_line, line=offset)
            if key in data:
                raise CarouselError(f"{path}: line {offset}: duplicate top-level field {key!r}")
            if key in {"hero", "images"} and value is not None:
                raise CarouselError(f"{path}: line {offset}: {key} must be an indented mapping/list")
            data[key] = [] if key == "images" else ({} if key == "hero" else value)
            current = key
            image = None
            image_subsection = None
        elif current == "hero":
            if indent not in {2, 4}:
                raise CarouselError(f"{path}: line {offset}: ambiguous hero metadata indentation")
            key, value = key_value(text_line, line=offset)
            hero = data["hero"]
            if indent == 2:
                if key in hero:
                    raise CarouselError(f"{path}: line {offset}: duplicate hero.{key}")
                hero[key] = {} if key == "focal" and value is None else value
            elif indent == 4 and isinstance(hero.get("focal"), dict):
                if key in hero["focal"]:
                    raise CarouselError(f"{path}: line {offset}: duplicate hero.focal.{key}")
                hero["focal"][key] = value
            else:
                raise CarouselError(f"{path}: line {offset}: unexpected nested hero field")
        elif current == "images":
            if indent == 2 and text_line.startswith("-"):
                remainder = text_line[1:].strip()
                image = {}
                data["images"].append(image)
                image_subsection = None
                if remainder:
                    key, value = key_value(remainder, line=offset)
                    image[key] = value
            elif indent == 4 and image is not None:
                key, value = key_value(text_line, line=offset)
                if key in image:
                    raise CarouselError(f"{path}: line {offset}: duplicate images[].{key}")
                image[key] = {} if key == "focal" and value is None else value
                image_subsection = key
            elif indent == 6 and image is not None and image_subsection == "focal":
                key, value = key_value(text_line, line=offset)
                focal = image["focal"]
                if key in focal:
                    raise CarouselError(f"{path}: line {offset}: duplicate images[].focal.{key}")
                focal[key] = value
            else:
                raise CarouselError(f"{path}: line {offset}: ambiguous images metadata")
        # Unrelated nested front matter is deliberately ignored.
    return data


def image_files(directory: Path) -> tuple[list[Path], list[Path]]:
    supported: list[Path] = []
    excluded_avif: list[Path] = []
    for path in directory.iterdir():
        if (not path.is_file() or path.name.startswith((".", "#"))
                or path.name.endswith(("~", ".tmp")) or HUGO_DERIVATIVE_RE.search(path.name)):
            continue
        suffix = path.suffix.lower()
        if suffix == ".avif":
            excluded_avif.append(path)
        elif suffix in IMAGE_SUFFIXES:
            supported.append(path)
    # Hugo 0.147.9 page resources were measured to use bytewise Name order.
    return sorted(supported, key=lambda path: path.name), sorted(excluded_avif, key=lambda path: path.name)


def coordinate(value: Any, field: str, directory: Path) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise CarouselError(f"{directory}: {field} must be a finite number in [0, 1]; correct the front matter")
    if value < 0 or value > 1:
        raise CarouselError(f"{directory}: {field} is {value!r}, outside [0, 1]; correct the front matter")
    return value


def proposed(directory: Path) -> tuple[list[dict[str, Any]], list[Path]]:
    index = directory / "index.md"
    if not index.is_file():
        raise CarouselError(f"{directory}: missing regular index.md; target a Hugo leaf page bundle")
    metadata = parse_front_matter(index)
    title = metadata.get("title")
    if not isinstance(title, str) or not title.strip():
        raise CarouselError(f"{index}: title must be a non-empty string")
    files, excluded_avif = image_files(directory)
    if not files:
        raise CarouselError(f"{directory}: no supported sibling raster images remain; add a Hugo-processable BMP, GIF, JPEG, PNG, TIFF, or WebP image")

    hero = metadata.get("hero") or {}
    if not isinstance(hero, dict):
        raise CarouselError(f"{index}: hero must be a mapping")
    explicit = hero.get("image")
    if explicit is not None and not isinstance(explicit, str):
        raise CarouselError(f"{index}: hero.image must be a filename string")
    names = {path.name: path for path in files}
    if explicit:
        if explicit not in names:
            raise CarouselError(f"{directory}: hero.image {explicit!r} is not a supported sibling image; correct hero.image or restore the file")
        canonical = names[explicit]
    else:
        canonical = files[0]
    ordered = [canonical, *(path for path in files if path != canonical)]

    focal_by_file: dict[str, dict[str, Any]] = {}
    for pos, item in enumerate(metadata.get("images") or [], start=1):
        if not isinstance(item, dict) or not isinstance(item.get("file"), str):
            raise CarouselError(f"{index}: images entry {pos} needs a string file field")
        name = item["file"]
        if name in focal_by_file:
            raise CarouselError(f"{index}: ambiguous duplicate images[] metadata for {name!r}")
        focal = item.get("focal") or {}
        if not isinstance(focal, dict):
            raise CarouselError(f"{index}: images[{name!r}].focal must be a mapping")
        for axis in ("x", "y"):
            if axis in focal:
                coordinate(focal[axis], f"images[{name!r}].focal.{axis}", directory)
        focal_by_file[name] = focal

    entries: list[dict[str, Any]] = []
    hashes: dict[str, str] = {}
    for path in ordered:
        stem = path.name[: -len(path.suffix)]
        derived_hash = stem.replace("_", "-").replace(".", "-")
        if not HASH_RE.fullmatch(derived_hash):
            raise CarouselError(f"{directory}: file {path.name!r} derives invalid hash {derived_hash!r}; rename the source file")
        if derived_hash in hashes:
            raise CarouselError(f"{directory}: files {hashes[derived_hash]!r} and {path.name!r} both derive hash {derived_hash!r}; rename one source file")
        hashes[derived_hash] = path.name
        x: float | int = 0.5
        y: float | int = 0.5
        if path == canonical:
            hero_focal = hero.get("focal") or {}
            if not isinstance(hero_focal, dict):
                raise CarouselError(f"{index}: hero.focal must be a mapping")
            if "x" in hero_focal:
                x = coordinate(hero_focal["x"], "hero.focal.x", directory)
            if "y" in hero_focal:
                y = coordinate(hero_focal["y"], 'hero.focal."y"', directory)
        if path.name in focal_by_file:
            focal = focal_by_file[path.name]
            if "x" in focal:
                x = coordinate(focal["x"], f"images[{path.name!r}].focal.x", directory)
            if "y" in focal:
                y = coordinate(focal["y"], f'images[{path.name!r}].focal."y"', directory)
        entries.append({"image": path.name, "hash": derived_hash, "alt": title, "focal": {"x": x, "y": y}})
    return entries, excluded_avif


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_number(value: float | int) -> str:
    if isinstance(value, int):
        return str(value)
    return format(value, ".15g")


def render(entries: list[dict[str, Any]]) -> str:
    chunks = []
    for entry in entries:
        chunks.extend([
            f"- image: {yaml_string(entry['image'])}",
            f"  hash: {yaml_string(entry['hash'])}",
            f"  alt: {yaml_string(entry['alt'])}",
            "  focal:",
            f"    x: {yaml_number(entry['focal']['x'])}",
            f"    \"y\": {yaml_number(entry['focal']['y'])}",
        ])
    return "\n".join(chunks) + "\n"


def parse_carousel(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    entry: dict[str, Any] | None = None
    subsection = None
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        text_line = raw.strip()
        if indent == 0 and text_line.startswith("-"):
            entry = {}
            entries.append(entry)
            subsection = None
            remainder = text_line[1:].strip()
            if remainder:
                key, value = key_value(remainder, line=line_no)
                entry[key] = value
        elif indent == 2 and entry is not None:
            key, value = key_value(text_line, line=line_no)
            entry[key] = {} if key == "focal" and value is None else value
            subsection = key
        elif indent == 4 and entry is not None and subsection == "focal":
            key, value = key_value(text_line, line=line_no)
            entry["focal"][key] = value
        else:
            raise CarouselError(f"{path}: line {line_no}: unsupported or ambiguous carousel YAML")
    return entries


def comparison_error(actual: list[dict[str, Any]], expected: list[dict[str, Any]]) -> str | None:
    if len(actual) != len(expected):
        return f"entry count is {len(actual)}, expected {len(expected)} (an entry is missing or extra)"
    for index, (found, wanted) in enumerate(zip(actual, expected), start=1):
        if found.get("image") != wanted["image"]:
            return (f"entry {index} has image {found.get('image')!r}, expected {wanted['image']!r} "
                    "(an image is missing, extra, or reordered)")
        missing = sorted(wanted.keys() - found.keys())
        extra = sorted(found.keys() - wanted.keys())
        if missing:
            return f"entry {index} ({wanted['image']}) is missing fields: {', '.join(missing)}"
        if extra:
            return f"entry {index} ({wanted['image']}) has extra fields: {', '.join(extra)}"
        for field in wanted:
            if found[field] != wanted[field]:
                return (f"entry {index} ({wanted['image']}) field {field!r} is {found[field]!r}, "
                        f"expected {wanted[field]!r}")
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", nargs="?", default=".", help="leaf bundle directory (default: current directory)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--dry-run", action="store_true", help="validate and print exact proposed YAML without writing")
    modes.add_argument("--check", action="store_true", help="compare an existing carousel.yaml with generated semantics")
    args = parser.parse_args(argv)
    directory = Path(args.directory).resolve()
    output = directory / "carousel.yaml"
    try:
        if not directory.is_dir():
            raise CarouselError(f"{directory}: target is not a directory")
        if output.exists() and not args.check:
            raise CarouselError(f"{output}: already exists; refusing to overwrite it (use --check to validate)")
        entries, excluded = proposed(directory)
        document = render(entries)
        if excluded:
            print(f"{directory}: excluded AVIF: {', '.join(path.name for path in excluded)}", file=sys.stderr)
        if args.dry_run:
            sys.stdout.write(document)
        elif args.check:
            if not output.is_file():
                raise CarouselError(f"{output}: missing regular file; generate it before using --check")
            actual = parse_carousel(output)
            mismatch = comparison_error(actual, entries)
            if mismatch:
                raise CarouselError(f"{output}: {mismatch}; review the file or regenerate it")
            print(f"{output}: valid ({len(entries)} entries)")
        else:
            temporary: str | None = None
            try:
                with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=directory, prefix=".carousel.", suffix=".tmp", delete=False) as handle:
                    temporary = handle.name
                    handle.write(document)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.link(temporary, output)
            except FileExistsError as exc:
                raise CarouselError(f"{output}: appeared during generation; refusing to overwrite it") from exc
            finally:
                if temporary:
                    Path(temporary).unlink(missing_ok=True)
            print(f"created {output} ({len(entries)} entries)")
    except (CarouselError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
