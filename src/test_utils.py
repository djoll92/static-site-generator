import unittest
from textnode import TextNode, TextType
from utils import *
import pprint


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


class TestSplitNodesImage(unittest.TestCase):
	def test_split_images(self):
		node = TextNode(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		expected = [
			TextNode("This is text with an ", TextType.TEXT),
			TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			TextNode(" and another ", TextType.TEXT),
			TextNode(
				"second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
			),
		]
		self.assertListEqual(expected, new_nodes)

	def test_split_image_begin(self):
		node = TextNode(
			"![image](https://i.imgur.com/zjjcJKZ.png) this text is after the image.",
			TextType.TEXT,
		)
		expected = [
			TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
			TextNode(" this text is after the image.", TextType.TEXT)
		]
		actual = split_nodes_image([node])
		self.assertListEqual(expected, actual)

	def test_split_image_end(self):
		node = TextNode(
			"This text ends with an image ![image](https://i.imgur.com/zjjcJKZ.png)",
			TextType.TEXT,
		)
		expected = [
			TextNode("This text ends with an image ", TextType.TEXT),
			TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
		]
		actual = split_nodes_image([node])
		self.assertListEqual(expected, actual)

	def test_split_image_only(self):
		node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
		expected = [TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
		actual = split_nodes_image([node])
		self.assertListEqual(expected, actual)

	def test_split_image_side_by_side(self):
		node = TextNode("![img1](url1)![img2](url2) Some text.", TextType.TEXT)
		expected = [
			TextNode("img1", TextType.IMAGE, "url1"),
			TextNode("img2", TextType.IMAGE, "url2"),
			TextNode(" Some text.", TextType.TEXT)
		]
		actual = split_nodes_image([node])
		self.assertListEqual(expected, actual)


class TestSplitNodesLink(unittest.TestCase):
	def test_split_links(self):
		node = TextNode(
			"This is text with a [link](https://google.com) and another [second link](https://duckduckgo.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		expected = [
			TextNode("This is text with a ", TextType.TEXT),
			TextNode("link", TextType.LINK, "https://google.com"),
			TextNode(" and another ", TextType.TEXT),
			TextNode(
				"second link", TextType.LINK, "https://duckduckgo.com"
			),
		]
		self.assertListEqual(expected, new_nodes)

	def test_split_link_begin(self):
		node = TextNode(
			"[anchor text](https://google.com) this text is after the anchor.",
			TextType.TEXT,
		)
		expected = [
			TextNode("anchor text", TextType.LINK, "https://google.com"),
			TextNode(" this text is after the anchor.", TextType.TEXT)
		]
		actual = split_nodes_link([node])
		self.assertListEqual(expected, actual)

	def test_split_link_end(self):
		node = TextNode(
			"This text ands with a link [anchor text](https://google.com)",
			TextType.TEXT,
		)
		expected = [
			TextNode("This text ands with a link ", TextType.TEXT),
			TextNode("anchor text", TextType.LINK, "https://google.com")
		]
		actual = split_nodes_link([node])
		self.assertListEqual(expected, actual)

	def test_split_link_only(self):
		node = TextNode("[anchor text](https://google.com)", TextType.TEXT)
		expected = [TextNode("anchor text", TextType.LINK, "https://google.com")]
		actual = split_nodes_link([node])
		self.assertListEqual(expected, actual)


class TestSplitURLNodesDelimiter(unittest.TestCase):
	text_types = [TextType.IMAGE, TextType.LINK]
	def test_split_node_without_image(self):
		node = TextNode("This is a text node", TextType.TEXT)
		for text_type in self.text_types:
			self.assertListEqual([node], split_url_nodes_delimiter([node], text_type))

	def test_split_node_with_bold(self):
		node = TextNode("This is a bold node", TextType.BOLD)
		for text_type in self.text_types:
			self.assertListEqual([node], split_url_nodes_delimiter([node], text_type))


if "__name__" == "__main__":
	unittest.main()