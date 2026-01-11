import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_multiple_paragraphs(self):
        md = """
Paragraph one.

Paragraph two.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph one.", "Paragraph two."])

    def test_leading_trailing_newlines(self):
        md = """

Paragraph with leading and trailing newlines.

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph with leading and trailing newlines."])

    def test_multiple_empty_lines_between_blocks(self):
        md = """
Block one.


Block two.


Block three.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block one.", "Block two.", "Block three."])

    def test_mixed_content_with_lists(self):
        md = """
This is a paragraph.

- List item one
- List item two

Another paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "- List item one\n- List item two",
                "Another paragraph.",
            ],
        )

    def test_code_block(self):
        md = """
This is a paragraph.

```
This is a code block.
It can have multiple lines.
```

End paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "```\nThis is a code block.\nIt can have multiple lines.\n```",
                "End paragraph.",
            ],
        )

    def test_headings(self):
        md = """
# Heading One

## Heading Two

This is a paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks, ["# Heading One", "## Heading Two", "This is a paragraph."]
        )

    def test_blockquotes(self):
        md = """
> This is a blockquote.
> It can span multiple lines.

Normal paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "> This is a blockquote.\n> It can span multiple lines.",
                "Normal paragraph.",
            ],
        )

    def test_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        heading1 = "# Heading One"
        self.assertEqual(block_to_block_type(heading1), BlockType.HEADING)
        heading2 = "## Heading Two"
        self.assertEqual(block_to_block_type(heading2), BlockType.HEADING)
        heading3 = "### Heading Three"
        self.assertEqual(block_to_block_type(heading3), BlockType.HEADING)
        heading4 = "#### Heading Four"
        self.assertEqual(block_to_block_type(heading4), BlockType.HEADING)
        heading5 = "##### Heading Five"
        self.assertEqual(block_to_block_type(heading5), BlockType.HEADING)
        heading6 = "###### Heading Six"
        self.assertEqual(block_to_block_type(heading6), BlockType.HEADING)
        invalid_heading = "#Heading One"
        self.assertEqual(block_to_block_type(invalid_heading), BlockType.PARAGRAPH)
        invalid_heading2 = "########## heading two"
        self.assertEqual(block_to_block_type(invalid_heading2), BlockType.PARAGRAPH)

    def test_blockquote(self):
        blockquote = "> This is a blockquote."
        self.assertEqual(block_to_block_type(blockquote), BlockType.QUOTE)
        multiline_blockquote = "> This is a blockquote.\n> This is a blockquote."
        self.assertEqual(block_to_block_type(multiline_blockquote), BlockType.QUOTE)
        invalid_blockquote = ">This is a blockquote."
        self.assertEqual(block_to_block_type(invalid_blockquote), BlockType.QUOTE)

    def test_code_block(self):
        code_block = "```\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        code_block2 = "```\nprint('Hello, World!')\n"
        self.assertEqual(block_to_block_type(code_block2), BlockType.PARAGRAPH)
        code_block3 = "```\nprint('Hello, World!')\n"
        self.assertEqual(block_to_block_type(code_block3), BlockType.PARAGRAPH)
        code_block4 = "```\nprint('Hello, World!')\n"
        self.assertEqual(block_to_block_type(code_block4), BlockType.PARAGRAPH)

    def test_paragraph(self):
        paragraph = "This is a paragraph."
        self.assertEqual(block_to_block_type(paragraph), BlockType.PARAGRAPH)
        multiline_paragraph = "This is a paragraph.\nThis is a paragraph."
        self.assertEqual(block_to_block_type(multiline_paragraph), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        list_block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(list_block), BlockType.UNORDERED_LIST)
        invalid_list_block = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(invalid_list_block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        list_block = "1. Item 1\n2. Item 2"
        self.assertEqual(block_to_block_type(list_block), BlockType.ORDERED_LIST)
        invalid_list_block = "1.Item 1\n2.Item 2"
        self.assertEqual(block_to_block_type(invalid_list_block), BlockType.PARAGRAPH)
        long_list_block = "1. Item 1\n2. Item 2\n3. Item 3\n4. Item 4\n5. Item 5"
        self.assertEqual(block_to_block_type(long_list_block), BlockType.ORDERED_LIST)
        long_invalid_list_block = (
            "1. Item 1\n2. Item 2\n4. Item 3\n8. Item 4\n5. Item 5"
        )
        self.assertEqual(
            block_to_block_type(long_invalid_list_block), BlockType.PARAGRAPH
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_simple_paragraph(self):
        markdown = "This is a paragraph.\nThere is nothing special about this paragraph, no formatting."
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><p>This is a paragraph. There is nothing special about this paragraph, no formatting.</p></div>",
        )

    def test_paragraph_with_formatting(self):
        markdown = (
            "This paragraph has **bold** and _italic_ text.\nAnd also some `code`."
        )
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><p>This paragraph has <b>bold</b> and <i>italic</i> text. And also some <code>code</code>.</p></div>",
        )

    def test_heading(self):
        h1 = "# Heading"
        node = markdown_to_html(markdown=h1)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><h1>Heading</h1></div>",
        )
        h2 = "## Subheading"
        node = markdown_to_html(markdown=h2)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><h2>Subheading</h2></div>",
        )
        h3 = "### Subsubheading"
        node = markdown_to_html(markdown=h3)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><h3>Subsubheading</h3></div>",
        )
        h4 = "#### Subsubsubheading"
        node = markdown_to_html(markdown=h4)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><h4>Subsubsubheading</h4></div>",
        )
        h5 = "##### Subsubsubsubheading"
        node = markdown_to_html(markdown=h5)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><h5>Subsubsubsubheading</h5></div>",
        )
        h6 = "###### Subsubsubsubsubheading"
        node = markdown_to_html(markdown=h6)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><h6>Subsubsubsubsubheading</h6></div>",
        )

    def test_block_quote(self):
        markdown = "> This is a block quote."
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><blockquote>This is a block quote.</blockquote></div>",
        )

    def test_block_quote_with_multiple_lines(self):
        markdown = "> This is a block quote.\n> It spans multiple lines."
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><blockquote>This is a block quote. It spans multiple lines.</blockquote></div>",
        )

    def test_block_quote_with_multiple_lines_and_author(self):
        markdown = """> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            '<div><blockquote>"I am in fact a Hobbit in all but size." -- J.R.R. Tolkien</blockquote></div>',
        )

    def test_code_block(self):
        markdown = """```
def my_function():
    pass
```"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><pre><code>\ndef my_function():\n    pass\n</code></pre></div>",
        )

    def test_code_block_doesnt_mess_with_formatting(self):
        markdown = """```
# This **text** should _remain_ unchanged. `No` exceptions!
```
"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><pre><code>\n# This **text** should _remain_ unchanged. `No` exceptions!\n</code></pre></div>",
        )

    def test_unordered_list(self):
        markdown = """- Item 1
- Item 2
- Item 3"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>",
        )

    def test_ordered_list(self):
        markdown = """1. Item 1
