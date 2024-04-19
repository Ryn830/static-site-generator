import re

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


def split_nodes_delimiter(nodes: TextNode, delimiter: str, text_type: str):
    split_nodes = []
    for node in nodes:
        if not node.text_type == text_type_text:
            split_nodes.append(node)
        else:
            substrings = node.text.split(delimiter)
            if len(substrings) % 2 == 0:
                raise ValueError("Text contains invalid markdown syntax.")
            for index, substring in enumerate(substrings):
                if index % 2 == 0:
                    split_nodes.append(TextNode(substring, text_type_text))
                else:
                    split_nodes.append(TextNode(substring, text_type))
    return split_nodes


def split_nodes_image(nodes: TextNode):
    split_nodes = []
    for node in nodes:
        captured_images = extract_markdown_images(node.text)
        if not len(captured_images):
            split_nodes.append(node)
        else:
            remaining_text = node.text
            while len(captured_images):
                image_text, image_url = captured_images.pop(0)
                link = f"![{image_text}]({image_url})"
                text = remaining_text.split(link, 1).pop(0)
                split_nodes.extend(
                    [
                        TextNode(text, text_type_text),
                        TextNode(image_text, text_type_image, image_url),
                    ]
                )
                remaining_text = remaining_text[len(text) + len(link) :]
            if len(remaining_text):
                split_nodes.append(TextNode(remaining_text, text_type_text))
    return split_nodes


def split_nodes_link(nodes: TextNode):
    split_nodes = []
    for node in nodes:
        captured_links = extract_markdown_links(node.text)
        if not len(captured_links):
            split_nodes.append(node)
        else:
            remaining_text = node.text
            while len(captured_links):
                link_text, link_url = captured_links.pop(0)
                link = f"[{link_text}]({link_url})"
                text = remaining_text.split(link, 1).pop(0)
                split_nodes.extend(
                    [
                        TextNode(text, text_type_text),
                        TextNode(link_text, text_type_link, link_url),
                    ]
                )
                remaining_text = remaining_text[len(text) + len(link) :]
            if len(remaining_text):
                split_nodes.append(TextNode(remaining_text, text_type_text))
    return split_nodes


def extract_markdown_images(text: str):
    capture_embedded_image_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(capture_embedded_image_regex, text)


def extract_markdown_links(text: str):
    capture_link_regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(capture_link_regex, text)


def text_to_textnodes(text: str):
    node = TextNode(text, text_type_text)
    and_images = split_nodes_image([node])
    and_links = split_nodes_link(and_images)
    and_code = split_nodes_delimiter(and_links, "`", text_type_code)
    and_bold = split_nodes_delimiter(and_code, "**", text_type_bold)
    all_nodes = split_nodes_delimiter(and_bold, "*", text_type_italic)
    return [node for node in all_nodes if len(node.text)]
