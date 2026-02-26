import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.tag, "div")

    def test_repr(self):
        node = HTMLNode(
            tag="div", value="Hello", children=[], props={"class": "my-div"}
        )
        self.assertEqual(
            repr(node),
            "HTMLNode(tag='div', value='Hello', children=[], props={'class': 'my-div'})",
        )

    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "my-div", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="my-div" id="main"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(value="Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_repr(self):
        node = LeafNode(tag="p", value="Hello, world!", props={"class": "my-p"})
        self.assertEqual(
            repr(node),
            "LeafNode(tag='p', value='Hello, world!', props={'class': 'my-p'})",
        )


if __name__ == "__main__":
    unittest.main()
