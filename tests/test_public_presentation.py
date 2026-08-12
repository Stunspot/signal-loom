from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parent.parent


class PublicPresentationTests(unittest.TestCase):
    def test_wide_viewport_cannot_collapse_the_content_column(self) -> None:
        css = (ROOT / "docs" / "style.css").read_text(encoding="utf-8")
        self.assertIn(
            ".hero,.section{width:min(82rem,calc(100% - 2rem));margin:auto;"
            "padding:clamp(4.5rem,8vw,7rem) 0}",
            css,
        )
        self.assertNotIn(
            ".hero,.section{width:min(86rem,100%);margin:auto;"
            "padding:clamp(4.5rem,8vw,7rem) max(1rem,calc((100% - 82rem)/2))}",
            css,
        )

    def test_readme_leads_with_the_product(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        opening = readme[:600]
        self.assertIn("Signal Loom makes infographics.", opening)
        self.assertIn("What you give it", readme)
        self.assertIn("What it makes", readme)
        self.assertIn("Make your first infographic", readme)


if __name__ == "__main__":
    unittest.main()