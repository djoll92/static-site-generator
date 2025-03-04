import os
import shutil
from pathlib import Path
from markdown import markdown_to_html_node, extract_title

def remove_and_replace_dir_content(from_path, dest_path):
    clean_or_make_dir(dest_path)
    if os.path.exists(from_path) and os.path.isdir(from_path) and os.path.exists(dest_path) and os.path.isdir(dest_path):
        static_items = os.listdir(from_path)
        for item in static_items:
            src_path = os.path.join(from_path, item)
            dst_path = os.path.join(dest_path, item)
            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
                print(f"Copying {src_path} to {dst_path}...")
            else:
                remove_and_replace_dir_content(src_path, dst_path)   


def clean_or_make_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    if os.path.exists(from_path) and os.path.isfile(from_path):
        with open(from_path) as md_file:
            markdown = md_file.read()
    if os.path.exists(template_path) and os.path.isfile(template_path):
        with open(template_path) as template:
            template_content = template.read()
    if markdown and template_content:
        title = extract_title(markdown)
        content = markdown_to_html_node(markdown).to_html()
        page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", content).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")
        dest_path_dir = os.path.dirname(dest_path)
        if dest_path_dir:
            os.makedirs(dest_path_dir, exist_ok=True)
        with open(dest_path, "w") as page_file:
            page_file.write(page_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if os.path.exists(dir_path_content) and os.path.isdir(dir_path_content):
        content_items = os.listdir(dir_path_content)
        for item in content_items:
            src_path = os.path.join(dir_path_content, item)
            dest_path = os.path.join(dest_dir_path, item)
            if os.path.isfile(src_path) and item.endswith(".md"):
                generate_page(src_path, template_path, dest_path.removesuffix("md") + "html", basepath)
            elif os.path.isdir(src_path):
                generate_pages_recursive(src_path, template_path, dest_path, basepath)