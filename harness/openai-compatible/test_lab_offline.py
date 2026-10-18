"""Offline tests of lab.py: pure functions only, no model, no network, no git.

Run from this directory:  python3 -m unittest -v test_lab_offline
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lab  # noqa: E402

T = lab.TERMINATOR


class ExtractFiles(unittest.TestCase):
    def test_two_blocks_and_report_outside(self):
        reply = ("Report line.\n<<<FILE 02_metodo.md>>>\n# Method\nbody\n" + T + "\n<<<END>>>\n"
                 "between\n<<<FILE 04_impl/a.py>>>\nprint(1)\n<<<END>>>\ntail")
        files = lab.extract_files(reply)
        self.assertEqual([p for p, _ in files], ["02_metodo.md", "04_impl/a.py"])
        self.assertEqual(files[0][1], "# Method\nbody\n" + T + "\n")
        self.assertEqual(files[1][1], "print(1)\n")
        self.assertEqual(lab.strip_blocks(reply), "Report line.\n\nbetween\n\ntail")

    def test_empty_block_and_spaces_in_marker(self):
        files = lab.extract_files("<<<FILE   x.md  >>>\n<<<END>>>")
        self.assertEqual(files, [("x.md", "")])

    def test_unterminated_block_is_ignored(self):
        self.assertEqual(lab.extract_files("<<<FILE x.md>>>\nhalf a file"), [])

    def test_end_marker_must_start_the_line(self):
        files = lab.extract_files("<<<FILE x.md>>>\nsee <<<END>>> inline\n<<<END>>>")
        self.assertEqual(files, [("x.md", "see <<<END>>> inline\n")])


class SafePath(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.run = Path(self.tmp.name) / "run"
        self.run.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_accepts_relative_paths_inside(self):
        p = lab.safe_path(self.run, "04_impl/logs/x.txt")
        self.assertEqual(p, (self.run / "04_impl/logs/x.txt").resolve())

    def test_refuses_escapes(self):
        for bad in ["../x.md", "04_impl/../../x.md", "a/..", "..\\x.md", "/etc/passwd",
                    "\\x", "~/x", "C:\\x", "C:/x", "", "   "]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                lab.safe_path(self.run, bad)

    def test_refuses_the_run_dir_itself(self):
        with self.assertRaises(ValueError):
            lab.safe_path(self.run, ".")

    def test_refuses_symlink_escape(self):
        outside = Path(self.tmp.name) / "outside"
        outside.mkdir()
        (self.run / "link").symlink_to(outside)
        with self.assertRaises(ValueError):
            lab.safe_path(self.run, "link/x.md")


class CheckComplete(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        p = self.dir / "doc.md"
        p.write_text(text, encoding="utf-8")
        return p

    def test_complete(self):
        self.assertIsNone(lab.check_complete(self.write("# A\nbody\n" + T + "\n")))

    def test_trailing_blank_lines_are_fine(self):
        self.assertIsNone(lab.check_complete(self.write("# A\n" + T + "\n\n  \n")))

    def test_missing_file(self):
        self.assertEqual(lab.check_complete(self.dir / "nope.md"), "missing")

    def test_empty(self):
        self.assertEqual(lab.check_complete(self.write("  \n\n")), "empty")

    def test_no_terminator(self):
        self.assertIn("does not end with", lab.check_complete(self.write("# A\nhalf")))

    def test_terminator_not_at_the_end(self):
        self.assertIsNotNone(lab.check_complete(self.write(T + "\nmore text after it\n")))


class ParseCommands(unittest.TestCase):
    def test_english_heading(self):
        md = ("# How to run\n\n## Prerequisites\n\n```bash\npip install x\n```\n\n"
              "## Run the full protocol\n\nAll 5 seeds:\n\n```bash\n# comment\n"
              "python3 -m venv .venv\n\n  .venv/bin/python run.py --seeds 1-5  \n```\n\n"
              "## Where the results go\n\n```bash\nrm -rf /\n```\n")
        self.assertEqual(lab.parse_commands(md),
                         ["python3 -m venv .venv", ".venv/bin/python run.py --seeds 1-5"])

    def test_italian_heading_and_sh_fence(self):
        md = "## Eseguire il protocollo completo\n```sh\npython3 a.py\n```\n"
        self.assertEqual(lab.parse_commands(md), ["python3 a.py"])

    def test_no_section(self):
        self.assertEqual(lab.parse_commands("## Prerequisites\n```bash\nls\n```\n"), [])

    def test_section_without_bash_block_does_not_borrow_the_next_one(self):
        md = ("## Run the full protocol\n\n    python3 run.py\n\n"
              "## Where the results go\n```bash\ncat logs/x\n```\n")
        self.assertEqual(lab.parse_commands(md), [])

    def test_subheading_inside_the_section_is_allowed(self):
        md = "## Run the full protocol\n### Commands\n```bash\npython3 run.py\n```\n"
        self.assertEqual(lab.parse_commands(md), ["python3 run.py"])

    def test_untagged_fence_is_not_a_bash_block(self):
        md = "## Run the full protocol\n```\npython3 run.py\n```\n"
        self.assertEqual(lab.parse_commands(md), [])


if __name__ == "__main__":
    unittest.main()
