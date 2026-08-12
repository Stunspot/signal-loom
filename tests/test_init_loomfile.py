from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.init_loomfile import REQUIRED_DIRECTORIES, initialize
from scripts.package_loomfile import package
from scripts.validate_loomfile import validate


class InitializeLoomfileTests(unittest.TestCase):
    def test_new_loomfile_immediately_satisfies_the_state_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "first-project"
            created = initialize(destination, "First project")
            for relative in REQUIRED_DIRECTORIES:
                self.assertTrue((created / relative).is_dir(), relative)
            errors, warnings = validate(created)
            self.assertEqual(errors, [])
            self.assertEqual(warnings, [])

    def test_existing_archive_refusal_preserves_archive_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "project"
            archive = root / "project.zip"
            initialize(destination, "Existing archive")
            package(destination, archive)
            archive_before = archive.read_bytes()
            manifest_path = destination / "review" / "release-manifest.json"
            manifest_before = manifest_path.read_bytes()

            with self.assertRaisesRegex(ValueError, "output already exists"):
                package(destination, archive)

            self.assertEqual(archive.read_bytes(), archive_before)
            self.assertEqual(manifest_path.read_bytes(), manifest_before)


if __name__ == "__main__":
    unittest.main()
