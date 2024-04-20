from os import path, listdir, mkdir
from shutil import copy


def copy_contents(src: str, dest: str):
    if path.isfile(src):
        copy(src, dest)
    else:
        files = listdir(src)
        for file in files:
            src_path = path.join(src, file)
            dest_path = path.join(dest, file)
            if path.isfile(src_path):
                copy(src_path, dest_path)
            else:
                mkdir(dest_path)
                copy_contents(src_path, dest_path)
