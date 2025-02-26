import re
from enum import Enum

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