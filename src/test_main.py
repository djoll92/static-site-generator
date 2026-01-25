import unittest
from main import markdown_to_html_node

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
		expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
		self.assertEqual(
			html,
			expected
		)

	def test_codeblock(self):
		md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
		)

	def test_unordered_list(self):
		md = """
- item one
- item two
- item three
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
		)

	def test_ordered_list(self):
		md = """
1. first
2. second
3. third
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
    	)

	def test_unordered_list_with_inline(self):
		md = """
- **bold** item
- item with _italic_ and `code`
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul>"
			"<li><b>bold</b> item</li>"
			"<li>item with <i>italic</i> and <code>code</code></li>"
			"</ul></div>",
		)

	def test_single_heading(self):
		md = """
# This is a **bold** heading with _italic_
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>This is a <b>bold</b> heading with <i>italic</i></h1></div>",
		)

	def test_multiple_headings(self):
		md = """
# Heading 1

## Heading 2

###### Smallest
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div>"
			"<h1>Heading 1</h1>"
			"<h2>Heading 2</h2>"
			"<h6>Smallest</h6>"
			"</div>",
		)


if "__name__" == "__main__":
	unittest.main()