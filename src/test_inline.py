import unittest

from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)

from inline import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestInline(unittest.TestCase):
    def test_split_nodes(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]

        self.assertListEqual(new_nodes, expected)

    def test_split_nodes_invalid(self):
        node = TextNode("This is invalid ` markdown", text_type_text)
        self.assertRaises(
            ValueError, split_nodes_delimiter, [node], "`", text_type_code
        )

    def test_split_nodes_bold_delimiter(self):
        node = TextNode("This is **bold** text", text_type_text)
        actual = split_nodes_delimiter([node], "**", text_type_bold)

        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text),
        ]

        self.assertListEqual(actual, expected)

    def test_split_nodes_multiple_captures(self):
        node = TextNode("This is **bold** text", text_type_text)
        node_2 = TextNode(
            "Multiple **bold** pieces of text are **bolded**", text_type_text
        )

        actual = split_nodes_delimiter([node, node_2], "**", text_type_bold)

        expected = [
            TextNode("This is ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" text", text_type_text),
            TextNode("Multiple ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" pieces of text are ", text_type_text),
            TextNode("bolded", text_type_bold),
            TextNode("", text_type_text),
        ]

        self.assertListEqual(actual, expected)

    def test_split_nodes_single_non_capture(self):
        node = TextNode("Example", text_type_text)
        actual = split_nodes_delimiter([node], "`", text_type_code)

        expected = [TextNode("Example", text_type_text)]

        self.assertListEqual(actual, expected)

    def test_split_nodes_single_capture(self):
        node = TextNode("`Code`", text_type_text)
        actual = split_nodes_delimiter([node], "`", text_type_code)

        expected = [
            TextNode("", text_type_text),
            TextNode("Code", text_type_code),
            TextNode("", text_type_text),
        ]

        self.assertListEqual(actual, expected)

    def test_extract_embedded_image(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        actual = extract_markdown_images(text)

        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]

        self.assertListEqual(actual, expected)

    def test_extract_embedded_image_no_captures(self):
        text = "This has no embedded image link"
        actual = extract_markdown_images(text)

        expected = []

        self.assertListEqual(actual, expected)

    def test_extract_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        actual = extract_markdown_links(text)

        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]

        self.assertListEqual(actual, expected)

    def test_extract_link_no_captures(self):
        text = "This has no link"
        actual = extract_markdown_images(text)

        expected = []

        self.assertListEqual(actual, expected)

    def test_split_node_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        actual = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertListEqual(actual, expected)

    def test_split_node_image_in_middle(self):
        node = TextNode(
            "Text with ![image](https://www.example.com) in the middle", text_type_text
        )
        actual = split_nodes_image([node])
        expected = [
            TextNode("Text with ", text_type_text),
            TextNode("image", text_type_image, "https://www.example.com"),
            TextNode(" in the middle", text_type_text),
        ]
        self.assertListEqual(actual, expected)

    def test_split_node_link(self):
        node = TextNode(
            "Text with [link](https://www.example.com) in it", text_type_text
        )
        actual = split_nodes_link([node])
        expected = [
            TextNode("Text with ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" in it", text_type_text),
        ]
        self.assertListEqual(actual, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        actual = text_to_textnodes(text)
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "image",
                text_type_image,
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
