#!/usr/bin/env python3
import sys
from binascii import hexlify

def main(argv):
    filename = argv[0]
    print filename
    f = open(filename, 'r+')

    Sync = 0

    B1 = 0
    B2 = 0
    B3 = 0
    B4 = 0

    addr = 0
    pre_addr = 0
    BA = 0      # Block type [25:23]
    TB = 0      # Top/bottom bit [22]
    RA = 0      # Row address [21:17]
    MJA= 0      # Column address [16:7]
    MNA= 0      # Minor address [6:0]
    NoOfFr = 0

    pre_BA = BA
    pre_TB = TB
    pre_RA = RA
    pre_MJA= MJA
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
            Sync = 1
            break

    if Sync == 1:
        while True:
            word = f.read(4)

            if word == '':
                break

            word = int(hexlify(word), 16)

            if word == 0x30002001:
#                print "FAR register commands"
                word = f.read(4)
                word1 = f.read(4)
                word2 = f.read(4)
                word3 = f.read(4)

                word = int(hexlify(word), 16)
                word3 = int(hexlify(word3), 16)

                BA = (word & 0x03800000) >> 23
                TB = (word & 0x00400000) >> 22
                RA = (word & 0x003E0000) >> 17
                MJA= (word & 0x0001FF80) >> 7
                MNA= (word & 0x0000007F)
                addr = (word & ~(0x0000007F))

                # check if that frame contains no configuration data
                if pre_addr == addr and word3 != 0x30008001:
                    NoOfFr = NoOfFr + 1
                elif word3 != 0x30008001:
                    print "address:",hex(pre_addr),"column BA:",pre_BA,"TB:",pre_TB,"RA:",pre_RA,"MJA:",pre_MJA,"has no. of frames:",NoOfFr
                    NoOfFr = 1
                    pre_BA = BA
                    pre_TB = TB
                    pre_RA = RA
                    pre_MJA= MJA
                    pre_addr = addr
    else:
        print "Couldn't find the SYNC word - Invalide bitfile"

    print "end of file!"
    f.close()

if __name__ == "__main__":
    main(sys.argv[1:])
