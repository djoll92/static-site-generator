import unittest
from markdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    extract_title,
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


class TestBlockToBlockType(unittest.TestCase):

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


class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```This is text that _should_ remain
the **same** even with inline stuff
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = "### This is h3 heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3> This is h3 heading</h3></div>",
        )

    def test_ul(self):
        md = """- one
- two
- three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>one</li><li>two</li><li>three</li></ul></div>",
        )

    def test_ol(self):
        md = """1. one
2. two
3. three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )

    def test_quote(self):
        md = """>one
>two
>three
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>one two three</blockquote></div>",
        )


class TestExtractTitle(unittest.TestCase):

    def test_valid(self):
        markdowns = ["# Heading 1", " #  Heading 1 ", "#Heading 1"]
        for markdown in markdowns:
            self.assertEqual(
                "Heading 1",
                extract_title(markdown)
            )

    def test_invalid(self):
        with self.assertRaises(Exception):
            markdown = "## Heading 1"
            extract_title(markdown)

    def test_invalid_2(self):
        with self.assertRaises(Exception):
            markdown = "Heading 1"
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()