from enum import Enum
from htmlnode import LeafNode
import re
from functools import reduce

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and  self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if None == delimiter:
        return old_nodes
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError(f"Invalid Markdown syntax. Matching closing delimiter '{delimiter}' isn't found.")
            split_text = node.text.split(delimiter)
            for i in range(len(split_text)):
                if split_text[i]:
                    new_node_text_type = TextType.TEXT
                    if i % 2 != 0:
                        new_node_text_type = text_type
                    new_nodes.append(TextNode(split_text[i], new_node_text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
        else:
            text = node.text    
            for image in images:
                image_alt, image_src = image
                image_markdown = f"![{image_alt}]({image_src})"
                split_text = text.split(image_markdown, 1)
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_src))
                text = split_text[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
        else:
            text = node.text    
            for link in links:
                link_text, link_url = link
                link_markdown = f"[{link_text}]({link_url})"
                split_text = text.split(link_markdown, 1)
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], TextType.TEXT))
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
                text = split_text[1]
            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    delimiters = {'**':TextType.BOLD, "*":TextType.ITALIC, "_":TextType.ITALIC, "`":TextType.CODE}
    return split_nodes_link(
        split_nodes_image(
            reduce(lambda accumulator, delimiter: split_nodes_delimiter(accumulator, delimiter, delimiters[delimiter]), 
                    delimiters, 
                    [TextNode(text, TextType.TEXT)])
            )
        )