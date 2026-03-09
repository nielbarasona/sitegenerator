from markdown_blocks import markdown_to_html_node
import os
import re


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path} ")
    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template_content)


def extract_title(markdown):
    h1_pattern = r"^#{1} ([^\n]+)"
    match = re.search(h1_pattern, markdown, re.MULTILINE)
    if match is None:
        raise ValueError("No H1 Found")
    return match.group(1)
