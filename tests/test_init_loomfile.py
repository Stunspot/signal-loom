from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.init_loomfile import REQUIRED_DIRECTORIES, initialize
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


if __name__ == "__main__":
    unittest.main()