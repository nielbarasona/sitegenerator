from markdown_blocks import markdown_to_html_node
import os
import re


def generate_page(from_path, template_path, dest_path, basepath):
    print(f" * {from_path} {template_path} -> {dest_path} ")
    with open(from_path, "r") as file:
        markdown_content = file.read()
    with open(template_path, "r") as file:
        template_content = file.read()
    html_string = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_string)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    list_dir = os.listdir(dir_path_content)
    for file in list_dir:
        source_full_path = os.path.join(dir_path_content, file)
        html_filename = os.path.join(dest_dir_path, f"{file[:-3]}.html")
        dest_full_path = os.path.join(dest_dir_path, file)
        print(f" * {source_full_path} -> {dest_full_path}")
        if os.path.isfile(source_full_path):
            generate_page(source_full_path, template_path, html_filename, basepath)
        else:
            generate_pages_recursive(
                source_full_path, template_path, dest_full_path, basepath
            )


def extract_title(markdown):
    h1_pattern = r"^#{1} ([^\n]+)"
    match = re.search(h1_pattern, markdown, re.MULTILINE)
    if match is None:
        raise ValueError("No H1 Found")
    return match.group(1)
