import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_eq_2(self):
		node = TextNode("This is a text node", TextType.TEXT, None)
		node2 = TextNode("This is a text node", TextType.TEXT)
		self.assertEqual(node, node2)
  
	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.TEXT)
		node2 = TextNode("This is a text nod", TextType.TEXT)
		self.assertNotEqual(node, node2)
  
	def test_invalid_text_type_raises(self):
		with self.assertRaises(TypeError):
			TextNode("This is text node", "text")


if __name__ == "__main__":
	unittest.main()