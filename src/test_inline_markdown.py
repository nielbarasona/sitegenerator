import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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

    def test_image_delimiter(self):
        nodes = [
            TextNode(
                "This is an image: ![alt text](https://www.example.com/image.jpg)",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("This is an image: ", TextType.TEXT),
                TextNode(
                    "alt text", TextType.IMAGE, "https://www.example.com/image.jpg"
                ),
            ],
        )

    def test_multiple_images_delimiter(self):
        nodes = [
            TextNode(
                "This is an image: ![alt1](https://www.example.com/image1.jpg) Image 2: ![alt2](https://www.example.com/image2.jpg)",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("This is an image: ", TextType.TEXT),
                TextNode("alt1", TextType.IMAGE, "https://www.example.com/image1.jpg"),
                TextNode(" Image 2: ", TextType.TEXT),
                TextNode("alt2", TextType.IMAGE, "https://www.example.com/image2.jpg"),
            ],
        )

    def test_image_delimiter_no_images(self):
        nodes = [TextNode("This text has no images.", TextType.TEXT)]
        result = split_nodes_image(nodes)
        self.assertEqual(result, [TextNode("This text has no images.", TextType.TEXT)])

    def test_image_delimiter_ending_string(self):
        nodes = [
            TextNode(
                "This is an image: ![image text](https://www.example.com/image1.jpg) and some more text",
                TextType.TEXT,
            )
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(
            result,
            [
                TextNode("This is an image: ", TextType.TEXT),
                TextNode(
                    "image text", TextType.IMAGE, "https://www.example.com/image1.jpg"
                ),
                TextNode(" and some more text", TextType.TEXT),
            ],
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_link_delimiter(self):
        nodes = [
            TextNode(
                "This is a link: [link text](https://www.example.com)", TextType.TEXT
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("This is a link: ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://www.example.com"),
            ],
        )

    def test_multiple_links_delimiter(self):
        nodes = [
            TextNode(
                "This is a link: [link1](https://www.example.com/link1) Link 2: [link2](https://www.example.com/link2)",
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("This is a link: ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "https://www.example.com/link1"),
                TextNode(" Link 2: ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://www.example.com/link2"),
            ],
        )

    def test_link_delimiter_no_links(self):
        nodes = [TextNode("This text has no links.", TextType.TEXT)]
        result = split_nodes_link(nodes)
        self.assertEqual(result, [TextNode("This text has no links.", TextType.TEXT)])

    def test_link_delimiter_ending_string(self):
        nodes = [
            TextNode(
                "This is a link: [link text](https://www.example.com) and some more text",
                TextType.TEXT,
            )
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("This is a link: ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://www.example.com"),
                TextNode(" and some more text", TextType.TEXT),
            ],
        )

    def test_split_link_single(self):
        node = TextNode(
            "[link text](https://www.example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link text", TextType.LINK, "https://www.example.com"),
            ],
            new_nodes,
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


class TestToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **bold** and _italic_ text with a [link](https://www.example.com) and an image ![alt](https://www.example.com/image.jpg)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" and an image ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://www.example.com/image.jpg"),
            ],
        )

    def test_text_to_textnodes_no_markdown(self):
        text = "This is plain text with no markdown."
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes, [TextNode("This is plain text with no markdown.", TextType.TEXT)]
        )

    def test_text_to_textnodes_only_markdown(self):
        text = "**bold** _italic_ [link](https://www.example.com) ![alt](https://www.example.com/image.jpg)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.example.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "https://www.example.com/image.jpg"),
            ],
        )
