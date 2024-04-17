import unittest

from blocks import (
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    block_type_paragraph,
    is_heading_block,
    is_code_block,
    is_quote_block,
    is_unordered_list_block,
    is_ordered_list_block,
    block_to_block_type,
    markdown_to_blocks,
)


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        actual = markdown_to_blocks(markdown)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertListEqual(actual, expected)

    def test_markdown_to_blocks_removes_empty_lines(self):
        markdown = """This markdown should produce a single block.


"""
        actual = markdown_to_blocks(markdown)
        expected = ["This markdown should produce a single block."]
        self.assertListEqual(actual, expected)

    def test_is_heading_block(self):
        mocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        for mock in mocks:
            self.assertTrue(is_heading_block(mock))

    def test_is_heading_block_invalid(self):
        mocks = ["#Not Heading", "Text", ">Quote", "*bold*"]
        for mock in mocks:
            self.assertFalse(is_heading_block(mock))

    def test_is_code_block(self):
        mock = """```
import pdb
pbd.set_trace()
```"""
        self.assertTrue(is_code_block(mock))

    def test_is_code_block_invalid(self):
        mocks = ["#Not Heading", "Text", ">Quote", "*bold*"]
        for mock in mocks:
            self.assertFalse(is_code_block(mock))

    def test_is_quote_block(self):
        mock = ">This is a valid quote\n>So is this one"
        self.assertTrue(is_quote_block(mock))

    def test_is_quote_block_invalid(self):
        mocks = ["#Not Heading", "Text", "*bold*"]
        for mock in mocks:
            self.assertFalse(is_quote_block(mock))

    def test_is_unordered_list_block(self):
        mocks = [
            "* list item 1\n* list item 2\n* list item 3",
            "- item 1\n- item 2\n- item 3",
            "* list item 1\n- list item 2\n* list 3",
        ]
        for mock in mocks:
            self.assertTrue(is_unordered_list_block(mock))

    def test_is_unordered_list_block_invalid(self):
        mocks = ["#Not Heading", "Text", ">Quote", "*bold*"]
        for mock in mocks:
            self.assertFalse(is_unordered_list_block(mock))

    def test_is_ordered_list_block(self):
        mock = "1. first\n2. second\n3. third"
        self.assertTrue(is_ordered_list_block(mock))

    def test_is_unordered_list_block_invalid(self):
        mocks = ["#Not Heading", "Text", ">Quote", "*bold*"]
        for mock in mocks:
            self.assertFalse(is_ordered_list_block(mock))

    def tests_block_to_block_type(self):
        mocks = [
            ("# Heading", block_type_heading),
            ("```print('something')```", block_type_code),
            (">Quote", block_type_quote),
            ("* item 1\n* item 2\n* item 3", block_type_unordered_list),
            ("1. item\n2. item 2\n3. item 3", block_type_ordered_list),
            ("paragraph text", block_type_paragraph),
        ]
        for mock, type in mocks:
            self.assertEqual(block_to_block_type(mock), type)


if __name__ == "__main__":
    unittest.main()
