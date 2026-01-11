from collections.abc import Sequence
from typing import override

VOID_TAGS: tuple[str, ...] = ("link", "img", "br", "meta")


class HtmlNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: Sequence[HtmlNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: Sequence[HtmlNode] = children or []
        self.props: dict[str, str] = props or {}

    @override
    def __repr__(self) -> str:
        return f"HtmlNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"

    def to_html(self) -> str:
        raise NotImplementedError("Method 'to_html' is not implemented")

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value=value, children=[], props=props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode value cannot be empty")
        elif not self.tag:
            return f"{self.value}"
        elif self.tag in VOID_TAGS:
            return f"<{self.tag}{self.props_to_html()}>{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str | None,
        children: Sequence[HtmlNode] | None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag=tag, value=None, children=children or [], props=props)

    @override
    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode tag cannot be empty")
        elif not self.children:
            raise ValueError("ParentNode children cannot be empty")
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"
