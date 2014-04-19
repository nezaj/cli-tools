#!/usr/bin/env python

"""
Usage: pfs <dir> [-d <int>]
CLI tool for printing file directory structure
"""

import argparse
import os

EXCLUDE_EXTS = [
    '.md',
    '.pyc',
    '.css',
    '.scss',
    '.ico'
]

def is_dotfile(f):
    return f[0] == '.'

def is_excluded_ext(f, exts=EXCLUDE_EXTS):
    return f[f.find('.'):] in exts

def is_too_deep(depth, max_depth=3):
    return depth > max_depth

def get_dirlist(path):
    """
    Return a sorted list of all entries in path.
    This returns just the names, not the full path to the names.
    """
    dirlist = os.listdir(path)
    dirlist.sort()
    return dirlist

def print_files(path, max_depth, prefix="", depth=1):
    " Print recursive listing of contents of path "
    indent = "| "
    if prefix == "":
        print os.path.abspath(path)
        prefix = indent

    dirlist = get_dirlist(path)
    for f in dirlist:
        if is_dotfile(f) or is_excluded_ext(f) or is_too_deep(depth, max_depth):
            continue
        print(prefix + f)
        fullname = os.path.join(path, f)
        if os.path.isdir(fullname):
            print_files(fullname, max_depth, prefix + indent, depth + 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for printing file directory structure')
    parser.add_argument('path', help="Path to directory to print out")
    parser.add_argument('--depth', '-d', type=int, default=3, help="Max recursive depth")

    args = parser.parse_args()
    print_files(path=args.path, max_depth=args.depth)
