from content import remove_and_replace_dir_content, generate_pages_recursive
from sys import argv

def main():
    basepath = argv[1] if len(argv) > 1 else "/"
    remove_and_replace_dir_content("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()