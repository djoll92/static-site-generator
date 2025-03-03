from content import remove_and_replace_dir_content, generate_page

def main():
    remove_and_replace_dir_content("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()