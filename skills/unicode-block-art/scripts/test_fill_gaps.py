"""Run with: python3 -m unittest discover -s scripts -p 'test_*.py'."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).with_name("fill_gaps.py")


class LineModesTest(unittest.TestCase):
    def run_script(self, text, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args], input=text,
                              text=True, capture_output=True, check=True).stdout

    def test_prefixes_and_default_do_not_leak_between_lines(self):
        rows = json.loads(self.run_script(
            "<org>a-中\n<inv>a-中\na-中\n<org>a-中\na-中\n", "--json"))
        for row, inverted in zip(rows, [False, True, True, False, True]):
            self.assertEqual("".join(c["glyph"] for c in row), "a-中")
            self.assertTrue(all(c["fg"] == ("hole" if inverted else "ink") for c in row))
            self.assertTrue(all(c["bg"] == ("ink" if inverted else "hole") for c in row))

    def test_ansi_colours_swap_and_rows_reset(self):
        self.assertEqual(self.run_script("<org>-\n<inv>-\n-\n"),
                         "\x1b[0;36;40m-\x1b[0m\n"
                         "\x1b[0;30;46m-\x1b[0m\n"
                         "\x1b[0;30;46m-\x1b[0m\n")

    def test_transparent_ties_and_full_blocks(self):
        rows = json.loads(self.run_script("<org>▀█\n<inv>▀█\n", "--hole", "default", "--json"))
        self.assertEqual(rows, [
            [{"glyph": "▀", "fg": "ink", "bg": "hole"},
             {"glyph": " ", "fg": "hole", "bg": "ink"}],
            [{"glyph": "▄", "fg": "ink", "bg": "hole"},
             {"glyph": " ", "fg": "ink", "bg": "hole"}],
        ])
        output = self.run_script("<org>-\n<inv>-\n", "--hole", "default")
        self.assertEqual(output, "\x1b[0;36;49m-\x1b[0m\n\x1b[0;7;36;49m-\x1b[0m\n")

    def test_only_leading_tag_is_removed_and_empty_lines_work(self):
        rows = json.loads(self.run_script("```text\n<org>\n<inv>\n\n <org>-\n```\n", "--json"))
        self.assertEqual(rows[:3], [[], [], []])
        self.assertEqual("".join(c["glyph"] for c in rows[3]), " <org>-")


if __name__ == "__main__":
    unittest.main()
