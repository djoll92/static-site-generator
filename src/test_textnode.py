import unittest

from textnode import TextNode, TextType
from textnode import text_node_to_html_node
from textnode import split_nodes_delimiter
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq_with_all_params(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(node, node2)
    
    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(
            "TextNode(This is a text node, text, None)", repr(node)
        )

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_text_2(self):
        text_node = TextNode("Boot dev logo image", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.boot.dev/img/bootdev-logo-full-small.webp")
        self.assertEqual(html_node.props["alt"], "Boot dev logo image")

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_bold(self):
        node = TextNode("This is a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_multiple_valid_parts(self):
        node = TextNode("This is a **bold** word as well as this **one**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word as well as this ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
            ],
            new_nodes
        )

    def test_incomplete_delimiters(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a **bold word", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_no_delimiters(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a bold word", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()