import os
import shutil

def remove_and_replace_dir_content(content_src_dir="./static", dst_dir="./public"):
    clean_or_make_dir(dst_dir)
    copy_dir_content(content_src_dir, dst_dir)


def copy_dir_content(src_dir, dst_dir):
    
    if os.path.exists(src_dir) and os.path.isdir(src_dir) and os.path.exists(dst_dir) and os.path.isdir(dst_dir):
        static_items = os.listdir(src_dir)
        for item in static_items:
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join(dst_dir, item)
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copying {src_path} to {dst_path}...")
            else:
                remove_and_replace_dir_content(src_path, dst_path)


def clean_or_make_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)