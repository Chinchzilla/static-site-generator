import re
from enum import Enum

from helpers import rgx_extract_match
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_text_nodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = None
    HEADING = "#"
    CODE = "`"
    QUOTE = ">"
    UNORDERED_LIST = "-"
    ORDERED_LIST = "."


def markdown_to_blocks(markdown: str) -> list[str]:
    """Converts a markdown string to a list of TextNodes."""
    blocks: list[str] = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]


def block_to_block_type(block: str) -> BlockType:
    block = block.strip()
    lines = block.split("\n")

    if isinstance(re.match(rf"^{BlockType.HEADING.value}{{1,6}}\s", block), re.Match):
        return BlockType.HEADING
    elif block.startswith(3 * BlockType.CODE.value) and block.endswith(
        3 * BlockType.CODE.value
    ):
        return BlockType.CODE
    elif all([b.strip().startswith(BlockType.QUOTE.value) for b in lines]):
        return BlockType.QUOTE
    elif all(
        [b.strip().startswith(BlockType.UNORDERED_LIST.value + " ") for b in lines]
    ):
        return BlockType.UNORDERED_LIST
    elif isinstance(
        re.match(rf"^\d+\{BlockType.ORDERED_LIST.value}\s", block), re.Match
    ):
        increment: int = 1
        for line in lines:
            if not line.startswith(f"{increment}{BlockType.ORDERED_LIST.value} "):
                break
            if increment < len(lines):
                increment += 1

        if increment == len(lines):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(block: str) -> list[LeafNode]:
    text: str = block.replace("\n", " ")
    return [text_node_to_html_node(text_node) for text_node in text_to_text_nodes(text)]


def block_to_html_node(block: str) -> ParentNode:
    block_type: BlockType = block_to_block_type(block)
    match block_type:
        case BlockType.HEADING:
            heading: str | None = rgx_extract_match(
                regex=rf"^{BlockType.HEADING.value}{{1,6}}\s", text=block
            )
            if heading is not None:
                heading = heading.strip()
                return ParentNode(
                    tag=f"h{len(heading)}",
                    children=text_to_children(block.replace(heading, "").strip()),
                )
        case BlockType.CODE:
            code_block_delimeter: str = BlockType.CODE.value * 3
            pure_code_block: str = (
                block.strip().lstrip(code_block_delimeter).rstrip(code_block_delimeter)
            )
            return ParentNode(
                tag="pre", children=[LeafNode(tag="code", value=pure_code_block)]
            )
        case BlockType.QUOTE:
            quote_lines: list[str] = []
            for line in block.split("\n"):
                line = line.lstrip(">").strip()
                if line:
                    quote_lines.append(line)
            return ParentNode(
                tag="blockquote",
                children=text_to_children(" ".join(quote_lines)),
            )
        case BlockType.UNORDERED_LIST:
            unordered_list_items: list[str] = [
                line.strip().lstrip("-").strip() for line in block.split("\n")
            ]
            return ParentNode(
                tag="ul",
                children=[
                    ParentNode(tag="li", children=text_to_children(item))
                    for item in unordered_list_items
                ],
            )
        case BlockType.ORDERED_LIST:
            ordered_list_items: list[str] = [
                re.sub(r"^\d+\.\s", "", line.strip()) for line in block.split("\n")
            ]
            return ParentNode(
                tag="ol",
                children=[
                    ParentNode(tag="li", children=text_to_children(item))
                    for item in ordered_list_items
                ],
            )
        case BlockType.PARAGRAPH:
            return ParentNode(tag="p", children=text_to_children(block))

    return ParentNode(tag="p", children=text_to_children(block))


def markdown_to_html(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    children: list[ParentNode] = [block_to_html_node(block) for block in blocks]
    return ParentNode(tag="div", children=children)
