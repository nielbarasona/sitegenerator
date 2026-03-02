import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_code_delimiter(self):
        nodes = [TextNode("This is `code` text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_double_delimiter(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_no_delimiter(self):
        nodes = [TextNode("This is plain text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [TextNode("This is plain text", TextType.TEXT)])

    def test_unmatched_delimiter(self):
        nodes = [TextNode("This is `code text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_multiple_delimiters(self):
        nodes = [TextNode("This is `code` and `more code`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("more code", TextType.CODE),
            ],
        )

    def test_delimiter_at_start_and_end(self):
        nodes = [TextNode("`code`", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("code", TextType.CODE),
            ],
        )

    def test_non_text_node(self):
        nodes = [TextNode("This is `code` text", TextType.BOLD)]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [TextNode("This is `code` text", TextType.BOLD)])

    def test_delimiter_bold_and_italic(self):
        nodes = [TextNode("This is **bold** and _italic_ text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_delimiter_multiword(self):
        nodes = [TextNode("This is **bold text**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold text", TextType.BOLD),
            ],
        )


class TestExtract(unittest.TestCase):
    def test_image(self):
        text = "This is an image: ![alt text](https://www.example.com/image.jpg)"
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [("alt text", "https://www.example.com/image.jpg")])

    def test_multiple_images(self):
        text = "Image 1: ![alt1](https://www.example.com/image1.jpg) Image 2: ![alt2](https://www.example.com/image2.jpg)"
        matches = extract_markdown_images(text)
        self.assertEqual(
            matches,
            [
                ("alt1", "https://www.example.com/image1.jpg"),
                ("alt2", "https://www.example.com/image2.jpg"),
            ],
        )

    def test_no_images(self):
        text = "This text has no images."
        matches = extract_markdown_images(text)
        self.assertEqual(matches, [])

    def test_link(self):
        text = "This is a link: [link text](https://www.example.com)"
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [("link text", "https://www.example.com")])

    def test_multiple_links(self):
        text = "Link 1: [link1](https://www.example.com/link1) Link 2: [link2](https://www.example.com/link2)"
        matches = extract_markdown_links(text)
        self.assertEqual(
            matches,
            [
                ("link1", "https://www.example.com/link1"),
                ("link2", "https://www.example.com/link2"),
            ],
        )

    def test_no_links(self):
        text = "this text has no links."
        matches = extract_markdown_links(text)
        self.assertEqual(matches, [])
