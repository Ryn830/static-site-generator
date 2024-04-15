import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


if __name__ == "__main__":
    unittest.main()
