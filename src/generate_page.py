from os import path, makedirs

from blocks import is_heading_block

from markdown import markdown_to_html_node, markdown_to_blocks

TITLE_PLACEHOLDER = "{{ Title }}"
CONTENT_PLACEHOLDER = "{{ Content }}"


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    template = open(template_path).read()
    markdown = open(from_path).read()

    title = extract_title(markdown)
    markdown_html = markdown_to_html_node(markdown).to_html()

    template_with_title = template.replace(TITLE_PLACEHOLDER, title)

    template_with_markdown = template_with_title.replace(
        CONTENT_PLACEHOLDER, markdown_html
    )

    dir = path.dirname(dest_path)
    if not path.exists(dir):
        makedirs(dir)
    with open(path.join(dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(template_with_markdown)


def extract_title(markdown: str):
    blocks = markdown_to_blocks(markdown)
    heading = [block for block in blocks if is_heading_block(block)]
    try:
        return heading.pop(0).lstrip("# ")
    except:
        raise ValueError(f"Page require a heading: {markdown}")
