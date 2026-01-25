from textnode import TextNode, TextType
from htmlnode import ParentNode
from markdown_blocks_functions import markdown_to_blocks, block_to_block_type, block_to_html_node


def main():
	print(TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev"))

def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children_nodes = []
	for block in blocks:
		block_type = block_to_block_type(block)
		html_node = block_to_html_node(block, block_type)
		children_nodes.append(html_node)
	parent_node = ParentNode("div", children_nodes)
	return parent_node

if __name__ == "__main__":
    main()