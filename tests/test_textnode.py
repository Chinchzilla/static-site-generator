import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        """TextNodes with the same text and TextType (and no URL) compare equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_w_url(self):
        """LINK TextNodes with matching text, type, and URL compare equal."""
        node = TextNode("Link node", TextType.LINK, "www.example.com")
        node2 = TextNode("Link node", TextType.LINK, "www.example.com")
        self.assertEqual(node, node2)

    def test_eq_w_image(self):
        """IMAGE TextNodes with matching text, type, and URL compare equal."""
        node = TextNode("Image node", TextType.IMAGE, "www.example.com/image.jpg")
        node2 = TextNode("Image node", TextType.IMAGE, "www.example.com/image.jpg")
        self.assertEqual(node, node2)

    def test_eq_w_plain(self):
        """PLAIN TextNodes with matching text and type compare equal."""
        node = TextNode("Plain node", TextType.TEXT)
        node2 = TextNode("Plain node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_neq(self):
        """TextNodes with different TextType values do not compare equal."""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_w_url(self):
        """A LINK TextNode does not equal a PLAIN TextNode even if text matches."""
        node = TextNode("Link node", TextType.LINK, "www.example.com")
        node2 = TextNode("Link node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_w_image(self):
        """An IMAGE TextNode does not equal a PLAIN TextNode even if text matches."""
        node = TextNode("Image node", TextType.IMAGE, "www.example.com/image.jpg")
        node2 = TextNode("Image node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_w_plain(self):
        """A PLAIN TextNode does not equal a BOLD TextNode even if text matches."""
        node = TextNode("Plain node", TextType.TEXT)
        node2 = TextNode("Plain node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_w_bold(self):
        """A BOLD TextNode does not equal a PLAIN TextNode even if text matches."""
        node = TextNode("Bold node", TextType.BOLD)
        node2 = TextNode("Bold node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_w_italic(self):
        """An ITALIC TextNode does not equal a PLAIN TextNode even if text matches."""
        node = TextNode("Italic node", TextType.ITALIC)
        node2 = TextNode("Italic node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_neq_w_url_and_image(self):
        """A LINK TextNode does not equal an IMAGE TextNode (different type/semantics)."""
        node = TextNode("Link node", TextType.LINK, "www.example.com")
        node2 = TextNode("Image node", TextType.IMAGE, "www.example.com/image.jpg")
        self.assertNotEqual(node, node2)


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_plain_returns_leafnode_with_no_tag(self):
        """PLAIN TextNodes should convert to a LeafNode with tag=None and the same value."""
        node: TextNode = TextNode("This is a text node", TextType.TEXT)

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.children, [])
        self.assertIsInstance(html_node.props, dict)
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold_returns_leafnode_with_b_tag(self):
        """BOLD TextNodes should convert to a LeafNode with tag='b'."""
        node: TextNode = TextNode("Bold text", TextType.BOLD)

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic_returns_leafnode_with_i_tag(self):
        """ITALIC TextNodes should convert to a LeafNode with tag='i'."""
        node = TextNode("Italic text", TextType.ITALIC)

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_code_returns_leafnode_with_code_tag(self):
        """CODE TextNodes should convert to a LeafNode with tag='code'."""
        node = TextNode("print('hi')", TextType.CODE)

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('hi')")
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.to_html(), "<code>print('hi')</code>")

    def test_link_returns_leafnode_with_a_tag_and_href_prop(self):
        """LINK TextNodes should convert to a LeafNode with tag='a' and props['href']=url."""
        node = TextNode("Example", TextType.LINK, "https://example.com")

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        self.assertEqual(html_node.children, [])
        self.assertIsInstance(html_node.props, dict)
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(
            html_node.to_html(), '<a href="https://example.com">Example</a>'
        )

    def test_link_with_no_url_sets_href_to_none(self):
        """LINK TextNodes with no url should still produce a LeafNode; href should be None."""
        node = TextNode("Example", TextType.LINK, "links/this.html")

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        self.assertEqual(html_node.children, [])
        self.assertIsInstance(html_node.props, dict)
        self.assertEqual(html_node.props, {"href": "links/this.html"})
        self.assertEqual(html_node.to_html(), '<a href="links/this.html">Example</a>')

    def test_image_returns_leafnode_with_img_tag_and_src_alt_props(self):
        """IMAGE TextNodes should convert to a LeafNode with tag='img' and src/alt props."""
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, [])
        self.assertIsInstance(html_node.props, dict)

        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, [])
        self.assertIsInstance(html_node.props, dict)
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/image.png", "alt": "Alt text"},
        )

        self.assertEqual(
            html_node.to_html(),
            '<img src="https://example.com/image.png" alt="Alt text">',
        )

    def test_image_with_no_url_sets_src_to_none_and_renders_img_html(self):
        """IMAGE TextNodes with no url should still set src=None and render img HTML."""
        node = TextNode("Alt text", TextType.IMAGE, "img/image.jpg")

        html_node = text_node_to_html_node(node)

        self.assertIsInstance(html_node, LeafNode, "img/image.jpg")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "img/image.jpg", "alt": "Alt text"})
        self.assertEqual(
            html_node.to_html(), '<img src="img/image.jpg" alt="Alt text">'
        )


if __name__ == "__main__":
    _: unittest.TestProgram = unittest.main()
