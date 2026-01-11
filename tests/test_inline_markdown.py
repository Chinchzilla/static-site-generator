import unittest
from typing import override

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_node_delimeter,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)
from textnode import TextNode, TextType


class TestSplitTextNode(unittest.TestCase):
    def test_split_text_node_with_delimeter(self):
        """SplitTextNode should split TextNodes with a delimeter."""
        node = TextNode("Hello, **bold** World!", TextType.TEXT, "!")
        new_nodes = split_node_delimeter([node], "**", TextType.BOLD)

        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Hello, ")
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[2].text, " World!")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_text_node_with_no_delimeter_raises_value_error(self):
        """SplitTextNode should raise a ValueError if no matching closing delimeter is found."""
        node = TextNode("Hello, **World*", TextType.TEXT, "**")
        with self.assertRaises(ValueError):
            _ = split_node_delimeter([node], "**", TextType.IMAGE)

    def test_split_node_multiple_delimiters_no_nesting(self):
        """SplitTextNode should correctly split a TextNode with multiple, non-nested delimiters."""
        node = TextNode("This is `code` and *italic* and **bold** text.", TextType.TEXT)

        # Split for bold
        nodes_after_bold: list[TextNode] = split_node_delimeter(
            [node], "**", TextType.BOLD
        )
        self.assertEqual(len(nodes_after_bold), 3)
        self.assertEqual(nodes_after_bold[0].text, "This is `code` and *italic* and ")
        self.assertEqual(nodes_after_bold[0].text_type, TextType.TEXT)
        self.assertEqual(nodes_after_bold[1].text, "bold")
        self.assertEqual(nodes_after_bold[1].text_type, TextType.BOLD)
        self.assertEqual(nodes_after_bold[2].text, " text.")
        self.assertEqual(nodes_after_bold[2].text_type, TextType.TEXT)

        # Split for italic on the result of bold split
        nodes_after_italic: list[TextNode] = []
        for n in nodes_after_bold:
            nodes_after_italic.extend(split_node_delimeter([n], "*", TextType.ITALIC))

        self.assertEqual(len(nodes_after_italic), 5)
        self.assertEqual(nodes_after_italic[0].text, "This is `code` and ")
        self.assertEqual(nodes_after_italic[0].text_type, TextType.TEXT)
        self.assertEqual(nodes_after_italic[1].text, "italic")
        self.assertEqual(nodes_after_italic[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes_after_italic[2].text, " and ")
        self.assertEqual(nodes_after_italic[2].text_type, TextType.TEXT)
        self.assertEqual(nodes_after_italic[3].text, "bold")  # This was already bold
        self.assertEqual(nodes_after_italic[3].text_type, TextType.BOLD)
        self.assertEqual(nodes_after_italic[4].text, " text.")
        self.assertEqual(nodes_after_italic[4].text_type, TextType.TEXT)

        # Split for code on the result of italic split
        final_nodes: list[TextNode] = []
        for n in nodes_after_italic:
            final_nodes.extend(split_node_delimeter([n], "`", TextType.CODE))

        self.assertEqual(len(final_nodes), 7)
        self.assertEqual(final_nodes[0].text, "This is ")
        self.assertEqual(final_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[1].text, "code")
        self.assertEqual(final_nodes[1].text_type, TextType.CODE)
        self.assertEqual(final_nodes[2].text, " and ")
        self.assertEqual(final_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[3].text, "italic")
        self.assertEqual(final_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(final_nodes[4].text, " and ")
        self.assertEqual(final_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(final_nodes[5].text, "bold")
        self.assertEqual(final_nodes[5].text_type, TextType.BOLD)
        self.assertEqual(final_nodes[6].text, " text.")
        self.assertEqual(final_nodes[6].text_type, TextType.TEXT)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )


class TestSplitNodesImage(unittest.TestCase):
    @override
    def setUp(self):
        self.maxDiff: int | None = None

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_at_beginning(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) text after image", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" text after image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode(
            "text before image ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("text before image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_only_image(self):
        node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        node1 = TextNode("No image here", TextType.TEXT)
        node2 = TextNode("Image here: ![img1](url1)", TextType.TEXT)
        node3 = TextNode("Another ![img2](url2) image", TextType.TEXT)

        new_nodes = split_nodes_image([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("No image here", TextType.TEXT),
                TextNode("Image here: ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("Another ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode(" image", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_three_images(self):
        node = TextNode(
            "Text with ![img1](url1) then ![img2](url2) and finally ![img3](url3) at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" then ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode(" and finally ", TextType.TEXT),
                TextNode("img3", TextType.IMAGE, "url3"),
                TextNode(" at the end.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_four_images(self):
        node = TextNode(
            "![img1](url1) ![img2](url2) ![img3](url3) ![img4](url4)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode(" ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "url2"),
                TextNode(" ", TextType.TEXT),
                TextNode("img3", TextType.IMAGE, "url3"),
                TextNode(" ", TextType.TEXT),
                TextNode("img4", TextType.IMAGE, "url4"),
            ],
            new_nodes,
        )

    def test_split_images_with_links_present(self):
        node = TextNode(
            "Text with ![image](img_url) and [link](url) then ![image2](img_url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "img_url"),
                TextNode(" and [link](url) then ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "img_url2"),
            ],
            new_nodes,
        )


class TestSplitNodesLink(unittest.TestCase):
    @override
    def setUp(self):
        self.maxDiff: int | None = None

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [second link](https://example.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_links_no_link(self):
        node = TextNode("This is just plain text.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_at_beginning(self):
        node = TextNode("[link](https://example.com) text after link", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" text after link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_at_end(self):
        node = TextNode("text before link [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("text before link ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_only_link(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_split_links_multiple_nodes(self):
        node1 = TextNode("No link here", TextType.TEXT)
        node2 = TextNode("Link here: [link1](url1)", TextType.TEXT)
        node3 = TextNode("Another [link2](url2) link", TextType.TEXT)

        new_nodes = split_nodes_link([node1, node2, node3])
        self.assertListEqual(
            [
                TextNode("No link here", TextType.TEXT),
                TextNode("Link here: ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode("Another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" link", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_links_with_images_present(self):
        node = TextNode("Text with [link](url) and ![image](img_url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" and ![image](img_url)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_three_links(self):
        node = TextNode(
            "Text with [link1](url1) then [link2](url2) and finally [link3](url3) at the end.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" then ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" and finally ", TextType.TEXT),
                TextNode("link3", TextType.LINK, "url3"),
                TextNode(" at the end.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_four_links(self):
        node = TextNode(
            "[link1](url1) [link2](url2) [link3](url3) [link4](url4)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" ", TextType.TEXT),
                TextNode("link3", TextType.LINK, "url3"),
                TextNode(" ", TextType.TEXT),
                TextNode("link4", TextType.LINK, "url4"),
            ],
            new_nodes,
        )

    def test_split_links_with_images_and_links_mixed(self):
        node = TextNode(
            "Text with ![image1](img_url1) and [link1](url1) then ![image2](img_url2) and [link2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text with ![image1](img_url1) and ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" then ![image2](img_url2) and ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
            ],
            new_nodes,
        )


class TestTextToTextNodes(unittest.TestCase):
    @override
    def setUp(self):
        self.maxDiff: int | None = None

    def test_split_text_with_bold(self):
        node = TextNode(
            "Text with **bold** and **bold** again",
            TextType.TEXT,
        )
        new_nodes = text_to_text_nodes(node.text)
        self.assertListEqual(
            [
                TextNode("Text with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" again", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_text_nodes_full_markdown(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_empty_string(self):
        text = ""
        expected_nodes = [TextNode("", TextType.TEXT)]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_plain_text(self):
        text = "This is just plain text with no markdown."
        expected_nodes = [
            TextNode("This is just plain text with no markdown.", TextType.TEXT)
        ]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_only_bold(self):
        text = "**bold**"
        expected_nodes = [TextNode("bold", TextType.BOLD)]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_only_italic(self):
        text = "_italic_"
        expected_nodes = [TextNode("italic", TextType.ITALIC)]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_only_code(self):
        text = "`code`"
        expected_nodes = [TextNode("code", TextType.CODE)]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_only_image(self):
        text = "![alt](url)"
        expected_nodes = [TextNode("alt", TextType.IMAGE, "url")]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_only_link(self):
        text = "[link](url)"
        expected_nodes = [TextNode("link", TextType.LINK, "url")]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_bold_and_italic(self):
        text = "This is **bold** and _italic_."
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_bold_and_code(self):
        text = "This has **bold** and `code`."
        expected_nodes = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_nested_markdown_unsupported(self):
        text = "**_nested_**"
        expected_nodes = [
            TextNode(
                "_nested_", TextType.BOLD
            ),  # Delimiter splitting is not truly nested
        ]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_multiple_of_each(self):
        text = "**bold1** _italic1_ `code1` ![img1](url1) [link1](url1) **bold2** _italic2_ `code2` ![img2](url2) [link2](url2)"
        expected_nodes = [
            TextNode("bold1", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic1", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code1", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic2", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code2", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_markdown_at_edges(self):
        text = "**start** text _middle_ text `end`"
        expected_nodes = [
            TextNode("start", TextType.BOLD),
            TextNode(" text ", TextType.TEXT),
            TextNode("middle", TextType.ITALIC),
            TextNode(" text ", TextType.TEXT),
            TextNode("end", TextType.CODE),
        ]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))

    def test_text_to_text_nodes_no_markdown_at_all(self):
        text = "This is a simple sentence."
        expected_nodes = [TextNode("This is a simple sentence.", TextType.TEXT)]
        self.assertListEqual(expected_nodes, text_to_text_nodes(text))


if __name__ == "__main__":
    _: unittest.TestProgram = unittest.main()