2. Item 2
3. Item 3"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>",
        )

    def test_image(self):
        markdown = """![Image](image.jpg)"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            '<div><p><img src="image.jpg" alt="Image"></p></div>',
        )

    def test_link(self):
        markdown = """[link](https://example.com)"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        self.assertEqual(
            node_html,
            '<div><p><a href="https://example.com">link</a></p></div>',
        )

    def test_all(self):
        self.maxDiff: int | None = None
        markdown = """# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien

```
def my_function():
    pass # This comment has **formatting** and `backticks` and _italics_
```

- Item 1
- Item 2
- Item 3

1. Item 1
2. Item 2
3. Item 3

![Image](image.jpg)
[link](https://example.com)

This paragraph should be **properly** _formatted_. Including `code`.
"""
        node = markdown_to_html(markdown=markdown)
        node_html = node.to_html()
        expected_html = (
            "<div><h1>Heading 1</h1>"
            "<h2>Heading 2</h2>"
            "<h3>Heading 3</h3>"
            "<h4>Heading 4</h4>"
            "<h5>Heading 5</h5>"
            "<h6>Heading 6</h6>"
            '<blockquote>"I am in fact a Hobbit in all but size." -- J.R.R. Tolkien</blockquote>'
            "<pre><code>\ndef my_function():\n    pass # This comment has **formatting** and `backticks` and _italics_\n</code></pre>"
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
            "<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>"
            '<p><img src="image.jpg" alt="Image"> '
            '<a href="https://example.com">link</a></p>'
            "<p>This paragraph should be <b>properly</b> <i>formatted</i>. Including <code>code</code>.</p></div>"
        )
        self.assertEqual(node_html, expected_html)


if __name__ == "__main__":
    _: unittest.TestProgram = unittest.main()
