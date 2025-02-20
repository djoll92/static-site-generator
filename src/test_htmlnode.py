import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_empty(self):
        node1 = HTMLNode()
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(repr(node1), repr(node2))

    def test_repr(self):
        node = HTMLNode("a", "link text", None, {"href":"https://www.google.com","target":"_blank"})
        self.assertEqual(
            "HTMLNode(a, link text, children: None, {'href': 'https://www.google.com', 'target': '_blank'})",
            repr(node)
        )

    def test_values(self):
        node = HTMLNode("p", "paragraph text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "paragraph text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)        

    def test_to_html(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode()
            node.to_html()


class TestLeafNode(unittest.TestCase):

    def test_props_to_html(self):
        node = LeafNode("a", "click me", {"href": "https://www.google.com","target": "_blank"})
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_empty(self):
        with self.assertRaises(ValueError):
            node = LeafNode("a", None)
            node.to_html()

    def test_repr(self):
        node = LeafNode("a", "link text", {"href":"https://www.google.com","target":"_blank"})
        self.assertEqual(
            "LeafNode(a, link text, {'href': 'https://www.google.com', 'target': '_blank'})",
            repr(node)
        )

    def test_values(self):
        node = LeafNode("p", "paragraph text")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "paragraph text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)    

    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())    

    def test_to_html_2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', node.to_html())    

    def test_to_html_2(self):
        node = LeafNode(None, "I have no tag!")
        self.assertEqual('I have no tag!', node.to_html())    


class TestParentNode(unittest.TestCase):
    multiple_leaves_children = [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ]

    def test_props_to_html(self):
        node = ParentNode("div", [LeafNode("p", "paragraph text")], {"class": "text-wrapper"})
        self.assertEqual(
            ' class="text-wrapper"', node.props_to_html()
        )

    def test_empty(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()

    def test_repr(self):
        node = ParentNode("div", [LeafNode("p", "paragraph text")], {"class": "text-wrapper"})
        self.assertEqual(
            "ParentNode(div, children: [LeafNode(p, paragraph text, None)], {'class': 'text-wrapper'})",
            repr(node)
        )

    def test_multiple_leaves_children(self):
        node = ParentNode("p", self.multiple_leaves_children)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, self.multiple_leaves_children)
        self.assertEqual(node.props, None)    

    def test_to_html_multiple_leaves_children(self):
        node = ParentNode("p", self.multiple_leaves_children)
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", node.to_html())    

    def test_to_html_nested_parent(self):
        node = ParentNode("div", [ParentNode("p", self.multiple_leaves_children)])
        self.assertEqual('<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>', node.to_html())


if __name__ == "__main__":
    unittest.main()