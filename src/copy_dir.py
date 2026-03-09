import os
import shutil


def copy_contents(source_dir, dest_dir):
    dest_dir_abs = os.path.abspath(dest_dir)
    if os.path.exists(dest_dir_abs):
        shutil.rmtree(dest_dir_abs)
    os.mkdir(dest_dir_abs)
    list_dir = os.listdir(source_dir)
    for file in list_dir:
        source_full_path = os.path.join(source_dir, file)
        dest_full_path = os.path.join(dest_dir, file)
        if os.path.isfile(source_full_path):
            shutil.copy(source_full_path, dest_full_path)
            print(f"copied {source_full_path} to {dest_full_path}")
        else:
            copy_contents(source_full_path, dest_full_path)
