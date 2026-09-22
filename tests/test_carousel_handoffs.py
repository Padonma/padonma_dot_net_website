from __future__ import annotations

import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "validate-carousel-handoffs.py"
SPEC = importlib.util.spec_from_file_location("validate_carousel_handoffs", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)

SAMPLE_IMAGE = ROOT / "content" / "topics" / "padonma-network" / "dotted-p-icon-r7.png"


class CarouselHandoffTests(unittest.TestCase):
    def test_repository_content_handoffs(self):
        handoffs, errors = validator.validate_content(ROOT)
        self.assertFalse(errors, "\n".join(errors))
        self.assertGreater(len(handoffs), 0)

    def test_reports_all_contract_violations(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "content" / "source"
            destination = root / "content" / "destination"
            source.mkdir(parents=True)
            destination.mkdir(parents=True)
            (source / "index.md").write_text("---\ntitle: Source\n---\n", encoding="utf-8")
            (destination / "index.md").write_text(
                "---\ntitle: Destination\n---\n", encoding="utf-8"
            )
            (destination / "shared.jpg").touch()
            (source / "carousel.yaml").write_text(
                "- image: /destination/shared.jpg\n  hash: source-hash\n  link: /destination/\n",
                encoding="utf-8",
            )
            (destination / "carousel.yaml").write_text(
                "- image: shared.jpg\n  hash: destination-hash\n", encoding="utf-8"
            )
            _, errors = validator.validate_content(root)
            self.assertEqual(len(errors), 2)
            self.assertTrue(any("needs a fragment" in error for error in errors))
            self.assertTrue(any("hashes differ" in error for error in errors))

    def test_allows_matching_non_carousel_hero_handoff(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "content" / "topics" / "source"
            destination = root / "content" / "topics" / "destination"
            source.mkdir(parents=True)
            destination.mkdir(parents=True)
            (root / "content" / "_index.md").write_text(
                "---\ntitle: Home\n---\n", encoding="utf-8"
            )
            (root / "content" / "topics" / "_index.md").write_text(
                "---\ntitle: Topics\n---\n", encoding="utf-8"
            )
            (source / "index.md").write_text("---\ntitle: Source\n---\n", encoding="utf-8")
            (destination / "index.md").write_text(
                "---\ntitle: Destination\nhero:\n  image: hero.png\n---\n", encoding="utf-8"
            )
            shutil.copyfile(SAMPLE_IMAGE, destination / "hero.png")
            (source / "carousel.yaml").write_text(
                "- image: /topics/destination/hero.png\n"
                "  hash: destination-hero\n"
                "  link: /topics/destination/\n"
                "  alt: Destination hero\n",
                encoding="utf-8",
            )

            handoffs, errors = validator.validate_content(root)

            self.assertFalse(errors, "\n".join(errors))
            self.assertEqual(len(handoffs), 1)
            self.assertEqual(handoffs[0].destination_kind, "hero")
            self.assertIsNone(handoffs[0].destination_hash)

    def test_rejects_destination_without_carousel_or_hero(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "content" / "topics" / "source"
            destination = root / "content" / "topics" / "destination"
            source.mkdir(parents=True)
            destination.mkdir(parents=True)
            (source / "index.md").write_text("---\ntitle: Source\n---\n", encoding="utf-8")
            shutil.copyfile(SAMPLE_IMAGE, source / "source.png")
            (destination / "index.md").write_text(
                "---\ntitle: Destination\n---\n", encoding="utf-8"
            )
            (source / "carousel.yaml").write_text(
                "- image: source.png\n"
                "  hash: source-image\n"
                "  link: /topics/destination/\n"
                "  alt: Source image\n",
                encoding="utf-8",
            )

            _, errors = validator.validate_content(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("neither carousel.yaml nor a hero image", errors[0])

            result = subprocess.run(
                [
                    "hugo",
                    "--source", str(ROOT),
                    "--contentDir", str(root / "content"),
                    "--destination", str(root / "public"),
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("neither carousel.yaml nor a hero image", result.stdout + result.stderr)

    def test_rejects_non_carousel_handoff_to_a_different_hero(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "content" / "topics" / "source"
            destination = root / "content" / "topics" / "destination"
            source.mkdir(parents=True)
            destination.mkdir(parents=True)
            (source / "index.md").write_text("---\ntitle: Source\n---\n", encoding="utf-8")
            (destination / "index.md").write_text(
                "---\ntitle: Destination\nhero:\n  image: hero.png\n---\n", encoding="utf-8"
            )
            shutil.copyfile(SAMPLE_IMAGE, source / "source.png")
            shutil.copyfile(SAMPLE_IMAGE, destination / "hero.png")
            (source / "carousel.yaml").write_text(
                "- image: source.png\n"
                "  hash: source-image\n"
                "  link: /topics/destination/\n"
                "  alt: Source image\n",
                encoding="utf-8",
            )

            _, errors = validator.validate_content(root)

            self.assertEqual(len(errors), 1)
            self.assertIn("does not use the destination hero image", errors[0])

    def test_hugo_renders_matching_hero_transition_names(self):
        with tempfile.TemporaryDirectory() as temporary:
            temporary_path = Path(temporary)
            content = temporary_path / "content"
            output = temporary_path / "public"
            source = content / "topics" / "source"
            destination = content / "topics" / "destination"
            source.mkdir(parents=True)
            destination.mkdir(parents=True)
            (content / "_index.md").write_text("---\ntitle: Home\n---\n", encoding="utf-8")
            (content / "topics" / "_index.md").write_text(
                "---\ntitle: Topics\n---\n", encoding="utf-8"
            )
            (source / "index.md").write_text("---\ntitle: Source\n---\n", encoding="utf-8")
            (destination / "index.md").write_text(
                "---\ntitle: Destination\nhero:\n  image: hero.png\n---\n", encoding="utf-8"
            )
            shutil.copyfile(SAMPLE_IMAGE, destination / "hero.png")
            (source / "carousel.yaml").write_text(
                "- image: /topics/destination/hero.png\n"
                "  hash: destination-hero\n"
                "  link: /topics/destination/\n"
                "  alt: Destination hero\n",
                encoding="utf-8",
            )
            handoffs, errors = validator.validate_content(temporary_path)
            self.assertFalse(errors, "\n".join(errors))

            subprocess.run(
                [
                    "hugo",
                    "--source", str(ROOT),
                    "--contentDir", str(content),
                    "--destination", str(output),
                    "--quiet",
                ],
                check=True,
            )

            errors = validator.validate_rendered(output, handoffs)
            self.assertFalse(errors, "\n".join(errors))

    def test_rendered_handoffs(self):
        handoffs, errors = validator.validate_content(ROOT)
        self.assertFalse(errors, "\n".join(errors))
        with tempfile.TemporaryDirectory() as temporary:
            subprocess.run(
                ["hugo", "--source", str(ROOT), "--destination", temporary, "--quiet"],
                check=True,
            )
            errors = validator.validate_rendered(Path(temporary), handoffs)
        self.assertFalse(errors, "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
