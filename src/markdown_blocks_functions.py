from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
	raw_blocks = markdown.split("\n\n")
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
	if md_block.startswith("> "):
		for line in md_block.split("\n"):
			if not line.startswith("> "):
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