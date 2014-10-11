#!/usr/bin/env python
"""CLI tool for printing file directory structure

Usage: pfs <dir> [-d <int>]

"""
import argparse
import os

EXCLUDE_EXTS = {
    '.pyc',
    '.ico'
}

def get_items_from_dir(path):
    """Return a sorted list of all entries in path.

    This returns just the names, not the full path to the names.
    """
    items = os.listdir(path)
    items.sort()
    return items

def is_blacklisted(fname):
    """ Indicates whether the file should not be printed """
    return is_dot(fname) or is_excluded_filetype(fname)

def is_dot(f):
    """ Indicates whether this is a dot file/folder """
    return f.startswith('.')

def is_excluded_filetype(f):
    """Indicates whether the file type is not permitted

    Returns False if no extension is found
    """
    index = f.find('.')
    if index < 0:
        return False

    ext = f[index:]
    return ext in EXCLUDE_EXTS

def print_files(path, max_depth, prefix="", depth=1):
    """ Print recursive listing of contents of path """
    indent = "| "
    prefix = prefix if prefix else indent

    items = get_items_from_dir(path)
    for item in items:

        if is_blacklisted(item):
            continue

        full_path = os.path.join(path, item)

        # Recurse on subdirectories to print their files
        if os.path.isdir(item):
            if depth > max_depth:
                continue  # Too deep, don't print out files for this subdirectory
            print_files(full_path, max_depth, prefix + indent, depth + 1)

        print(prefix + item)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool for printing file directory structure')
    parser.add_argument('path', help="Path to directory to print out")
    parser.add_argument('--max_depth', '-md', type=int, default=3, help="Max recursive depth")

    args = parser.parse_args()
    print_files(path=args.path, max_depth=args.max_depth)
