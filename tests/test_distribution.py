"""Distribution-layout checks never install a Skill or fetch provider content."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skill/polyfork-assets"


class DistributionTests(unittest.TestCase):
    def test_isolated_skill_copy_has_working_entry_points_and_relative_references(self):
        """The distributable folder works without repository packaging imports."""
        with TemporaryDirectory() as temporary:
            copied = Path(temporary) / "polyfork-assets"
            shutil.copytree(SKILL, copied, ignore=shutil.ignore_patterns("__pycache__"))
            for name in ("polyfork_assets.py", "check_readback.py"):
                result = subprocess.run(
                    [sys.executable, str(copied / "scripts" / name), "--help"],
                    cwd=temporary, capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            result = subprocess.run(
                [sys.executable, str(copied / "scripts/check_readback.py"),
                 str(copied / "references/scene-plan.json"),
                 str(copied / "references/readback-fixture.json")],
                cwd=temporary, capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["native_acceptance"], "not_established")
            for path in copied.rglob("*"):
                if path.is_file():
                    self.assertEqual(hashlib.sha256(path.read_bytes()).digest(),
                                     hashlib.sha256((SKILL / path.relative_to(copied)).read_bytes()).digest())

    def test_skill_file_allowlist_excludes_vendor_payloads_and_raw_receipts(self):
        """The installable folder has an explicit small public payload."""
        expected = {
            "LICENSE", "SKILL.md", "scripts/polyfork_assets.py",
            "scripts/check_readback.py", "scripts/blender_acceptance.py",
            "references/sources.md", "references/native-validation.md",
            "references/scene-plan.json", "references/readback-fixture.json",
        }
        actual = {p.relative_to(SKILL).as_posix() for p in SKILL.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts}
        self.assertEqual(actual, expected)

    def test_tool_and_source_contract(self):
        """Keep task definitions separate from pinned tools and source lineage."""
        import tomllib

        config = tomllib.loads((ROOT / "vx.toml").read_text())
        self.assertEqual(set(config), {"tools"})
        self.assertEqual(config["tools"]["python"], "3.12.12")
        history = json.loads((ROOT / "docs/source-history.json").read_text())
        self.assertEqual(history["source_commit"], "fd6064c7d7beb86f5f187f129fde04af3b239b99")
        self.assertEqual(len(history["files"]), 11)
        for entry in history["files"]:
            self.assertEqual(len(entry["source_blob"]), 40)
            self.assertTrue((ROOT / entry["destination_path"]).is_file())


if __name__ == "__main__":
    unittest.main()
