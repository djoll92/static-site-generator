from enum import Enum
from htmlnode import ParentNode
from textnode_functions import text_node_to_html_node, text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
	raw_blocks = markdown.strip().split("\n\n")
	filtered_blocks = []
	for i in range(len(raw_blocks)):
		block = raw_blocks[i].strip()
		if block != "":
			filtered_blocks.append(block)
	return filtered_blocks


def block_to_block_type(md_block):
	default_type = BlockType.PARAGRAPH
	# Heading
	if re.match(r"^#{1,6} .+", md_block):
		return BlockType.HEADING
	# Code
	if md_block.startswith("```\n") and md_block.endswith("```"):
		return BlockType.CODE
	# Quote
	if md_block.startswith(">"):
		for line in md_block.split("\n"):
			if not line.startswith(">"):
				return default_type
		return BlockType.QUOTE
	# Unordered list
	if md_block.startswith("- "):
		for line in md_block.split("\n"):
			if not line.startswith("- "):
				return default_type
		return BlockType.ULIST
	# Ordered list
	if md_block.startswith("1. "):
		count = 1
		for line in md_block.split("\n"):
			if not line.startswith(f"{count}. "):
				return default_type
			count += 1
		return BlockType.OLIST
	# Paragraph
	return default_type


def text_to_children(text):
	children = []
	textnodes = text_to_textnodes(text)
	for textnode in textnodes:
		children.append(text_node_to_html_node(textnode))
	return children
	

def block_to_html_nodes(md_block, block_type):
	if block_type == BlockType.HEADING:
		md_block = md_block.split(" ", 1)[1]
		md_block = " ".join( md_block.split("\n") )
		return text_to_children(md_block)

	if block_type == BlockType.QUOTE:
		lines = md_block.split("\n")

		def strip_quote_marker(line: str) -> str:
			if not line.startswith(">"):
				return line
			# handle "> " and ">" with no following space
			if len(line) > 1 and line[1] == " ":
				return line[2:]
			return line[1:]

		stripped_lines = list(map(strip_quote_marker, lines))
		md_block = " ".join(stripped_lines)
		return text_to_children(md_block)

	if block_type in [BlockType.ULIST, BlockType.OLIST]:
		children = []
		lines = md_block.split("\n")
		for line in lines:
			item = line.split(" ", 1)[1]
			children.append(ParentNode("li", text_to_children(item)))
		return children
	md_block = " ".join( md_block.split("\n") )
	return text_to_children(md_block)


def block_to_html_node(md_block, block_type):
	if block_type == BlockType.CODE:
		code_children = [text_node_to_html_node(TextNode(md_block.lstrip("```\n").rstrip("```"), TextType.TEXT))]
		code_node = ParentNode("code", code_children)
		return ParentNode("pre", [code_node])
	
	if block_type == BlockType.HEADING:
		tag = f"h{len(md_block.split(" ", 1)[0])}"

	if block_type == BlockType.QUOTE:
		tag = "blockquote"
	
	if block_type == BlockType.ULIST:
		tag = "ul"
	
	if block_type == BlockType.OLIST:
		tag = "ol"

	if block_type == BlockType.PARAGRAPH:
		tag = "p"

	return ParentNode(tag, block_to_html_nodes(md_block, block_type))


def extract_title(markdown):
	lines = markdown.split("\n")
	for line in lines:
		if line.startswith("# "):
			return line.lstrip("# ").strip()
	raise Exception("There is no title!")