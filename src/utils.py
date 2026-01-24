from textnode import TextType, TextNode
from htmlnode import LeafNode
import re


def text_node_to_html_node(text_node):
	match text_node.text_type:
		case TextType.TEXT:
			return LeafNode(None, text_node.text)
		case TextType.BOLD:
			return LeafNode("b", text_node.text)
		case TextType.ITALIC:
			return LeafNode("i", text_node.text)
		case TextType.IMAGE:
			return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
		case TextType.LINK:
			return LeafNode("a", text_node.text, {"href": text_node.url})
		case TextType.CODE:
			return LeafNode("code", text_node.text)
		

def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for node in old_nodes:
		if node.text_type != TextType.TEXT:
			new_nodes.append(node)
		elif delimiter not in node.text:
			new_nodes.append(node)
		else:
			text = node.text
			delimiter_count = 0
			while delimiter in text:
				delimiter_count += 1
				current_list = text.split(delimiter, 1)
				text = current_list[-1]
				if current_list[0] == "":
					continue
				elif delimiter_count % 2 == 0:
					new_nodes.append(TextNode(current_list[0], text_type))
				else:
					new_nodes.append(TextNode(current_list[0], node.text_type))
			if delimiter_count % 2 != 0:
				raise Exception("Invalid Markdown syntax: number of opening and closing delimiters don't match.")
			if text != "":
				new_nodes.append(TextNode(text, node.text_type))
	return new_nodes


def extract_markdown_images(text):
	"""
	:param text: Raw Markdown text
	Return list of tuples.
	Each tuple should contain the alt text and the URL of any markdown images.
	"""
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
	"""
	:param text: Raw Markdown text
	Return list of tuples.
	Each tuple should contain the anchor text and the URLs of any markdown links.
	"""
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)