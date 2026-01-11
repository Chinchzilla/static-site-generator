import re

from textnode import TextNode, TextType


def split_node_delimeter(
    old_nodes: list[TextNode], delimeter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimeter)
            if len(parts) == 1:
                new_nodes.append(node)
                continue
            if len(parts) % 2 == 0:
                raise ValueError("No matching closing delimeter found.")

            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    image_rgx = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return image_rgx.findall(text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_rgx = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")
    return link_rgx.findall(text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_images: list[tuple[str, str]] = extract_markdown_images(node.text)

        if not extracted_images:
            new_nodes.append(node)
            continue

        current_text: str = node.text
        for alt, link in extracted_images:
            image_markdown: str = f"![{alt}]({link})"
            parts: list[str] = current_text.split(image_markdown, maxsplit=1)

            if len(parts) != 2:
                raise ValueError(f"Invalid markdown image link: {image_markdown}")

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, link))

            current_text = parts[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        extracted_links: list[tuple[str, str]] = extract_markdown_links(node.text)

        if not extracted_links:
            new_nodes.append(node)
            continue

        current_text: str = node.text
        for alt, link in extracted_links:
            link_markdown: str = f"[{alt}]({link})"
            parts: list[str] = current_text.split(link_markdown, maxsplit=1)

            if len(parts) != 2:
                raise ValueError(f"Invalid markdown link: {link_markdown}")

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.LINK, link))

            current_text = parts[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]

    for type in TextType:
        match type:
            case TextType.BOLD:
                nodes = split_node_delimeter(nodes, type.value, type)
            case TextType.ITALIC:
                nodes = split_node_delimeter(nodes, type.value, type)
            case TextType.CODE:
                nodes = split_node_delimeter(nodes, type.value, type)
            case TextType.LINK:
                nodes = split_nodes_link(nodes)
            case TextType.IMAGE:
                nodes = split_nodes_image(nodes)
            case _:
                continue

    return nodes
