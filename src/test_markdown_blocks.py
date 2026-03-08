import unittest

from markdown_blocks import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
    markdown_to_html_node,
)


class TestTextNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    # Headings
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### My Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Deep Heading"), BlockType.HEADING)

    def test_heading_no_space_fails(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    def test_heading_seven_hashes_fails(self):
        self.assertEqual(block_to_block_type("####### Too Many"), BlockType.PARAGRAPH)

    # Code
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_code_multiline(self):
        self.assertEqual(block_to_block_type("```\nline1\nline2\n```"), BlockType.CODE)

    def test_code_no_newline_after_ticks_fails(self):
        self.assertEqual(block_to_block_type("```some code```"), BlockType.PARAGRAPH)

    # Quote
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">some quote"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> some quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type(">line1\n>line2"), BlockType.QUOTE)

    def test_quote_missing_marker_fails(self):
        self.assertEqual(block_to_block_type(">line1\nline2"), BlockType.PARAGRAPH)

    # Unordered list
    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.ULIST)

    def test_unordered_list_multi(self):
        self.assertEqual(
            block_to_block_type("- item1\n- item2\n- item3"), BlockType.ULIST
        )

    def test_unordered_list_missing_space_fails(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    # Ordered list
    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.OLIST)

    def test_ordered_list_multi(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"), BlockType.OLIST
        )

    def test_ordered_list_wrong_start_fails(self):
        self.assertEqual(block_to_block_type("2. item"), BlockType.PARAGRAPH)

    def test_ordered_list_skipped_number_fails(self):
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)

    # Paragraph
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just some text."), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(
            block_to_block_type("Line one.\nLine two."), BlockType.PARAGRAPH
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_invalid_codeblock(self):
        md = """
```
this is a heading with too many levels
"""
        with self.assertRaises(ValueError):
            markdown_to_html_node(md)


if __name__ == "__main__":
    unittest.main()
