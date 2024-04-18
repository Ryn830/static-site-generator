from blocks import (
    block_to_block_type,
    markdown_to_blocks,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
)

from htmlnode import (
    ParentNode,
    code_block_to_html_node,
    quote_block_to_html_node,
    paragraph_block_to_html_node,
    unordered_list_block_to_html_node,
    ordered_list_block_to_html_node,
    heading_block_to_html_node,
)


def get_html_node_func(block_type: str):
    block_type_to_html_node_func = {
        f"{block_type_heading}": heading_block_to_html_node,
        f"{block_type_code}": code_block_to_html_node,
        f"{block_type_quote}": quote_block_to_html_node,
        f"{block_type_ordered_list}": ordered_list_block_to_html_node,
        f"{block_type_unordered_list}": unordered_list_block_to_html_node,
        f"{block_type_paragraph}": paragraph_block_to_html_node,
    }
    return block_type_to_html_node_func[f"{block_type}"]


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        child_nodes.append(get_html_node_func(block_type)(block))
    root = ParentNode("div", child_nodes)
    return root
