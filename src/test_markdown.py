import unittest
from markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType
)

class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_text(self):
        markdown = "Block 1\n\nBlock 2\n\nBlock 3"
        self.assertListEqual(
            ["Block 1", "Block 2", "Block 3"],
            markdown_to_blocks(markdown)
        )

    def test_extra_newlines(self):
        markdown = "Block 1\n\n\nBlock 2\n\n\nBlock 3"
        self.assertListEqual(
            ["Block 1", "Block 2", "Block 3"],
            markdown_to_blocks(markdown)
        )

    def test_spaces_and_tabs_between_blocks(self):
        markdown = "Block 1\n \n\t\nBlock 2"
        self.assertListEqual(
            ["Block 1", "Block 2"],
            markdown_to_blocks(markdown)
        )

    def test_whitespaces_at_edges(self):
        markdown = "\n\nBlock 1\n\nBlock 2\n\n"
        self.assertListEqual(
            ["Block 1", "Block 2"],
            markdown_to_blocks(markdown)
        )


class TestBlcokToBlockType(unittest.TestCase):

    def test_heading(self):
        markdown = "##### Heading 5"
        self.assertEqual(
            BlockType.HEADING,
            block_to_block_type(markdown)
        )

    def test_paragraph(self):
        markdown = "This is a paragraph of text."
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(markdown)
        )

    def test_code(self):
        markdown = "```This is code```"
        self.assertEqual(
            BlockType.CODE,
            block_to_block_type(markdown)
        )

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type(markdown)
        )

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2\3. Item 3"
        self.assertEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type(markdown)
        )

    def test_faulty_ol(self):
        markdown = "1. Item 1\n2. Item 2\n4. Item 3"
        self.assertEqual(
            BlockType.PARAGRAPH,
            block_to_block_type(markdown)
        )


if __name__ == "__main__":
    unittest.main()