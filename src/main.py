from textnode import TextNode, TextType
from htmlnode import ParentNode
from markdown_blocks_functions import markdown_to_blocks, block_to_block_type, block_to_html_node
import os
import shutil


def main():
	copy_contents("static", "public")


def markdown_to_html_node(markdown):
	blocks = markdown_to_blocks(markdown)
	children_nodes = []
	for block in blocks:
		block_type = block_to_block_type(block)
		html_node = block_to_html_node(block, block_type)
		children_nodes.append(html_node)
	parent_node = ParentNode("div", children_nodes)
	return parent_node


# Copies all the contents from the destination directory to source directory
# It should delete all the contents from the destination dir
# If the destination dir doesn't exist it should create it
def copy_contents(src, dst):
	src = os.path.abspath(src)
	dst = os.path.abspath(dst)
	if not os.path.exists(src):
		raise FileNotFoundError(f"Source directory does not exist: {src}")
	if os.path.exists(dst):
		try:
			shutil.rmtree(dst)
		except Exception as err:
			print(f"Cannot delete {dst} - {err}")
	try:
		os.mkdir(dst)
	except Exception as err:
		print(f"Cannot create {dst} - {err}")

	for path in os.listdir(src):
		src_path = os.path.join(src, path)
		dst_path = os.path.join(dst, path)
		if os.path.isfile(src_path):
			shutil.copyfile(src_path, dst_path)
		else:
			copy_contents(src_path, dst_path)


if __name__ == "__main__":
    main()