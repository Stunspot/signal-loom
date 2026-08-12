from __future__ import annotations

import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import scripts.package_loomfile as package_module
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
            manifest_path = destination / "review" / "release-manifest.json"
            with zipfile.ZipFile(archive) as packaged_zip:
                archived_manifest = packaged_zip.read("project/review/release-manifest.json")
            self.assertEqual(archived_manifest, manifest_path.read_bytes())
            archive_before = archive.read_bytes()
            manifest_before = manifest_path.read_bytes()

            with self.assertRaisesRegex(ValueError, "output already exists"):
                package(destination, archive)

            self.assertEqual(archive.read_bytes(), archive_before)
            self.assertEqual(manifest_path.read_bytes(), manifest_before)

    def test_manifest_commit_failure_rolls_back_final_archive(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "project"
            archive = root / "project.zip"
            initialize(destination, "Manifest commit failure")
            manifest_path = destination / "review" / "release-manifest.json"
            manifest_before = manifest_path.read_bytes()

            with patch.object(
                package_module.os,
                "replace",
                side_effect=OSError("simulated manifest commit failure"),
            ):
                with self.assertRaisesRegex(OSError, "simulated manifest commit failure"):
                    package(destination, archive)

            self.assertEqual(manifest_path.read_bytes(), manifest_before)
            self.assertFalse(archive.exists())
            self.assertEqual(list(root.glob(f".{archive.name}.*.tmp")), [])
            self.assertEqual(list(manifest_path.parent.glob(".release-manifest.*.tmp")), [])

            packaged, _ = package(destination, archive)
            self.assertEqual(packaged, archive)
            self.assertTrue(archive.is_file())

    def test_competing_output_is_not_overwritten_and_state_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "project"
            archive = root / "project.zip"
            initialize(destination, "Competing archive")
            manifest_path = destination / "review" / "release-manifest.json"
            manifest_before = manifest_path.read_bytes()
            competing_bytes = b"created by another process"

            def create_competing_output(*_args, **_kwargs):  # type: ignore[no-untyped-def]
                archive.write_bytes(competing_bytes)
                raise FileExistsError("simulated competing output")

            with patch.object(package_module.os, "link", side_effect=create_competing_output):
                with self.assertRaisesRegex(FileExistsError, "simulated competing output"):
                    package(destination, archive)

            self.assertEqual(archive.read_bytes(), competing_bytes)
            self.assertEqual(manifest_path.read_bytes(), manifest_before)
            self.assertEqual(list(root.glob(f".{archive.name}.*.tmp")), [])
            self.assertEqual(list(manifest_path.parent.glob(".release-manifest.*.tmp")), [])

    def test_mid_archive_failure_preserves_state_and_allows_retry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "project"
            archive = root / "project.zip"
            initialize(destination, "Interrupted archive")
            manifest_path = destination / "review" / "release-manifest.json"
            manifest_before = manifest_path.read_bytes()
            real_zip_file = zipfile.ZipFile

            class FailingZip(real_zip_file):
                writes = 0

                def write(self, *args, **kwargs):  # type: ignore[no-untyped-def]
                    type(self).writes += 1
                    if type(self).writes == 2:
                        raise OSError("simulated archive write failure")
                    return super().write(*args, **kwargs)

            with patch.object(package_module.zipfile, "ZipFile", FailingZip):
                with self.assertRaisesRegex(OSError, "simulated archive write failure"):
                    package(destination, archive)

            self.assertEqual(manifest_path.read_bytes(), manifest_before)
            self.assertFalse(archive.exists())
            self.assertEqual(list(root.glob(f".{archive.name}.*.tmp")), [])
            self.assertEqual(list(manifest_path.parent.glob(".release-manifest.*.tmp")), [])

            packaged, count = package(destination, archive)
            self.assertEqual(packaged, archive)
            self.assertGreater(count, 1)
            self.assertTrue(archive.is_file())
            self.assertNotEqual(manifest_path.read_bytes(), manifest_before)


if __name__ == "__main__":
    unittest.main()
