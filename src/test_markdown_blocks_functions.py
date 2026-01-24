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


if "__name__" == "__main__":
	unittest.main()