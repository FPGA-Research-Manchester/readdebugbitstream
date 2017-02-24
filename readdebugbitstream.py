#!/usr/bin/env python3
import sys

def main(argv):
    filename = argv[0]
    print filename
    f = open(filename, 'r+')
    byte = f.read(4)
    print " ".join(hex(ord(n)) for n in byte)
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
