# tests/test_stargazer.py
import unittest

from stargazer import parse_repo_url, format_stars


class TestParseRepoUrl(unittest.TestCase):
    def test_full_url(self):
        self.assertEqual(parse_repo_url("https://github.com/anthropics/claude-code"), ("anthropics", "claude-code"))

    def test_full_url_trailing_slash(self):
        self.assertEqual(parse_repo_url("https://github.com/anthropics/claude-code/"), ("anthropics", "claude-code"))

    def test_slug(self):
        self.assertEqual(parse_repo_url("anthropics/claude-code"), ("anthropics", "claude-code"))

    def test_invalid_url(self):
        with self.assertRaises(SystemExit):
            parse_repo_url("not-a-repo")

    def test_http_url(self):
        self.assertEqual(parse_repo_url("http://github.com/anthropics/claude-code"), ("anthropics", "claude-code"))


class TestFormatStars(unittest.TestCase):
    def test_small(self):
        self.assertEqual(format_stars(500), "500")

    def test_thousands(self):
        self.assertEqual(format_stars(12345), "12.3k")

    def test_exact_thousand(self):
        self.assertEqual(format_stars(1000), "1.0k")

    def test_zero(self):
        self.assertEqual(format_stars(0), "0")


if __name__ == "__main__":
    unittest.main()
