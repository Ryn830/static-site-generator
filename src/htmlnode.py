import re

from textnode import (
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    TextNode,
)
from inline import text_to_textnodes


class HTMLNode:
    def __init__(self, tag="", value="", children=[], props={}) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        prop_list = []

        for key, value in self.props.items():
            prop_list.append(f' {key}="{value}"')

        return "".join(prop_list)

    def __eq__(self, value) -> bool:
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.props == value.props
            and all(
                [
                    self_child == value_child
                    for self_child, value_child in zip(self.children, value.children)
                ]
            )
        )


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props=None) -> None:
        super().__init__(tag, value, None, props)
        if self.value is None:
            raise ValueError("LeafNodes require values.")

    def to_html(self):
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __eq__(self, value) -> bool:
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.props == value.props
        )

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: object, props=None) -> None:
        super().__init__(tag, None, children, props)
        if self.tag is None:
            raise ValueError("ParentNodes require tags.")
        if children is None or not len(children):
            raise ValueError("ParentNodes require children.")

    def to_html(self):
        nodes = "".join([node.to_html() for node in self.children])
        return f"<{self.tag}{self.props_to_html()}>{nodes}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Unrecognized text_type found on {text_node}")


def quote_block_to_html_node(block: str):
    text_nodes = text_to_textnodes("".join(re.split("\n?> ", block)))
    child_html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    html = ParentNode("blockquote", child_html_nodes)
    return html


def unordered_list_block_to_html_node(block: str):
    items = [item for item in re.split("\n?[*-] ", block) if len(item)]
    list_items = [
        ParentNode(
            "li",
            [text_node_to_html_node(node) for node in text_to_textnodes(list_item)],
        )
        for list_item in items
    ]
    html = ParentNode("ul", list_items)
    return html


def ordered_list_block_to_html_node(block: str):
    items = [item for item in re.split("\n?\d+\. ", block) if len(item)]
    list_items = [
        ParentNode(
            "li",
            [text_node_to_html_node(node) for node in text_to_textnodes(list_item)],
        )
        for list_item in items
    ]
    html = ParentNode("ol", list_items)
    return html


def code_block_to_html_node(block: str):
    text = block.lstrip("```").rstrip("```")
    text_nodes = text_to_textnodes(text)
    child_html_nodes = [
        ParentNode("code", [text_node_to_html_node(node) for node in text_nodes])
    ]
    html = ParentNode("pre", child_html_nodes)
    return html


def heading_block_to_html_node(block: str):
    heading_level = block.count("#", 0, block.index(" "))
    text = block.split(" ", 1).pop(1)
    text_nodes = text_to_textnodes(text)
    child_html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    html = ParentNode(f"h{heading_level}", child_html_nodes)
    return html


def paragraph_block_to_html_node(block: str):
    text_nodes = text_to_textnodes(block)
    child_html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    html = ParentNode("p", child_html_nodes)
    return html
