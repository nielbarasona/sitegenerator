from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        working_string = old_node.text
        images = extract_markdown_images(working_string)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        for image in images:
            image_alt, image_url = image
            sections = working_string.split(f"![{image_alt}]({image_url})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            working_string = sections[1]
        if working_string != "":
            split_nodes.append(TextNode(working_string, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        working_string = old_node.text
        links = extract_markdown_links(working_string)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        for link in links:
            link_text, link_url = link
            sections = working_string.split(f"[{link_text}]({link_url})", 1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            working_string = sections[1]
        if working_string != "":
            split_nodes.append(TextNode(working_string, TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\]]+)\]\(([^)]+)\)"
    matches = re.findall(pattern, text)
    return matches


def text_to_textnodes(text):
    original_node = [TextNode(text, TextType.TEXT)]
    bolded = split_nodes_delimiter(original_node, "**", TextType.BOLD)
    italics = split_nodes_delimiter(bolded, "_", TextType.ITALIC)
    code = split_nodes_delimiter(italics, "`", TextType.CODE)
    links = split_nodes_link(code)
    images = split_nodes_image(links)
    return images
