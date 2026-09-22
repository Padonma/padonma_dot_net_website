from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "validate-carousel-handoffs.py"
SPEC = importlib.util.spec_from_file_location("validate_carousel_handoffs", SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)


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
