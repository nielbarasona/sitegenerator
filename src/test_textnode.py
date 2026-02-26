import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.LINK)
        self.assertEqual(node.url, None)

    def test_url_equal(self):
        node = TextNode("This is a text node", TextType.LINK, "https://baraso.app/")
        node2 = TextNode("This is a text node", TextType.LINK, "https://baraso.app/")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://baraso.app/")
        self.assertEqual(
            repr(node),
            "TextNode(text='This is a text node', text_type=link, url='https://baraso.app/')",
        )


if __name__ == "__main__":
    unittest.main()
