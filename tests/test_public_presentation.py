from pathlib import Path
import json
import struct
import unittest


ROOT = Path(__file__).resolve().parent.parent


class PublicPresentationTests(unittest.TestCase):
    def test_current_display_title_keeps_the_supported_invocation_identity(self) -> None:
        title = "Signal Loom Infographics"
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(title, manifest["product_name"])
        self.assertEqual("signal-loom", manifest["name"])
        self.assertEqual("0.2.0", manifest["version"])
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("\nname: signal-loom\n", skill)
        self.assertIn(f"\n# {title}\n", skill)
        agent = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn(f'  display_name: "{title}"', agent)
        self.assertIn("$signal-loom", agent)
        page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        self.assertIn(f'<meta property="og:title" content="{title}">', page)
        self.assertIn(f'<meta name="twitter:title" content="{title}">', page)
        self.assertIn(f'<span>{title}</span>', page)
        self.assertIn(f"<strong>{title}</strong>", page)
        recovery = (ROOT / "docs" / "404.html").read_text(encoding="utf-8")
        self.assertIn(f"<title>Not found · {title}</title>", recovery)

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

    def test_social_metadata_uses_deployable_jpg(self) -> None:
        page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        card = ROOT / "docs" / "assets" / "signal-loom-social-card.jpg"
        self.assertTrue(card.is_file())
        self.assertLess(card.stat().st_size, 1024 * 1024)
        self.assertEqual(2, page.count("signal-loom-social-card.jpg"))
        self.assertNotIn("signal-loom-social-card.png", page)
        master = (ROOT / "docs" / "assets" / "signal-loom-social-card.png").read_bytes()
        self.assertEqual(b"\x89PNG\r\n\x1a\n", master[:8])
        width, height = struct.unpack(">II", master[16:24])
        self.assertIn(f'<meta property="og:image:width" content="{width}">', page)
        self.assertIn(f'<meta property="og:image:height" content="{height}">', page)

    def test_readme_leads_with_the_product(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        opening = readme[:600]
        self.assertIn("Signal Loom Infographics makes infographics.", opening)
        self.assertIn("What you give it", readme)
        self.assertIn("What it makes", readme)
        self.assertIn("Make your first infographic", readme)


if __name__ == "__main__":
    unittest.main()