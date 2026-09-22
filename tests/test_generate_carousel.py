from __future__ import annotations

import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout


SCRIPT = Path(__file__).parents[1] / "scripts" / "generate-carousel.py"
SPEC = importlib.util.spec_from_file_location("generate_carousel", SCRIPT)
generator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(generator)


class GeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.bundle = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def write_index(self, body="title: Test page"):
        (self.bundle / "index.md").write_text(f"---\n{body}\n---\nBody\n", encoding="utf-8")

    def image(self, name):
        (self.bundle / name).write_bytes(b"not decoded by generator")

    def invoke(self, *args):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = generator.main(list(args))
        return result, stdout.getvalue(), stderr.getvalue()

    def test_current_directory_and_explicit_directory(self):
        self.write_index()
        self.image("one.jpg")
        old = Path.cwd()
        try:
            import os
            os.chdir(self.bundle)
            result, output, _ = self.invoke("--dry-run")
        finally:
            os.chdir(old)
        self.assertEqual(result, 0)
        self.assertIn('image: "one.jpg"', output)
        self.assertEqual(self.invoke(str(self.bundle), "--dry-run")[1], output)

    def test_multiple_images_are_bytewise_sorted_and_canonical_first(self):
        self.write_index("title: Order\nhero:\n  image: z.PNG")
        for name in ("z.PNG", "a.webp", "B.JPEG"):
            self.image(name)
        entries, _ = generator.proposed(self.bundle)
        self.assertEqual([entry["image"] for entry in entries], ["z.PNG", "B.JPEG", "a.webp"])

    def test_implicit_hero_and_avif_exclusion(self):
        self.write_index()
        self.image("b.png")
        self.image("a.jpg")
        self.image("ignored.AVIF")
        entries, excluded = generator.proposed(self.bundle)
        self.assertEqual(entries[0]["image"], "a.jpg")
        self.assertEqual([path.name for path in excluded], ["ignored.AVIF"])

    def test_other_hugo_rasters_and_generated_derivatives(self):
        self.write_index()
        self.image("animation.GIF")
        self.image("scan.TIFF")
        self.image("animation_hu_0123456789abcdef.webp")
        entries, _ = generator.proposed(self.bundle)
        self.assertEqual([entry["image"] for entry in entries], ["animation.GIF", "scan.TIFF"])

    def test_unicode_and_quoted_title_are_yaml_safe(self):
        self.write_index('title: "Lotus: café #1"')
        self.image("one.jpg")
        output = generator.render(generator.proposed(self.bundle)[0])
        self.assertIn('alt: "Lotus: café #1"', output)

    def test_focal_coordinate_precedence_and_unquoted_y(self):
        self.write_index("""title: Focal
hero:
  image: hero.jpg
  focal:
    x: 0.2
    y: 0.3
images:
  - file: hero.jpg
    focal:
      x: 0.4
  - file: other.png
    focal:
      \"y\": 1""")
        self.image("hero.jpg")
        self.image("other.png")
        entries, _ = generator.proposed(self.bundle)
        self.assertEqual(entries[0]["focal"], {"x": 0.4, "y": 0.3})
        self.assertEqual(entries[1]["focal"], {"x": 0.5, "y": 1})

    def test_invalid_focal_fails(self):
        self.write_index("title: Bad\nhero:\n  focal:\n    x: 2")
        self.image("one.jpg")
        with self.assertRaisesRegex(generator.CarouselError, "outside"):
            generator.proposed(self.bundle)

    def test_hash_uses_final_extension_only(self):
        self.write_index()
        self.image("lotus_silk.economics.1.png")
        entry = generator.proposed(self.bundle)[0][0]
        self.assertEqual(entry["hash"], "lotus-silk-economics-1")

    def test_invalid_hash_and_collision_fail(self):
        self.write_index()
        self.image("bad name.jpg")
        with self.assertRaisesRegex(generator.CarouselError, "invalid hash"):
            generator.proposed(self.bundle)
        (self.bundle / "bad name.jpg").unlink()
        self.image("same.jpg")
        self.image("same.png")
        with self.assertRaisesRegex(generator.CarouselError, "both derive"):
            generator.proposed(self.bundle)

    def test_generation_refuses_overwrite_and_check_modes(self):
        self.write_index()
        self.image("one.jpg")
        self.assertEqual(self.invoke(str(self.bundle))[0], 0)
        original = (self.bundle / "carousel.yaml").read_bytes()
        self.assertEqual(self.invoke(str(self.bundle))[0], 1)
        self.assertEqual((self.bundle / "carousel.yaml").read_bytes(), original)
        self.assertEqual(self.invoke(str(self.bundle), "--check")[0], 0)
        (self.bundle / "carousel.yaml").write_text(original.decode().replace("0.5", "0.4", 1))
        self.assertEqual(self.invoke(str(self.bundle), "--check")[0], 1)

    def test_dry_run_is_deterministic_and_never_emits_link(self):
        self.write_index()
        self.image("one.jpg")
        first = self.invoke(str(self.bundle), "--dry-run")
        second = self.invoke(str(self.bundle), "--dry-run")
        self.assertEqual(first, second)
        self.assertNotIn("link:", first[1])
        self.assertFalse((self.bundle / "carousel.yaml").exists())


if __name__ == "__main__":
    unittest.main()
