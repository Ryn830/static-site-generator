import unittest

from htmlnode import ParentNode, LeafNode

from markdown import markdown_to_html_node


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_html_node(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        actual = markdown_to_html_node(markdown)
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is ", None),
                        LeafNode("b", "bolded", None),
                        LeafNode(None, " paragraph", None),
                    ],
                    None,
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "This is another paragraph with ", None),
                        LeafNode("i", "italic", None),
                        LeafNode(None, " text and ", None),
                        LeafNode("code", "code", None),
                        LeafNode(
                            None,
                            " here\nThis is the same paragraph on a new line",
                            None,
                        ),
                    ],
                    None,
                ),
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li", [LeafNode(None, "This is a list", None)], None
                        ),
                        ParentNode("li", [LeafNode(None, "with items", None)], None),
                    ],
                    None,
                ),
            ],
            None,
        )
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
