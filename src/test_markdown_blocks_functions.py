import unittest
from markdown_blocks_functions import *


class TestMarkdownToBlocks(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)
	
	def test_markdown_to_blocks_newlines_inbetween(self):
		md = """
This is regular paragraph.



This is another paragraph.
"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is regular paragraph.",
				"This is another paragraph."
			]
		)

	def test_markdown_to_blocks_newlines_around(self):
		md = """

		
This is regular paragraph.

This is another paragraph.


"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is regular paragraph.",
				"This is another paragraph."
			]
		)


class TestBlockToBlockType(unittest.TestCase):
	def test_heading(self):
		md = "# Heading"
		self.assertEqual(BlockType.HEADING, block_to_block_type(md))

	def test_heading_edge(self):
		md = "######  Heading"
		self.assertEqual(BlockType.HEADING, block_to_block_type(md))

	def test_heading_overleveled(self):
		md = "####### Heading"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_heading_no_text(self):
		md = "####### "
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_heading_no_space(self):
		md = "#######Heading"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_code(self):
		md = "```\na = b + 1```"
		self.assertEqual(BlockType.CODE, block_to_block_type(md))

	def test_code_empty(self):
		md = "```\n```"
		self.assertEqual(BlockType.CODE, block_to_block_type(md))

	def test_code_empty_fail(self):
		md = "``````"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_code_malformed(self):
		md = "```\nThis should likely be `BlockType.PARAGRAPH` as it's malformed."
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_code_inline(self):
		md = "```Some code```"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_code_trailing_whitespaces(self):
		md = "```\n\n\nSome code\n\n```"
		self.assertEqual(BlockType.CODE, block_to_block_type(md))

	def test_quote(self):
		md = "> quote"
		self.assertEqual(BlockType.QUOTE, block_to_block_type(md))

	def test_quote_multiline(self):
		md = "> quote\n> quote"
		self.assertEqual(BlockType.QUOTE, block_to_block_type(md))

	def test_quote_multiline_no_text(self):
		md = "> quote\n> \n> quote\n> "
		self.assertEqual(BlockType.QUOTE, block_to_block_type(md))

	def test_quote_no_space(self):
		md = ">quote"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_quote_invalid_multiline(self):
		md = "> quote\nquote\n> quote"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_quote_invalid_space(self):
		md = "> quote\n > quote"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ul(self):
		md = "- li"
		self.assertEqual(BlockType.ULIST, block_to_block_type(md))

	def test_ul_multiline(self):
		md = "- li\n- li"
		self.assertEqual(BlockType.ULIST, block_to_block_type(md))

	def test_ul_multiline_no_text(self):
		md = "- li\n- \n- li\n- "
		self.assertEqual(BlockType.ULIST, block_to_block_type(md))

	def test_ul_no_space(self):
		md = "-li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ul_invalid_multiline(self):
		md = "- li\nli\n- li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ul_invalid_space(self):
		md = "- li\n - li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ol(self):
		md = "1. li"
		self.assertEqual(BlockType.OLIST, block_to_block_type(md))

	def test_ol_multiline(self):
		md = "1. li\n2. li"
		self.assertEqual(BlockType.OLIST, block_to_block_type(md))

	def test_ol_multiline_no_text(self):
		md = "1. li\n2. \n3. li\n4. "
		self.assertEqual(BlockType.OLIST, block_to_block_type(md))

	def test_ol_no_space(self):
		md = "1.li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ol_invalid_multiline(self):
		md = "1. li\nli\n2. li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ol_invalid_space(self):
		md = "1. li\n 2. li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ol_wrong_order(self):
		md = "1. li\n3. li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))

	def test_ol_wrong_format(self):
		md = "1 li\n2 li"
		self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(md))



if "__name__" == "__main__":
	unittest.main()