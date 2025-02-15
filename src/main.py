from textnode import TextNode
from textnode import TextType

def main():
    new_text_node = TextNode("This is the text node", TextType.BOLD, "https://www.boot.dev")
    print(new_text_node)

main()