import json
import os
import re
import unittest

from _load import ROOT, SKILLS_DIR

SKILLS = ["founder-locale", "founder-board", "founder-marketing", "founder-cfo", "founder-consumer", "founder-launch",
          "founder-pricing", "founder-offer", "founder-competitors", "founder-brand", "founder-ops", "founder-plan"]
ABOUT = ("Twelve free Claude skills that test a business before you launch it, with the local rules of your "
         "country (Malaysia first): a board applying frameworks from books by and about Hormozi, Thiel and Jobs, "
         "a marketing director, a CFO, and a consumer panel of simulated buyers. Free, MIT.")


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


EM = chr(0x2014)  # built in code so this file does not trip its own check


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".txt")) or f in ("LICENSE", ".gitignore"):
                yield os.path.join(base, f)


class Repo(unittest.TestCase):
    def test_twelve_skill_folders(self):
        found = sorted(d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))
        self.assertEqual(found, sorted(SKILLS))

    def test_frontmatter_name_and_description(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 300, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_tools_named_in_skills_exist(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for tool in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w.\-/]+\.(?:py|md))", text):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(SKILLS_DIR, s, tool))), "%s: %s" % (s, tool))

    def test_plugin_manifests(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json")) as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "founder-skill")
        self.assertEqual(plugin["description"], ABOUT)
        self.assertEqual(plugin["license"], "MIT")
        with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json")) as fh:
            market = json.load(fh)
        self.assertEqual(market["name"], "founder-skill")
        self.assertEqual(market["plugins"][0]["name"], "founder-skill")
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_readme_carries_the_reel_copy(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = " ".join(fh.read().split())
        self.assertTrue(readme.startswith("# The Founder skill: country edition"))
        for line in (
            "Twelve Claude skills that test a business before you launch it, using the rules of the country you "
            "are launching in. Malaysia first. Free, MIT, no signup, no API key, nothing to connect.",
            "This is a fork of [The Founder skill](https://github.com/Jakeschincariol/founder-skill) by Jake "
            "Schincariol",
            "applying frameworks summarised from books by and about Alex Hormozi, Peter Thiel and Steve Jobs.",
            "Paste this repo link into Claude and say `install skill`",
            "/plugin marketplace add TechStarting/founder-skill-global",
            "/plugin install founder-skill@founder-skill",
            "## Fine print",
        ):
            self.assertIn(line, readme)
        for s in SKILLS:
            self.assertIn("`skills/%s`" % s, readme)

    def test_examples_parse(self):
        for rel in ("founder-cfo/example.json", "founder-consumer/customer.example.json"):
            with open(os.path.join(SKILLS_DIR, rel), encoding="utf-8") as fh:
                json.load(fh)

    def test_no_em_dashes(self):
        for path in text_files():
            with open(path, encoding="utf-8") as fh:
                self.assertNotIn(EM, fh.read(), os.path.relpath(path, ROOT))


if __name__ == "__main__":
    unittest.main()
