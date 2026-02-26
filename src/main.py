from textnode import TextNode, TextType


def main():
    dummy_testnode = TextNode("Hello World", TextType.LINK, "https://baraso.app/")
    print(dummy_testnode)


if __name__ == "__main__":
    main()
