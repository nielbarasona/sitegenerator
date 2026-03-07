import unittest

from markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type


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


if __name__ == "__main__":
    unittest.main()
