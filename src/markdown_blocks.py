from enum import Enum
from htmlnode import ParentNode
import re

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processed_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped == "":
            continue
        processed_blocks.append(stripped)
    return processed_blocks


def block_to_block_type(block):
    heading_pattern = r"#{1,6} "
    if re.match(heading_pattern, block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST

    is_ordered = True
    for i, line in enumerate(lines):
        if not line.startswith(f"{i + 1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.HEADING:
                counter = 0
                while block[counter] == "#":
                    counter += 1
                content = block[counter:].strip()
                children = text_to_children(content)
                heading_node = ParentNode(f"h{counter}", children)
                nodes.append(heading_node)
            case BlockType.CODE:
                if not block.startswith("```") or not block.endswith("```"):
                    raise ValueError("invalid code block")
                content = block[4:-3]
                text_node = TextNode(content, TextType.TEXT)
                content_leaf = text_node_to_html_node(text_node)
                code_parent = ParentNode("code", [content_leaf])
                pre_parent = ParentNode("pre", [code_parent])
                nodes.append(pre_parent)
            case BlockType.QUOTE:
                lines = block.split("\n")
                new_lines = []
                for line in lines:
                    new_lines.append(line[1:].strip())
                rejoined = " ".join(new_lines)
                children = text_to_children(rejoined)
                quote_node = ParentNode("blockquote", children)
                nodes.append(quote_node)
            case BlockType.ULIST:
                lines = block.split("\n")
                children = []
                for line in lines:
                    stripped = line[2:].strip()
                    children.append(ParentNode("li", text_to_children(stripped)))
                ulist_node = ParentNode("ul", children)
                nodes.append(ulist_node)
            case BlockType.OLIST:
                lines = block.split("\n")
                children = []
                for line in lines:
                    stripped = line.split(". ", 1)[1].strip()
                    children.append(ParentNode("li", text_to_children(stripped)))
                olist_node = ParentNode("ol", children)
                nodes.append(olist_node)
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                rejoined = " ".join(lines)
                children = text_to_children(rejoined)
                paragraph_node = ParentNode("p", children)
                nodes.append(paragraph_node)
    parent_node = ParentNode("div", nodes)
    return parent_node


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    nodes = []
    for node in textnodes:
        nodes.append(text_node_to_html_node(node))
    return nodes
