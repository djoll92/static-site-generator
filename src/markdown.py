import re
from enum import Enum
from htmlnode import ParentNode
from textnode import (TextNode, TextType, text_to_textnodes, text_node_to_html_node)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    QUOTE = "quote"
    CODE = "code"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    return re.split(r"\s*\n\s*\n\s*", markdown.strip())

def block_to_block_type(block):
    if len(re.findall(r"^#{1,6}", block)):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    if len(list(filter(lambda line: line.startswith(">"), lines))) == len(lines):
        return BlockType.QUOTE
    if len(list(filter(lambda line: line.startswith("- "), lines))) == len(lines):
        return BlockType.UNORDERED_LIST
    is_ol = True
    for i in range(len(lines)):
        if lines[i].startswith(f"{i+1}. "):
            continue
        else:
            is_ol = False
            break
    if is_ol:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    parent_node = ParentNode("div", [])
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                parent_node.children.append(ParentNode("p", text_to_inline_html(block)))
            case BlockType.QUOTE:
                parent_node.children.append(ParentNode("blockquote", text_to_inline_html(block.replace("\n>", " ").removeprefix(">").lstrip())))
            case BlockType.HEADING:
                hash_count = re.findall(r"^#{1,6}", block)[0].count("#")
                parent_node.children.append(ParentNode(f"h{hash_count}", text_to_inline_html(block.replace("#", "", hash_count).lstrip())))
            case BlockType.UNORDERED_LIST | BlockType.ORDERED_LIST:
                parent_node.children.append(list_block_to_html(block, block_type))
            case BlockType.CODE:
                parent_node.children.append(ParentNode("pre", [text_node_to_html_node(TextNode(block.removeprefix("```").removesuffix("```"), TextType.CODE))]))
    return parent_node


def text_to_inline_html(text):
    text_nodes = text_to_textnodes(re.sub(r"\s+", " ", text))
    return list(map(lambda text_node: text_node_to_html_node(text_node), text_nodes))


def list_block_to_html(block_text, block_type = BlockType.UNORDERED_LIST):
    if block_type not in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
        raise ValueError(f"Invalid list type as 2nd argument. It can only be {BlockType.UNORDERED_LIST} or {BlockType.ORDERED_LIST}")
    list_items = block_text.split("\n")
    if block_type == BlockType.ORDERED_LIST:
        list_tag = "ol"
        list_items = list(map(lambda li: re.sub(r"^\d+\. ", "", li), list_items))
    else:
        list_tag = "ul"
        list_items = list(map(lambda li: li.removeprefix("- "), list_items))
    list_node = ParentNode(list_tag, [])
    for list_item in list_items:
        list_node.children.append(ParentNode("li", text_to_inline_html(list_item)))
    return list_node


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("#") and not block.startswith("##"):
            return block.lstrip("# ")
    raise Exception("There is no h1 header in markdown.")