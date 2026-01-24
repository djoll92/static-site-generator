import unittest
from textnode import TextNode, TextType
from utils import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestTextNodeToHTMLNode(unittest.TestCase):
	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("This is a bold node", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "This is a bold node")

	def test_italic(self):
		node = TextNode("This is an italic node", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "This is an italic node")

	def test_image(self):
		node = TextNode("This is an image node", TextType.IMAGE, "url/of/image.jpg")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "img")
		self.assertEqual(html_node.value, "")
		self.assertEqual(html_node.props["src"], "url/of/image.jpg")
		self.assertEqual(html_node.props["alt"], "This is an image node")

	def test_link(self):
		node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "This is a link node")
		self.assertEqual(html_node.props["href"], "https://www.google.com")

	def test_code(self):
		node = TextNode("This is a code node", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "This is a code node")


class TestSplitNodesDelimiter(unittest.TestCase):
	def test_single_occurrence(self):
		node = TextNode("hello **world** friend", TextType.TEXT)
		actual = split_nodes_delimiter([node], "**", TextType.BOLD)
		expected = [
			TextNode("hello ", TextType.TEXT),
			TextNode("world", TextType.BOLD),
			TextNode(" friend", TextType.TEXT)
		]
		self.assertEqual(actual, expected)

	def test_multiple_occurrences(self):
		node = TextNode("This is **very** cool **indeed**!", TextType.TEXT)
		actual = split_nodes_delimiter([node], "**", TextType.BOLD)
		expected = [
			TextNode("This is ", TextType.TEXT),
			TextNode("very", TextType.BOLD),
			TextNode(" cool ", TextType.TEXT),
			TextNode("indeed", TextType.BOLD),
			TextNode("!", TextType.TEXT),
		]
		self.assertEqual(actual, expected)

	def test_multiple_nodes(self):
		node1 = TextNode("**bold** text", TextType.TEXT)
		node2 = TextNode("Just plain text", TextType.TEXT)
		node3 = TextNode("text **bold**", TextType.TEXT)
		node4 = TextNode("very", TextType.BOLD)
		actual = split_nodes_delimiter([node1, node2, node3, node4], "**", TextType.BOLD)
		expected = [
			TextNode("bold", TextType.BOLD),
			TextNode(" text", TextType.TEXT),
			TextNode("Just plain text", TextType.TEXT),
			TextNode("text ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode("very", TextType.BOLD),
		]
		self.assertEqual(actual, expected)
		  
	def test_unmatched_delimiter_raises(self):
		with self.assertRaises(Exception):
			split_nodes_delimiter([TextNode("This is **broken", TextType.TEXT)], "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

	def test_extract_markdown_images_empty(self):
		matches = extract_markdown_images(
			"This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([], matches)

	def test_extract_markdown_images_multiple(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another one ![second image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("second image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
	def test_extract_markdown_links(self):
		matches = extract_markdown_links(
			"This is a text with a [link](google.com)"
		)
		self.assertListEqual([("link", "google.com")], matches)

	def test_extract_markdown_links_empty(self):
		matches = extract_markdown_links(
			"This is a text with a ![link](google.com)"
		)
		self.assertListEqual([], matches)

	def test_extract_markdown_links_multiple(self):
		matches = extract_markdown_links(
			"This is a text with a [link](google.com) and [another link](https://duckduckgo.com/)"
		)
		self.assertListEqual([("link", "google.com"), ("another link", "https://duckduckgo.com/")], matches)



if "__name__" == "__main__":
	unittest.main()