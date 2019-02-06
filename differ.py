#!/usr/bin/env python3

from git import repo
import sys



def main():
    if len(sys.argv) == 1:
        print("Usage: differ [path/to/directory]")
    else:
        directory = sys.argv[1]
        print(directory)


if __name__ == "__main__":
    main()