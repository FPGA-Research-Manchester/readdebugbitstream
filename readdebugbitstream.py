#!/usr/bin/env python3
import sys
from binascii import hexlify

def main(argv):
    filename = argv[0]
    print filename
    f = open(filename, 'r+')

    B1 = 0
    B2 = 0
    B3 = 0
    B4 = 0
    while True:
#    for i in range(200):
        B4 = B3
        B3 = B2
        B2 = B1

        byte = f.read(1)

        if byte == '':
            break

        byte = hexlify(byte)
        B1 = int(byte, 16)
#        print B4,B3,B2,B1
#        print hex(B4),hex(B3),hex(B2),hex(B1)
        if B4 == 0xaa and B3 == 0x99 and B2 == 0x55 and B1 == 0x66:
            print "Sync Word!"

    print "end of file!"
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
