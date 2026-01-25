from textnode import TextNode, TextType
from htmlnode import ParentNode
from markdown_blocks_functions import markdown_to_blocks, block_to_block_type, block_to_html_node, extract_title
import os
import shutil


def main():
	copy_contents("static", "public")
	generate_page("content/index.md", "template.html", "public/index.html")


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
			print(f"Copying file from {src_path} to {dst_path}")
			shutil.copyfile(src_path, dst_path)
		else:
			copy_contents(src_path, dst_path)


def generate_page(from_path, template_path, dest_path):
	from_path = os.path.abspath(from_path)
	template_path = os.path.abspath(template_path)
	dest_path = os.path.abspath(dest_path)

	print(f"Generating page from {from_path} to {dest_path} using {template_path}")

	if not os.path.exists(from_path) or not os.path.isfile(from_path):
		raise FileNotFoundError(f"Markdown file does not exist on this path: {from_path}")
	
	if not os.path.exists(template_path):
		raise FileNotFoundError(f"Template file does not exist on this path: {template_path}")
	
	if os.path.isdir(dest_path):
		raise Exception(f'Cannot write to "{dest_path}" as it is a directory')
	
	try:
		file = open(from_path)
		markdown = file.read()
		file.close()
	except Exception as err:
		print(f"Cannote read from file {from_path}" - {err})

	try:
		file = open(template_path)
		template = file.read()
		file.close()
	except Exception as err:
		print(f"Cannote read from file {template_path}" - {err})

	content = markdown_to_html_node(markdown).to_html()
	title = extract_title(markdown)

	html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

	try:
		os.makedirs(os.path.dirname(dest_path), exist_ok=True)

		with open(dest_path, "w") as file:
			file.write(html)
	except Exception as err:
		print(f"Cannot write to file {dest_path} - {err}")


if __name__ == "__main__":
    main()