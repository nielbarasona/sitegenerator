import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!", {"class": "my-p"})
        self.assertEqual(
            repr(node),
            "LeafNode(tag='p', value='Hello, world!', props={'class': 'my-p'})",
        )

    def test_parent_repr(self):
        node = ParentNode("div", [LeafNode("p", "Hello")], {"class": "my-div"})
        self.assertEqual(
            repr(node),
            "ParentNode(tag='div', children=[LeafNode(tag='p', value='Hello', props=None)], props={'class': 'my-div'})",
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_nested_parent_node(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node2])
        parent_node2 = ParentNode("div", [child_node1, parent_node])
        self.assertEqual(
            parent_node2.to_html(),
            "<div><span>child1</span><div><span>child2</span></div></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span></div>",
        )


if __name__ == "__main__":
    unittest.main()
