import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
    quote_block_to_html_node,
    code_block_to_html_node,
    heading_block_to_html_node,
    paragraph_block_to_html_node,
    ordered_list_block_to_html_node,
    unordered_list_block_to_html_node,
)


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        html_node = HTMLNode(
            "a", "text", [], {"href": "https://www.boot.dev", "target": "_blank"}
        )
        html_props = html_node.props_to_html()
        self.assertEqual(html_props, ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html_single(self):
        html_node = HTMLNode("a", "text", [], {"href": "https://www.boot.dev"})
        html_props = html_node.props_to_html()
        self.assertEqual(html_props, ' href="https://www.boot.dev"')


class TestLeafNode(unittest.TestCase):
    def test_raise_when_no_value(self):
        self.assertRaises(ValueError, LeafNode, "p", None)

    def test_leaf_node_to_html(self):
        leaf_node = LeafNode("p", "some text", {"class": "paragraph"})
        self.assertEqual(leaf_node.to_html(), '<p class="paragraph">some text</p>')


class TestParentNode(unittest.TestCase):
    def test_raise_when_no_tag(self):
        leaf_nodes = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        self.assertRaises(ValueError, ParentNode, None, leaf_nodes)

    def test_raise_when_no_children(self):
        no_children_nodes = None
        self.assertRaises(ValueError, ParentNode, "div", no_children_nodes)

        empty_children_nodes = []
        self.assertRaises(ValueError, ParentNode, "div", empty_children_nodes)

    def test_parent_node_to_html(self):
        children_nodes = [
            LeafNode("b", "Bold text"),
        ]
        parent_node = ParentNode("div", children_nodes)
        self.assertEqual(parent_node.to_html(), "<div><b>Bold text</b></div>")

    def test_nested_parent_nodes(self):
        children_nodes = [
            ParentNode("div", [LeafNode("b", "Bold text", {"class": "bold"})])
        ]
        parent_node = ParentNode("section", children_nodes)
        self.assertEqual(
            parent_node.to_html(),
            '<section><div><b class="bold">Bold text</b></div></section>',
        )

    def test_nested_three_levels(self):
        children_nodes = [
            ParentNode("div", [ParentNode("div", [LeafNode("p", "paragraph")])])
        ]
        parent_node = ParentNode("section", children_nodes)
        self.assertEqual(
            parent_node.to_html(),
            "<section><div><div><p>paragraph</p></div></div></section>",
        )

    def test_two_parents_in_children(self):
        children_nodes = [
            ParentNode("div", [LeafNode("b", "child 1")]),
            ParentNode("div", [LeafNode("b", "child 2")]),
        ]
        parent_node = ParentNode("section", children_nodes)
        self.assertEqual(
            parent_node.to_html(),
            "<section><div><b>child 1</b></div><div><b>child 2</b></div></section>",
        )

    def test_create_quote_html_node(self):
        block = ">example quote\n>another line\n>and another"
        actual = quote_block_to_html_node(block)
        expected = ParentNode("blockquote", [LeafNode(None, block)])
        self.assertEqual(actual, expected)

    def test_code_block_to_html_node(self):
        block = "```print('something')```"
        actual = code_block_to_html_node(block)
        expected = ParentNode(
            "pre", [ParentNode("code", [LeafNode(None, "print('something')")])]
        )
        self.assertEqual(actual, expected)

    def test_heading_block_to_html_node(self):
        blocks = [
            ("# Heading 1", ParentNode("h1", [LeafNode(None, "Heading 1")])),
            ("## Heading 2", ParentNode("h2", [LeafNode(None, "Heading 2")])),
            ("### Heading 3", ParentNode("h3", [LeafNode(None, "Heading 3")])),
            ("#### Heading 4", ParentNode("h4", [LeafNode(None, "Heading 4")])),
            ("##### Heading 5", ParentNode("h5", [LeafNode(None, "Heading 5")])),
            ("###### Heading 6", ParentNode("h6", [LeafNode(None, "Heading 6")])),
        ]
        for block, expected in blocks:
            actual = heading_block_to_html_node(block)
            self.assertEqual(actual, expected)

    def test_paragraph_block_to_html_node(self):
        block = "Test paragraph"
        actual = paragraph_block_to_html_node(block)
        expected = ParentNode("p", [LeafNode(None, block)])
        self.assertEqual(actual, expected)

    def test_ordered_list_block_to_html_node(self):
        block = "1. first item\n2. second item\n3. third item"
        actual = ordered_list_block_to_html_node(block)
        expected = ParentNode(
            "ol",
            [
                ParentNode("li", [LeafNode(None, "first item")]),
                ParentNode("li", [LeafNode(None, "second item")]),
                ParentNode("li", [LeafNode(None, "third item")]),
            ],
        )
        self.assertEqual(actual, expected)

    def test_unordered_list_block_to_html_node(self):
        block = "* first item\n- second item\n* third item"
        actual = unordered_list_block_to_html_node(block)
        expected = ParentNode(
            "ul",
            [
                ParentNode("li", [LeafNode(None, "first item")]),
                ParentNode("li", [LeafNode(None, "second item")]),
                ParentNode("li", [LeafNode(None, "third item")]),
            ],
        )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
