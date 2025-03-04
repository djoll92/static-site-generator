from content import remove_and_replace_dir_content, generate_pages_recursive

def main():
    remove_and_replace_dir_content("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()