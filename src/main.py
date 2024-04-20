from os import path, mkdir
from shutil import rmtree

from generate_page import generate_pages_recursive
from copy_contents import copy_contents


def main():
    if path.exists("public"):
        rmtree("public")
    mkdir("public")

    copy_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")


main()
