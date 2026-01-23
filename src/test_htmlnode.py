import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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
		expected = "HTMLNode(tag=h1, value=Hello there, children=None, props=None)"
		self.assertEqual(expected, str(node))

	def test_repr_nested(self):
		child1 = HTMLNode(tag="h1", value="Hello there")
		child2 = HTMLNode(tag="p", value="This is the first paragraph.")
		node = HTMLNode(tag="div", children=[child1, child2])
		expected = f"HTMLNode(tag=div, value=None, children=[{str(child1)}, {str(child2)}], props=None)"
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
		self.assertEqual(str(node), "LeafNode(tag=p, value=Hello, world!, props=None)")	


class TestParentNode(unittest.TestCase):
	def test_to_html_with_multiple_children(self):
		node = ParentNode(
			"p",
			[
				LeafNode("b", "Bold text"),
				LeafNode(None, "Normal text"),
				LeafNode("i", "italic text"),
				LeafNode(None, "Normal text"),
			],
		)
		expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
		self.assertEqual(node.to_html(), expected)

	def test_to_html_with_children(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

	def test_to_html_with_grandchildren(self):
		grandchild_node = LeafNode("b", "grandchild")
		child_node = ParentNode("span", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><span><b>grandchild</b></span></div>",
		)

	def test_to_html_with_grandgrandchildren(self):
		grandgrandchild_node = LeafNode("b", "grandchild")
		grandchild_node = ParentNode("span", [grandgrandchild_node])
		child_node = ParentNode("p", [grandchild_node])
		parent_node = ParentNode("div", [child_node])
		self.assertEqual(
			parent_node.to_html(),
			"<div><p><span><b>grandchild</b></span></p></div>",
		)

	def test_to_html_with_props(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node], {"class": "parent"})
		self.assertEqual(parent_node.to_html(), "<div class=\"parent\"><span>child</span></div>")

	def test_repr(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode("div", [child_node])
		expected = f"ParentNode(tag=div, value=None, children=[{str(child_node)}], props=None)"
		self.assertEqual(expected, str(parent_node))

	def test_value_error_raises_none_tag(self):
		child_node = LeafNode("span", "child")
		parent_node = ParentNode(None, [child_node])
		with self.assertRaises(ValueError):
			parent_node.to_html()

	def test_value_error_raises_none_children(self):
		parent_node = ParentNode("div", None)
		with self.assertRaises(ValueError):
			parent_node.to_html()

	def test_value_error_raises_empty_children(self):
		parent_node = ParentNode("div", [])
		with self.assertRaises(ValueError):
			parent_node.to_html()



if __name__ == "__main__":
	unittest.main()