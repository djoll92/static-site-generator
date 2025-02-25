import unittest

from textnode import (
        TextNode,
        TextType,
        text_node_to_html_node,
        split_nodes_delimiter,
        extract_markdown_links,
        extract_markdown_images,
        split_nodes_image,
        split_nodes_link,
        text_to_textnodes
    )
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
        node = TextNode("This is text with a code block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a code block word", TextType.TEXT)
            ],
            new_nodes
        )

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


class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_image(self):
        text = "![alt text](image.jpg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [("alt text", "image.jpg")]
        )

    def test_multiple_image(self):
        text = "![img1](url1.jpg) some text ![img2](url2.jpg)"
        self.assertListEqual(
            extract_markdown_images(text),
            [("img1", "url1.jpg"), ("img2", "url2.jpg")]
        )

    def test_with_no_images(self):
        text = "Just plain text"
        self.assertListEqual(
            extract_markdown_images(text),
            []
        )

    def test_with_regular_links(self):
        text = "[not an image](not-image.jpg)"
        self.assertListEqual(
            extract_markdown_images(text),
            []
        )


class TestExtractMarkdownLinks(unittest.TestCase):

    def test_single_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev")]
        )

    def test_multiple_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertListEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_with_no_links(self):
        text = "Just plain text"
        self.assertListEqual(
            extract_markdown_links(text),
            []
        )

    def test_with_image(self):
        text = "![alt text](image.jpg)"
        self.assertListEqual(
            extract_markdown_links(text),
            []
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_only_image(self):
        node = TextNode("![boot dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("boot dev logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
            ],
            new_nodes
        )

    def test_single_image(self):
        node = TextNode("This is text with an image ![boot dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) in the middle!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("boot dev logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
                TextNode(" in the middle!", TextType.TEXT),
            ],
            new_nodes
        )

    def test_multiple_valid_images(self):
        node = TextNode("This is text with an image ![boot dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) and ![sorcerer avatar](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/7W7Koad.png)",
                        TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("boot dev logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
                TextNode(" and ", TextType.TEXT),
                TextNode("sorcerer avatar", TextType.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/7W7Koad.png"),
            ],
            new_nodes
        )

    def test_no_images(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev)", TextType.TEXT),
            ],
            new_nodes
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_only_link(self):
        node = TextNode("[to boot dev](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )

    def test_single_link(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) in the middle!", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" in the middle!", TextType.TEXT),
            ],
            new_nodes
        )

    def test_multiple_valid_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                        TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes
        )

    def test_no_links(self):
        node = TextNode("![boot dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("![boot dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp)", TextType.TEXT)
            ],
            new_nodes
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_multiple_valid_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            textnodes
        )

    def test_only_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
            textnodes
        )
    
    def test_single_image(self):
        text = "This is text with an image ![boot dev logo](https://www.boot.dev/img/bootdev-logo-full-small.webp) in the middle!"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("boot dev logo", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-small.webp"),
                TextNode(" in the middle!", TextType.TEXT),
            ],
            textnodes
        )

    def test_incomplete_delimiters(self):
        with self.assertRaises(ValueError):
            text = "This is a **bold word"
            text_to_textnodes(text)

    def test_no_delimiters(self):
        text = "This is text with a code block word"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a code block word", TextType.TEXT)
            ],
            textnodes
        )

    def test_delim_bold_and_italic(self):
        text = "**bold** and *italic*"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            textnodes,
        )


if __name__ == "__main__":
    unittest.main()