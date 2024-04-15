from textnode import (
    text_type_text,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
)


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


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props=None) -> None:
        super().__init__(tag, value, None, props)
        if not self.value:
            raise ValueError("LeafNodes require values.")

    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: object, props=None) -> None:
        super().__init__(tag, None, children, props)
        if not tag:
            raise ValueError("ParentNodes require tags.")
        if not children or not len(children):
            raise ValueError("ParentNodes require children.")

    def to_html(self):
        nodes = "".join([node.to_html() for node in self.children])
        return f"<{self.tag}{self.props_to_html()}>{nodes}</{self.tag}>"


def text_node_to_html_node(text_node: str):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.value)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.value)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.value)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.value)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.value, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.value})
    raise ValueError(f"Unrecognized text_type found on {text_node}")
