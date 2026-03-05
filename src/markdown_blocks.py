def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    processed_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped == "":
            continue
        processed_blocks.append(stripped)
    return processed_blocks
