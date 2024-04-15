from textnode import TextNode
from htmlnode import HTMLNode


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)
    htmlnode = HTMLNode(
        "a", "link tag", None, {"href": "https://www.boot.dev", "target": "_blank"}
    )
    print(htmlnode)


main()
