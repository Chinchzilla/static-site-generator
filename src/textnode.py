import html
from enum import Enum
from typing import override

from htmlnode import LeafNode


class TextType(Enum):
    """
    Enum representing different types of text nodes.

    Values represent the delimeter in markdown syntax for each text type.
    """

    TEXT = None
    BOLD = "**"
    ITALIC = "_"
    CODE = "`"
    LINK = "[]()"
    IMAGE = "![]()"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: str | None = url

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        return self.text_type == other.text_type

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=html.escape(text_node.text))
        case TextType.BOLD:
            return LeafNode(tag="b", value=html.escape(text_node.text))
        case TextType.ITALIC:
            return LeafNode(tag="i", value=html.escape(text_node.text))
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("URL is required for LINK text type")
            return LeafNode(
                tag="a",
                value=html.escape(text_node.text),
                props={"href": text_node.url},
            )
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("URL is required for IMAGE text type")
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": html.escape(text_node.text)},
            )
