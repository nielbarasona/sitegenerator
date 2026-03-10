import os
import shutil
from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
from sys import argv

dir_path_static = "./static"
dir_path_dest = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    if argv[1]:
        basepath = argv[1]
    else:
        basepath = "/"

    print("Deleting public dicrectory...")
    if os.path.exists(dir_path_dest):
        shutil.rmtree(dir_path_dest)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_dest)

    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_dest, basepath)


if __name__ == "__main__":
    main()
