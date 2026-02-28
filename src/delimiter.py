from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            node_list.append(node)
        else:
            if delimiter not in node.text:
                node_list.append(node)
            else:
                delimiter_offset = len(delimiter)
                working_string = node.text
                while delimiter in working_string:
                    if working_string.index(delimiter) != 0:
                        pre_node = TextNode(
                            working_string[: working_string.index(delimiter)],
                            TextType.TEXT,
                        )
                        working_string = working_string[
                            working_string.index(delimiter) :
                        ]
                        node_list.append(pre_node)
                    start_index = working_string.index(delimiter)
                    try:
                        end_index = working_string.index(
                            delimiter, start_index + delimiter_offset
                        )
                    except ValueError:
                        raise ValueError("Could not find closing delimiter")
                    new_node = TextNode(
                        working_string[start_index + delimiter_offset : end_index],
                        text_type,
                    )
                    node_list.append(new_node)
                    working_string = working_string[end_index + delimiter_offset :]
                if working_string:
                    post_node = TextNode(working_string, TextType.TEXT)
                    node_list.append(post_node)
    return node_list
