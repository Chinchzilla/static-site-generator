import unittest

from gen_content import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# Title\n\nContent"
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_from_middle(self):
        markdown = "Content\n\n# Title\n\nMore content"
        self.assertEqual(extract_title(markdown), "Title")

    def test_extract_title_with_no_title(self):
        markdown = "Content"
        self.assertRaisesRegex(ValueError, "No title found", extract_title, markdown)

    def test_empty_string(self):
        markdown = ""
        self.assertRaisesRegex(ValueError, "No title found", extract_title, markdown)


if __name__ == "__main__":
    _: unittest.TestProgram = unittest.main()
