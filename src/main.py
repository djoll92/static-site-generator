from textnode import TextNode
from textnode import TextType
from textnode import extract_markdown_images

def main():
    new_text_node = TextNode("This is the text node", TextType.BOLD, "https://www.boot.dev")
    print(new_text_node)

main()