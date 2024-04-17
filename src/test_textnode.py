import unittest

from textnode import (
    TextNode,
    text_type_bold,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        node_2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")

        self.assertEqual(node, node_2)


if __name__ == "__main__":
    unittest.main()
