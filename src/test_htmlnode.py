import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
	def test_props_to_html(self):
		props = {
			"href": "https://www.google.com",
			"target": "_blank",
		}
		node = HTMLNode(props=props)
		expected = ' href="https://www.google.com" target="_blank"'
		actual = node.props_to_html()
		self.assertEqual(expected, actual)

	def test_props_to_html_single_prop(self):
		props = {"href": "https://www.google.com"}
		node = HTMLNode(props=props)
		expected = ' href="https://www.google.com"'
		actual = node.props_to_html()
		self.assertEqual(expected, actual)

	def test_props_to_html_empty_dict(self):
		node = HTMLNode(props={})
		self.assertEqual("", node.props_to_html())
	
	def test_props_to_html_none(self):
		node = HTMLNode()
		self.assertEqual("", node.props_to_html())

	def test_repr_simple(self):
		node = HTMLNode(tag="h1", value="Hello there")
		expected = "HTMLNode(h1, Hello there, None, None)"
		self.assertEqual(expected, str(node))

	def test_repr_nested(self):
		child1 = HTMLNode(tag="h1", value="Hello there")
		child2 = HTMLNode(tag="p", value="This is the first paragraph.")
		node = HTMLNode(tag="div", children=[child1, child2])
		expected = f"HTMLNode(div, None, [{str(child1)}, {str(child2)}], None)"
		self.assertEqual(expected, str(node))


class TestLeafNode(unittest.TestCase):
	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")		

	def test_leaf_to_html_a(self):
		node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
		self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

	def test_leaf_to_html_none_tag(self):
		node = LeafNode(None, "Hello there")
		self.assertEqual(node.to_html(), "Hello there")

	def test_repr(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(str(node), "LeafNode(p, Hello, world!, None)")	

if __name__ == "__main__":
	unittest.main()