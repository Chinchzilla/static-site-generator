import unittest

from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_init(self):
        node = HtmlNode(
            tag="div", value="Hello", children=[], props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_repr(self):
        node = HtmlNode(
            tag="div", value="Hello", children=[], props={"class": "container"}
        )
        self.assertEqual(
            repr(node),
            "HtmlNode(tag='div', value='Hello', children=[], props={'class': 'container'})",
        )

    def test_props_to_html(self):
        node = HtmlNode(
            tag="div", value="Hello", children=[], props={"class": "container"}
        )
        self.assertEqual(node.props_to_html(), ' class="container"')

    def test_props_to_html_with_multiple_props(self):
        node = HtmlNode(
            tag="div",
            value="Hello",
            children=[],
            props={"class": "container", "id": "main"},
        )
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_to_html_raises_not_implemented_error(self):
        node = HtmlNode(tag="div", value="Hello", children=[], props={})
        with self.assertRaisesRegex(
            NotImplementedError, "Method 'to_html' is not implemented"
        ):
            _ = node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_empty_tag_and_value(self):
        node = LeafNode("", "")
        self.assertEqual(node.to_html(), "")

    def test_leaf_to_html_none_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaisesRegex(ValueError, "LeafNode value cannot be empty"):
            _ = node.to_html()

    def test_leaf_to_html_with_props(self):
        node = LeafNode("p", "Hello, world!", props={"class": "container"})
        self.assertEqual(node.to_html(), '<p class="container">Hello, world!</p>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_attributes(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "child2")
        child_node3 = ParentNode(
            "div", [child_node, child_node2], props={"class": "child3"}
        )
        parent_node = ParentNode("div", [child_node3], props={"class": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="parent"><div class="child3"><span>child</span><b>child2</b></div></div>',
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaisesRegex(ValueError, "ParentNode children cannot be empty"):
            _ = parent_node.to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaisesRegex(ValueError, "ParentNode tag cannot be empty"):
            _ = parent_node.to_html()

    def test_to_html_none_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaisesRegex(ValueError, "ParentNode tag cannot be empty"):
            _ = parent_node.to_html()

    def test_to_html_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaisesRegex(ValueError, "ParentNode children cannot be empty"):
            _ = parent_node.to_html()

    if __name__ == "__main__":
        _: unittest.TestProgram = unittest.main()
