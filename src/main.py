from os import path, listdir, mkdir
from shutil import copy, rmtree


def copy_contents(src: str, dest: str):
    if path.isfile(src):
        copy(path.join(src), path.join(dest))
    else:
        files = listdir(src)
        for file in files:
            if path.isfile(path.join(src, file)):
                copy(path.join(src, file), path.join(dest, file))
            else:
                mkdir(path.join(dest, file))
                copy_contents(path.join(src, file), path.join(dest, file))


def main():
    if not path.exists("public"):
        mkdir("public")
    else:
        rmtree("public")
        mkdir("public")

    copy_contents("static", "public")


main()
