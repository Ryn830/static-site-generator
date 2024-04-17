block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(markdown: str):
    return list(
        filter(
            # Reject empty strings
            lambda s: len(s) > 1,
            # Remove whitespace
            [block.strip() for block in markdown.split("\n\n")],
        )
    )


def block_to_block_type(block: str):
    if is_heading_block(block):
        return block_type_heading
    if is_code_block(block):
        return block_type_code
    if is_quote_block(block):
        return block_type_quote
    if is_unordered_list_block(block):
        return block_type_unordered_list
    if is_ordered_list_block(block):
        return block_type_ordered_list
    return block_type_paragraph


def is_heading_block(block: str):
    return block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### "))


def is_code_block(block: str):
    return block.startswith("```") and block.endswith("```")


def is_quote_block(block: str):
    return all(line.startswith(">") for line in block.split("\n"))


def is_unordered_list_block(block: str):
    return all(line.startswith(("* ", "- ")) for line in block.split("\n"))


def is_ordered_list_block(block: str):
    numbers = [line.split(". ").pop(0) for line in block.split("\n")]
    return (
        numbers[0] == "1"
        and all(num.isdigit() for num in numbers)
        and sorted(numbers) == numbers
    )
